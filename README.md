# StableDiffusion-webui的CivitAI下载插件

## 安装方式
### 方式1：手动安装
1. 进入stable-diffusion-webui的extensions，执行以下命令：
```
git clone https://github.com/hyqhyq3/civitai-downloader.git
```
2. 重启stable-diffusion-webui或者reload ui


### 方式2: 从URL安装

本方法可能会报错 `AssertionError: extension access disabled because of command line flags`, 导致安装失败, 请使用方式1

1. 在stable-diffusion-webui的extensions页面，点击“Install Extension From URL”按钮
2. 在弹出的对话框中，输入以下URL：
```
https://github.com/hyqhyq3/civitai-downloader.git
```
3. 点击“Install Extension”按钮
4. 重启stable-diffusion-webui或者reload ui

## 使用方式
1. 安装成功后,会在stable-diffusion-webui的菜单栏中出现“CivitDownloader”菜单，点击该菜单，即可进入CivitAI下载器页面。
2. 在CivitAI网站找到合适的模型, 复制模型页面连接, 贴入到`civit url`, 然后点击fetch按钮
3. 在下方的文件列表中, 选择需要下载的文件, 点击download按钮, 即可下载文件. 下载将会在后台异步进行, 请耐心等待
4. 如果需要查看进度, 请重新点击fetch按钮. 下载进度将会显示在原来的Download按钮上, 如果下载完成,会显示`Downloaded`字样


## 已知Bug
1. 如果碰到文件名重复的情况,可能会导致进度判断异常,但是问题不大,不影响使用
2. 暂时只支持下载LORA和Checkpoint类型的模型,其他类型的模型暂时不支持