document.addEventListener('DOMContentLoaded', function () {
    const imageInput = document.getElementById('image-upload');
    const preview = document.getElementById('preview');
    const previewContainer = document.getElementById('preview-container');
    const uploadForm = document.getElementById('upload-form');
    const resultContainer = document.getElementById('result-container');
    const resultImg = document.getElementById('result-img');
    const resetBtn = document.getElementById('reset-btn');
    const nightModeToggle = document.getElementById('night-mode-toggle');
    const nightModeIcon = document.getElementById('night-mode-icon');

    // Night mode logic
    function setNightMode(on) {
        if (on) {
            document.body.classList.add('night-mode');
            nightModeIcon.textContent = '☀️';
            localStorage.setItem('nightMode', 'on');
        } else {
            document.body.classList.remove('night-mode');
            nightModeIcon.textContent = '🌙';
            localStorage.setItem('nightMode', 'off');
        }
    }
    if (nightModeToggle) {
        nightModeToggle.addEventListener('click', function () {
            setNightMode(!document.body.classList.contains('night-mode'));
        });
        // Restore preference
        if (localStorage.getItem('nightMode') === 'on') {
            setNightMode(true);
        }
    }

    imageInput.addEventListener('change', function () {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        } else {
            preview.src = '#';
            preview.style.display = 'none';
        }
    });

    uploadForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const file = imageInput.files[0];
        if (!file) return;
        const formData = new FormData();
        formData.append('image', file);
        resultContainer.classList.remove('active');
        resultImg.style.display = 'none';
        fetch('/predict', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) throw new Error('Prediction failed');
            return response.blob();
        })
        .then(blob => {
            const url = URL.createObjectURL(blob);
            resultImg.src = url;
            resultImg.style.display = 'block';
            resultContainer.classList.add('active');
        })
        .catch(() => {
            alert('Prediction failed. Please try again.');
        });
    });

    resetBtn.addEventListener('click', function () {
        imageInput.value = '';
        preview.src = '#';
        preview.style.display = 'none';
        resultImg.src = '#';
        resultImg.style.display = 'none';
        resultContainer.classList.remove('active');
    });
}); 