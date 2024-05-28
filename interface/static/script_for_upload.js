function uploadFolder() {
    // Получаем выбранный файл/папку
    let input = document.createElement('input');
    input.type = 'file';
    input.webkitdirectory = true;
    input.onchange = e => {
        let files = e.target.files;
        let formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append('files[]', files[i]);
        }

        // Отправляем файлы на сервер
        fetch('/upload_folder', {
            method: 'POST',
            body: formData
        }).then(response => {
            return response.text();
        }).then(data => {
            alert('Папка загружена: ' + data);
        }).catch(error => {
            alert('Ошибка загрузки: ' + error);
        });
    };
    input.click();
}

function uploadZip() {
    let input = document.createElement('input');
    input.type = 'file';
    input.accept = '.zip';
    input.onchange = e => {
        let file = e.target.files[0];
        let formData = new FormData();
        formData.append('file', file);

        // Отправляем файл на сервер
        fetch('/upload_zip', {
            method: 'POST',
            body: formData
        }).then(response => {
            return response.text();
        }).then(data => {
            alert('ZIP загружен: ' + data);
        }).catch(error => {
            alert('Ошибка загрузки: ' + error);
        });
    };
    input.click();
}


