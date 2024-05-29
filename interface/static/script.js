document.addEventListener("DOMContentLoaded", function() {
    const thumbnails = document.querySelectorAll('.thumbnail img');
    const mainImageViewer = document.querySelector('.image-viewer img');
    const deleteButton = document.getElementById('delete-image-btn');
    const filenameDisplay = document.querySelector('.image-details p');

    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', function() {
            thumbnails.forEach(img => img.parentElement.classList.remove('selected'));
            this.parentElement.classList.add('selected');
            mainImageViewer.src = this.src; 
            mainImageViewer.dataset.filename = this.dataset.filename;
            filenameDisplay.textContent = this.dataset.filename.split('\\').pop();
            filenameDisplay.textContent = this.dataset.filename.split('/').pop();
        });
    });

    deleteButton.addEventListener('click', function() {
        const filename = mainImageViewer.dataset.filename;
        if (filename) {
            deleteImage(filename);
        } else {
            alert('No image selected for deletion.');
        }
    });
});



document.addEventListener("DOMContentLoaded", function() {
const imageContainer = document.querySelector('.image-viewer-inside');
const image = imageContainer.querySelector('img');
const resetButton = document.getElementById('reset-image-btn');

let isDragging = false;
let originX, originY;
let translateX = 0, translateY = 0;
let scale = 1;
imageContainer.addEventListener('mousedown', function(e) {
    isDragging = true;
    originX = e.clientX;
    originY = e.clientY;
    e.preventDefault();
});
document.addEventListener('mouseup', function() {
    isDragging = false;
});
document.addEventListener('mousemove', function(e) {
    if (isDragging) {
        translateX += e.clientX - originX;
        translateY += e.clientY - originY;
        originX = e.clientX;
        originY = e.clientY;
        updateTransform();
    }
});
imageContainer.addEventListener('wheel', function(e) {
    if (e.ctrlKey) {
        e.preventDefault();
        scale += e.deltaY * -0.01;
        scale = Math.min(Math.max(.125, scale), 4);
        updateTransform();
    }
});
function updateTransform() {
    image.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
}

imageContainer.addEventListener('touchstart', function(e) {
    if (e.touches.length === 1) {
        isDragging = true;
        originX = e.touches[0].clientX;
        originY = e.touches[0].clientY;
    }
});
imageContainer.addEventListener('touchend', function() {
    isDragging = false;
});
imageContainer.addEventListener('touchmove', function(e) {
    if (isDragging && e.touches.length === 1) {
        translateX += e.touches[0].clientX - originX;
        translateY += e.touches[0].clientY - originY;
        originX = e.touches[0].clientX;
        originY = e.touches[0].clientY;
        updateTransform();
    }
});
// Обработка жестов pinch-to-zoom
let initialDistance = null;
imageContainer.addEventListener('touchmove', function(e) {
    if (e.touches.length === 2) {
        e.preventDefault();
        const dist = Math.hypot(
            e.touches[0].pageX - e.touches[1].pageX,
            e.touches[0].pageY - e.touches[1].pageY
        );
        if (initialDistance) {
            let deltaScale = dist / initialDistance;
            scale *= deltaScale;
            updateTransform();
        }
        initialDistance = dist;
    }
});
imageContainer.addEventListener('touchstart', function(e) {
    if (e.touches.length === 2) {
        initialDistance = Math.hypot(
            e.touches[0].pageX - e.touches[1].pageX,
            e.touches[0].pageY - e.touches[1].pageY
        );
    }
});

resetButton.addEventListener('click', function() { // Обработчик событий для сброса
    resetTransform();
});

function resetTransform() {
    translateX = 0;
    translateY = 0;
    scale = 1;
    updateTransform();
}

});

document.addEventListener("DOMContentLoaded", function() {
    fetch('/get_metadata/' + document.querySelector('.thumbnail img').dataset.filename)
        .then(response => response.text())
        .then(data => {
            document.getElementById('metadata').textContent = data;
        })
        .catch(error => console.error('Error:', error));
});

function deleteImage(filename) {
    if (filename) {
        fetch(`/delete_image/${filename}`, { method: 'DELETE' })
            .then(response => response.json())
            .then(data => {
                if (data == "Success") {
                    window.location.reload();
                } else {
                    alert('Error deleting image');
                }
            })
            .catch(error => console.error('Error:', error));
    }
}