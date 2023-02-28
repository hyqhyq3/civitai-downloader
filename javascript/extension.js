function download(btn, url, type, name) {
    btn.disabled = "disabled"
    btn.value = "Downloading..."

    tb_url = gradioApp().querySelector('#tb_url textarea')
    tb_url.value = url
    updateInput(tb_url)

    tb_type = gradioApp().querySelector('#tb_type textarea')
    tb_type.value = type
    updateInput(tb_type)

    tb_name = gradioApp().querySelector('#tb_name textarea')
    tb_name.value = name
    updateInput(tb_name)
    

    gradioApp().querySelector('#btn_download').click()
}