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




document.addEventListener('DOMContentLoaded', function() {
    let dropArea = document.getElementById('drag-drop-area');
    let fileInput = document.getElementById('file-input');

    dropArea.addEventListener('click', function() {
        fileInput.click(); // Активирует скрытый input при клике на область drag&drop
    });

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => dropArea.classList.add('drag-over'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => dropArea.classList.remove('drag-over'), false);
    });

    dropArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        let dt = e.dataTransfer;
        let files = dt.files;
        uploadFiles(files); // Функция для загрузки файлов
    }
    
    function uploadFiles(files) {
        let formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append('files[]', files[i]);
        }
    
        fetch('/upload_file', {
            method: 'POST',
            body: formData
        }).then(response => response.text())
          .then(data => alert('Files uploaded: ' + data))
          .catch(error => alert('Error uploading files: ' + error));
    }
});

function handleFiles(files) {
    let formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append('files[]', files[i]);
    }

    fetch('/upload_file', {
        method: 'POST',
        body: formData
    }).then(response => response.text())
      .then(data => alert('Files uploaded: ' + data))
      .catch(error => alert('Error uploading files: ' + error));
}