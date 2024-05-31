function uploadFolder() {
    let input = document.createElement('input');
    input.type = 'file';
    input.webkitdirectory = true;
    input.onchange = e => {
        let files = e.target.files;
        if (files.length > 500) {
            alert('The number of files should not exceed 500');
            return;
        }
        let formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            if (!files[i].type.startsWith('image/')) {
                alert('Only image files are allowed!');
                continue;
            }
            if (files[i].size > 50000000) { 
                alert('File size should not exceed 50 MB');
                continue;
            }
            formData.append('files[]', files[i]);
        }

        document.getElementById('loading-message').style.display = 'block';
        fetch('/upload_folder', {
            method: 'POST',
            body: formData
        }).then(response => {
            return response.text();
        }).then(data => {
            alert('Папка загружена: ' + data);
            var iframe = parent.document.getElementById('contentFrame');
            iframe.src = 'main';
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
        if (file.size > 300000000) {
            alert('ZIP file size should not exceed 300 MB');
            return;
        }
        let formData = new FormData();
        formData.append('file', file);

        document.getElementById('loading-message').style.display = 'block';
        fetch('/upload_zip', {
            method: 'POST',
            body: formData
        }).then(response => {
            return response.text();
        }).then(data => {
            alert('ZIP загружен: ' + data);
            var iframe = parent.document.getElementById('contentFrame');
            iframe.src = 'main';
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
        fileInput.click();
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
        uploadFiles(files);
    }
    
    function uploadFiles(files) {
        let formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            if (!files[i].type.startsWith('image/')) {
                alert('Only image files are allowed!');
                continue;
            }
            if (files[i].size > 50000000) {
                alert('File size should not exceed 50MB');
                continue;
            }
            formData.append('files[]', files[i]);
        }
    
        if (formData.has('files[]')) {
            document.getElementById('loading-message').style.display = 'block';
            fetch('/upload_file', {
                method: 'POST',
                body: formData
            }).then(response => response.text())
              .then(data => {
                alert('Files uploaded: ' + data)
                var iframe = parent.document.getElementById('contentFrame');
                iframe.src = 'main';
            })
              .catch(error => alert('Error uploading files: ' + error));
        }
    }
});

function handleFiles(files) {
    let formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        if (!files[i].type.startsWith('image/')) {
            alert('Only image files are allowed!');
            continue;
        }
        if (files[i].size > 50000000) {
            alert('File size should not exceed 50 MB');
            continue;
        }
        formData.append('files[]', files[i]);
    }

    document.getElementById('loading-message').style.display = 'block';
    if (formData.has('files[]')) {
        fetch('/upload_file', {
            method: 'POST',
            body: formData
        }).then(response => response.text())
          .then(data => {
              alert('Files uploaded: ' + data);
              var iframe = parent.document.getElementById('contentFrame');
              iframe.src = 'main';
          })
          .catch(error => alert('Error uploading files: ' + error));
    }
}