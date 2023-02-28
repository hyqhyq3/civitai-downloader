import gradio as gr
import re, os.path
import requests
import json
import html
from modules import script_callbacks,ui
import subprocess
import threading
import requests

class Task(object):
    downloaded = 0
    total = 0
    name = ''
    url = ''

class Manager(object):

    def __init__(self):
        self.tasks = {}

    def download(self,u,n):
        task = Task()
        task.url = u
        task.name = n
        name = os.path.basename(n)

        self.tasks[name] = task

        task.thread = threading.Thread(target=Manager._download, args=[self, task])
        task.thread.start()

    def _download(self,t):
        with requests.get(t.url, stream=True, allow_redirects=True, verify=False) as r:
            r.raise_for_status()
            t.total = int(r.headers.get('content-length', 0))
            print("file name: %s" % t.name)
            print("file size: %d" % t.total)
            with open(t.name, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    if chunk:
                        f.write(chunk)
                        t.downloaded += len(chunk)
        return

    def get_progress(self, n):
        if n not in self.tasks:
            print(f'{n} not found')
            return 1
        return self.tasks[n].downloaded * 1.0 / self.tasks[n].total if self.tasks[n].total > 0 else 1
    
    # finalize
    def __del__(self):
        for t in self.tasks.values():
            t.thread.join()


manager = Manager()

def fetch(u):
    regexp = re.compile("https://civitai.com/models/(\d+)/.*")
    m = regexp.match(u)
    if m is None:
        return
    id = m[1]
    resp = requests.get("https://civitai.com/api/v1/models/%s" % id)
    info = resp.json()

    name = info.get('name')
    model_type = info.get('type')
    description = info.get('description')

    code = "<div>"

    code += f"<div>Name: {name}</div>"
    code += f"<div>Type: {model_type}</div>"
    code += f"<div>Description: {description}</div>"
    code += '<table><tbody>'
    for ver in info.get('modelVersions'):
        vn = ver.get('name')
        for f in ver.get('files'):
            fn = f.get('name')
            fmt = f.get('format')
            size = int(f.get('sizeKB') / 1024)
            url = f.get('downloadUrl')
            lfn = os.path.join(get_path_by_type(model_type),fn)
            exists = False
            progress = 100
            if os.path.exists(lfn):
                exists = True
                progress = manager.get_progress(fn)*100
            btn_code = f"""<input type=button onclick="download(this, '{html.escape(url)}', '{html.escape(model_type)}', '{html.escape(fn)}')" value={ '%d%%' % progress if progress < 100 else 'downloaded' if exists else 'download'} {'disabled' if exists else ''} class="gr-button gr-button-lg gr-button-secondary"></input>"""
            code += f'<tr><td>{vn}</td><td>{fmt}</td><td>{size} MB</td><td>{btn_code}</td></tr>'

    code += '</tbody></table>'

    code += "</div>"
    return [code]

def get_path_by_type(t):
    if t == 'LORA':
        return 'models/Lora'
    elif t == 'Checkpoint':
        return 'models/Stable-diffusion'

def download(u,t,n):
    # reject slash and backslash
    if re.search(r'[/\\]|(^\.\.)', n):
        return 'invalid name'
    # reject if url not start with https://civitai.com/api/download
    if not u.startswith('https://civitai.com/api/download/models'):
        return 'invalid url'
    download_path = get_path_by_type(t)
    manager.download(u, os.path.join(download_path,n))
    return 'download started'

def on_ui_tabs():
    print("tabui")
    with gr.Blocks() as interface:
        with gr.Row():
            with gr.Column():
                tb_input = gr.Textbox(label='civit url', interactive=True, value="")
                btn_fetch = gr.Button(value='fetch')

                console = gr.Text(elem_id='console')

                tb_url = gr.Text(elem_id='tb_url', visible=False)
                tb_type = gr.Text(elem_id='tb_type', visible=False)
                tb_name = gr.Text(elem_id='tb_name', visible=False)
                btn_download = gr.Button(elem_id='btn_download', visible=False)
        with gr.Row():
            version_list = gr.HTML()

        btn_fetch.click(
                fn=fetch, 
                inputs=[tb_input], 
                outputs=[version_list])
        
        btn_download.click(
                fn=download,
                inputs=[tb_url, tb_type, tb_name],
                outputs=[console])
    return [(interface, "CivitDownloader", "CivitDownloader")]


script_callbacks.on_ui_tabs(on_ui_tabs)

