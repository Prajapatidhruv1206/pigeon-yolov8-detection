document.addEventListener('DOMContentLoaded', () => {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const loader = document.getElementById('loader');
    
    const thumbnailsGrid = document.getElementById('thumbnailsGrid');
    const resultImage = document.getElementById('resultImage');
    const imagePlaceholder = document.getElementById('imagePlaceholder');
    const jsonOutput = document.getElementById('jsonOutput');

    const confSlider = document.getElementById('confSlider');
    const iouSlider = document.getElementById('iouSlider');
    const confValue = document.getElementById('confValue');
    const iouValue = document.getElementById('iouValue');

    let currentFile = null;

    // Sliders event listeners
    function updatePrediction() {
        if (currentFile) {
            handleFile(currentFile, false);
        }
    }

    confSlider.addEventListener('input', (e) => {
        confValue.textContent = e.target.value + '%';
    });
    
    confSlider.addEventListener('change', () => {
        updatePrediction();
    });

    iouSlider.addEventListener('input', (e) => {
        iouValue.textContent = e.target.value + '%';
    });

    iouSlider.addEventListener('change', () => {
        updatePrediction();
    });

    // Click to upload
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });

    // Drag and drop events
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        uploadArea.addEventListener(eventName, () => {
            uploadArea.style.borderColor = 'var(--primary)';
            uploadArea.style.background = 'var(--bg-light)';
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        uploadArea.addEventListener(eventName, () => {
            uploadArea.style.borderColor = 'var(--border-color)';
            uploadArea.style.background = 'var(--bg-white)';
        }, false);
    });

    uploadArea.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;

        if (files && files.length > 0) {
            handleFile(files[0], true);
        }
    }

    fileInput.addEventListener('change', function() {
        if (this.files && this.files.length > 0) {
            handleFile(this.files[0], true);
        }
    });

    function handleFile(file, isNewUpload = true) {
        if (!file.type.startsWith('image/')) {
            alert('Please upload an image file.');
            return;
        }

        currentFile = file;

        // Show Loader
        loader.classList.remove('hidden');

        // Create form data
        const formData = new FormData();
        formData.append('file', file);
        formData.append('conf', confSlider.value / 100.0);
        formData.append('iou', iouSlider.value / 100.0);

        // Send to backend
        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            loader.classList.add('hidden');
            
            if (data.success) {
                const imageUrl = data.image_url + "?t=" + new Date().getTime();
                
                // Show in Center Viewer
                imagePlaceholder.style.display = 'none';
                resultImage.src = imageUrl;
                resultImage.style.display = 'block';

                if (isNewUpload) {
                    // Add to thumbnails grid
                    addThumbnail(imageUrl);
                }

                // Update JSON Output
                const outputData = {
                    "predictions": data.predictions_data || []
                };

                jsonOutput.textContent = JSON.stringify(outputData, null, 2);

            } else {
                alert('Error processing image: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            loader.classList.add('hidden');
            alert('Something went wrong contacting the server.');
        });
    }

    function addThumbnail(url) {
        // Remove active class from all existing
        document.querySelectorAll('.thumbnail').forEach(t => t.classList.remove('active'));

        const img = document.createElement('img');
        img.src = url;
        img.className = 'thumbnail active';
        
        img.addEventListener('click', function() {
            document.querySelectorAll('.thumbnail').forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            imagePlaceholder.style.display = 'none';
            resultImage.src = this.src;
            resultImage.style.display = 'block';
            
            // Note: Since we don't save JSON output per file in frontend, switching thumbnails 
            // won't automatically revert JSON or slider values for past images in this simple implementation.
        });

        // Insert at beginning
        thumbnailsGrid.insertBefore(img, thumbnailsGrid.firstChild);
    }
});
