print("hello")
import gradio as gr
import re, os.path
import requests
import json
import html
from modules import script_callbacks,ui
import subprocess

tasks = []

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
            if os.path.exists(lfn):
                exists = True
            btn_code = f"""<input type=button onclick="download(this, '{html.escape(url)}', '{html.escape(model_type)}')" value={'downloaded' if exists else 'download'} {'disabled' if exists else ''} class="gr-button gr-button-lg gr-button-secondary"></input>"""
            code += f'<tr><td>{vn}</td><td>{fmt}</td><td>{size} MB</td><td>{btn_code}</td></tr>'

    code += '</tbody></table>'

    code += "</div>"
    return [code]

def get_path_by_type(t):
    if t == 'LORA':
        return 'models/Lora'
    elif t == 'Checkpoint':
        return 'models/Stable-diffusion'

def download(u,t):
    download_path = get_path_by_type(t)
    
    aria2c = f"aria2c -x 16 -s 16 -d {download_path} {u}"
    subprocess.Popen(aria2c, shell=True)
    return 

def on_ui_tabs():
    print("tabui")
    with gr.Blocks() as interface:
        with gr.Row():
            with gr.Column():
                tb_input = gr.Textbox(label='civit url', interactive=True, value="https://civitai.com/models/5743/style-jelly")
                btn_fetch = gr.Button(value='fetch')

                tb_url = gr.Text(elem_id='tb_url', visible=False)
                tb_type = gr.Text(elem_id='tb_type', visible=False)
                btn_download = gr.Button(elem_id='btn_download', visible=False)
        with gr.Row():
            version_list = gr.HTML()

        btn_fetch.click(
                fn=fetch, 
                inputs=[tb_input], 
                outputs=[version_list])
        
        btn_download.click(
                fn=download,
                inputs=[tb_url, tb_type],
                outputs=[])
    return [(interface, "myext", "mytext")]


script_callbacks.on_ui_tabs(on_ui_tabs)

