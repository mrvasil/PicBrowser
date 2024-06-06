document.addEventListener("DOMContentLoaded", function() {
    const thumbnails = document.querySelectorAll('.thumbnail img');
    const mainImageViewer = document.querySelector('.image-viewer img');
    const deleteButton = document.getElementById('delete-image-btn');
    const filenameDisplay = document.querySelector('.image-details h2');
    const resetButton = document.getElementById('reset-image-btn');
    const imageContainer = document.querySelector('.image-viewer-inside');
    const image = imageContainer.querySelector('img');
    const prevImageButton = document.getElementById('prev-image-btn');
    const nextImageButton = document.getElementById('next-image-btn');

    let initialDistance = null;
    let currentIndex = 0;
    let isDragging = false;
    let originX, originY;
    let translateX = 0, translateY = 0;
    let scale = 1;

    if (thumbnails.length > 0) {
        const firstThumbnail = thumbnails[0];
        mainImageViewer.src = firstThumbnail.src;
        mainImageViewer.dataset.filename = firstThumbnail.dataset.filename;
        filenameDisplay.textContent = firstThumbnail.dataset.filename.split('\\').pop().split('/').pop();
        fetchMetadata(firstThumbnail.dataset.filename);
    }

    prevImageButton.addEventListener('click', function() {
        if (currentIndex > 0) {
            currentIndex--;
            changeImage(currentIndex);
        }
    });

    nextImageButton.addEventListener('click', function() {
        if (currentIndex < thumbnails.length - 1) {
            currentIndex++;
            changeImage(currentIndex);
        }
    });

    thumbnails.forEach((thumbnail, index) => {
        thumbnail.addEventListener('click', function() {
            if (!this.parentElement.classList.contains('selected')) {
                thumbnails.forEach(img => img.parentElement.classList.remove('selected'));
                this.parentElement.classList.add('selected');
                mainImageViewer.src = this.src;
                mainImageViewer.dataset.filename = this.dataset.filename;
                filenameDisplay.textContent = this.dataset.filename.split('\\').pop().split('/').pop();
                fetchMetadata(this.dataset.filename);
                resetTransform();
                currentIndex = index;
            }
        });
    });

    function changeImage(index) {
        const newImage = thumbnails[index];
        mainImageViewer.src = newImage.src;
        mainImageViewer.dataset.filename = newImage.dataset.filename;
        filenameDisplay.textContent = newImage.dataset.filename.split('\\').pop().split('/').pop();
        fetchMetadata(newImage.dataset.filename);
        thumbnails.forEach(thumb => thumb.parentElement.classList.remove('selected'));
        newImage.parentElement.classList.add('selected');
        resetTransform();
    }

    deleteButton.addEventListener('click', function() {
        const filename = mainImageViewer.dataset.filename;
        if (filename) {
            deleteImage(filename);
        } else {
            alert('No image selected for deletion.');
        }
    });

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

    imageContainer.addEventListener('touchstart', function(e) {
        if (e.touches.length === 1) {
            isDragging = true;
            originX = e.touches[0].clientX;
            originY = e.touches[0].clientY;
        } else if (e.touches.length === 2) {
            initialDistance = Math.hypot(
                e.touches[0].pageX - e.touches[1].pageX,
                e.touches[0].pageY - e.touches[1].pageY
            );
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
        } else if (e.touches.length === 2) {
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

    resetButton.addEventListener('click', function() {
        resetTransform();
    });

    function updateTransform() {
        image.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
    }

    function resetTransform() {
        translateX = 0;
        translateY = 0;
        scale = 1;
        updateTransform();
    }

    function fetchMetadata(filename) {
        fetch('/get_metadata/' + filename)
            .then(response => response.json())
            .then(data => {
                let metadataHtml = '';
                for (const key in data) {
                    metadataHtml += `<b>${key}:</b> ${data[key]} <br>`;
                }
                document.getElementById('metadata').innerHTML = metadataHtml;
            })
            .catch(error => console.error('Error fetching metadata:', error));
    }
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


document.addEventListener("DOMContentLoaded", function() {
    const thumbnails = document.querySelectorAll('.thumbnail');
    let draggedItem = null;

    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('dragstart', function(e) {
            draggedItem = thumbnail;
            setTimeout(() => thumbnail.classList.add('dragging'), 0);
        });

        thumbnail.addEventListener('dragend', function(e) {
            setTimeout(() => thumbnail.classList.remove('dragging'), 0);
            updateImagePosition(draggedItem);
        });
    });

    const container = document.querySelector('.thumbnail-container');
    container.addEventListener('dragover', function(e) {
        e.preventDefault();
        const afterElement = getDragAfterElement(container, e.clientY);
        if (afterElement == null) {
            container.appendChild(draggedItem);
        } else {
            container.insertBefore(draggedItem, afterElement);
        }
    });

    function getDragAfterElement(container, x, y) {
        const draggableElements = [...container.querySelectorAll('.thumbnail:not(.dragging)')];
    
        return draggableElements.reduce((closest, child) => {
            const box = child.getBoundingClientRect();
            const offsetX = x - box.left - box.width / 2;
            const offsetY = y - box.top - box.height / 2;
            const offsetDist = Math.sqrt(offsetX * offsetX + offsetY * offsetY);
    
            if (offsetDist < closest.dist) {
                return { dist: offsetDist, element: child };
            } else {
                return closest;
            }
        }, { dist: Number.POSITIVE_INFINITY }).element;
    }
    
    container.addEventListener('dragover', function(e) {
        e.preventDefault();
        const afterElement = getDragAfterElement(container, e.clientX, e.clientY);
        if (afterElement == null) {
            container.appendChild(draggedItem);
        } else {
            container.insertBefore(draggedItem, afterElement);
        }
    });

    function updateImagePosition(draggedItem) {
        const allThumbnails = [...container.querySelectorAll('.thumbnail')];
        const newIndex = allThumbnails.indexOf(draggedItem);
        const filename = draggedItem.querySelector('img').dataset.filename;

        fetch('/image_number', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ number: newIndex, filename: filename })
        })
        .then(response => response.json())
        .then(data => console.log('Success:', data))
        .catch((error) => console.error('Error:', error));
    }
});