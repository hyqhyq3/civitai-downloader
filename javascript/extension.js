function download(btn, url, type) {
    btn.disabled = "disabled"
    btn.value = "Downloading..."

    tb_url = gradioApp().querySelector('#tb_url textarea')
    tb_url.value = url
    updateInput(tb_url)

    tb_type = gradioApp().querySelector('#tb_type textarea')
    tb_type.value = type
    updateInput(tb_type)
    

    gradioApp().querySelector('#btn_download').click()
}