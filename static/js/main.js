
class ObjectMeasurement {
    constructor() {
        this.video = document.getElementById('video');
        this.originalCanvas = document.getElementById('originalCanvas');
        this.processedImage = document.getElementById('processedImage');
        this.originalCtx = this.originalCanvas.getContext('2d');
        
        this.stream = null;
        this.capturedImageData = null;
        
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        document.getElementById('startCamera').addEventListener('click', () => this.startCamera());
        document.getElementById('captureImage').addEventListener('click', () => this.captureImage());
        document.getElementById('processImage').addEventListener('click', () => this.processImage());
        document.getElementById('uploadProcess').addEventListener('click', () => this.uploadAndProcess());
        
        // File input handler
        document.getElementById('fileInput').addEventListener('change', (e) => {
            document.getElementById('uploadProcess').disabled = !e.target.files[0];
        });
        
        // Update threshold value display
        document.getElementById('threshold').addEventListener('input', (e) => {
            document.getElementById('thresholdValue').textContent = e.target.value;
        });
        
        // Update blur value display
        document.getElementById('blur').addEventListener('input', (e) => {
            document.getElementById('blurValue').textContent = e.target.value;
        });
    }

    async startCamera() {
        try {
            this.stream = await navigator.mediaDevices.getUserMedia({ 
                video: { width: 640, height: 480 } 
            });
            this.video.srcObject = this.stream;
            
            document.getElementById('startCamera').disabled = true;
            document.getElementById('captureImage').disabled = false;
        } catch (err) {
            this.showError('Error accessing camera: ' + err.message);
        }
    }

    captureImage() {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        canvas.width = this.video.videoWidth;
        canvas.height = this.video.videoHeight;
        ctx.drawImage(this.video, 0, 0);
        
        this.capturedImageData = canvas.toDataURL('image/png');
        
        // Display original image
        this.originalCanvas.width = canvas.width;
        this.originalCanvas.height = canvas.height;
        this.originalCtx.drawImage(this.video, 0, 0);
        
        document.getElementById('processImage').disabled = false;
        
        // Stop camera
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }
        this.video.srcObject = null;
        document.getElementById('startCamera').disabled = false;
        document.getElementById('captureImage').disabled = true;
    }

    async uploadAndProcess() {
        const fileInput = document.getElementById('fileInput');
        const file = fileInput.files[0];
        
        if (!file) {
            this.showError('Please select a file');
            return;
        }

        this.showLoading(true);
        
        try {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('threshold', document.getElementById('threshold').value);
            formData.append('blur_amount', document.getElementById('blur').value);
            formData.append('pixel_ratio', document.getElementById('pixelRatio').value);

            const response = await fetch('/upload_image', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            
            if (result.error) {
                this.showError(result.error);
            } else {
                // Display uploaded image in canvas
                const img = new Image();
                img.onload = () => {
                    this.originalCanvas.width = img.width;
                    this.originalCanvas.height = img.height;
                    this.originalCtx.drawImage(img, 0, 0);
                };
                img.src = URL.createObjectURL(file);
                
                this.displayResults(result);
            }
        } catch (error) {
            this.showError('Upload failed: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }

    async processImage() {
        if (!this.capturedImageData) {
            this.showError('Please capture an image first');
            return;
        }

        this.showLoading(true);

        try {
            const response = await fetch('/process_image', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    image_data: this.capturedImageData,
                    threshold: document.getElementById('threshold').value,
                    blur_amount: document.getElementById('blur').value,
                    pixel_ratio: document.getElementById('pixelRatio').value
                })
            });

            const result = await response.json();
            
            if (result.error) {
                this.showError(result.error);
            } else {
                this.displayResults(result);
            }
        } catch (error) {
            this.showError('Processing failed: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }

    displayResults(result) {
        // Hide error display
        document.getElementById('errorDisplay').classList.add('hidden');
        
        // Display processed image
        if (result.processed_image) {
            this.processedImage.src = result.processed_image;
            this.processedImage.style.display = 'block';
        }
        
        // Update results display
        document.getElementById('diameter').textContent = result.diameter_mm + ' mm';
        document.getElementById('category').textContent = result.category;
        document.getElementById('pixelRadius').textContent = result.radius_pixels + ' px';
        document.getElementById('results').classList.remove('hidden');
    }

    showError(message) {
        document.getElementById('errorMessage').textContent = message;
        document.getElementById('errorDisplay').classList.remove('hidden');
        document.getElementById('results').classList.add('hidden');
    }

    showLoading(show) {
        const spinner = document.getElementById('loadingSpinner');
        const text = document.getElementById('processText');
        const button = document.getElementById('processImage');
        
        if (show) {
            spinner.classList.remove('active');
            spinner.style.display = 'inline-flex';
            text.style.display = 'none';
            button.disabled = true;
        } else {
            spinner.style.display = 'none';
            text.style.display = 'inline';
            button.disabled = false;
        }
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    new ObjectMeasurement();
});
