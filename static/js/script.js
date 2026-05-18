let selectedFile = null;

const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const browseBtn = document.getElementById('browseBtn');
const previewSection = document.getElementById('previewSection');
const imagePreview = document.getElementById('imagePreview');
const removeBtn = document.getElementById('removeBtn');
const analyzeBtn = document.getElementById('analyzeBtn');
const loading = document.getElementById('loading');
const resultSection = document.getElementById('resultSection');
const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');
const newAnalysisBtn = document.getElementById('newAnalysisBtn');
const retryBtn = document.getElementById('retryBtn');

// Click to browse
browseBtn.addEventListener('click', () => fileInput.click());
uploadArea.addEventListener('click', () => fileInput.click());

// File input change
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) handleFile(file);
});

// Drag and drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
});

// Handle file selection
function handleFile(file) {
    if (!file.type.match('image.*')) {
        showError('Please select a valid image file (PNG, JPG, JPEG)');
        return;
    }

    selectedFile = file;

    const reader = new FileReader();
    reader.onload = (e) => {
        imagePreview.src = e.target.result;
        uploadArea.style.display = 'none';
        previewSection.style.display = 'block';
        analyzeBtn.disabled = false;
        hideResults();
    };
    reader.readAsDataURL(file);
}

// Remove image
removeBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    resetUpload();
});

// Analyze button
analyzeBtn.addEventListener('click', async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('file', selectedFile);

    hideResults();
    loading.style.display = 'block';
    analyzeBtn.disabled = true;

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            displayResults(data);
        } else {
            showError(data.error || 'An error occurred during analysis');
        }
    } catch (error) {
        showError('Network error. Please check your connection and try again.');
    } finally {
        loading.style.display = 'none';
    }
});

// Display results
function displayResults(data) {
    const predictionBadge = document.getElementById('predictionBadge');
    const predictionText = document.getElementById('predictionText');
    const confidenceValue = document.getElementById('confidenceValue');
    const realBar = document.getElementById('realBar');
    const fakeBar = document.getElementById('fakeBar');
    const realValue = document.getElementById('realValue');
    const fakeValue = document.getElementById('fakeValue');

    predictionText.textContent = data.prediction;
    predictionBadge.className = `prediction-badge ${data.prediction}`;
    confidenceValue.textContent = `${data.confidence.toFixed(2)}%`;

    realBar.style.width = `${data.real_probability}%`;
    fakeBar.style.width = `${data.fake_probability}%`;
    realValue.textContent = `${data.real_probability.toFixed(2)}%`;
    fakeValue.textContent = `${data.fake_probability.toFixed(2)}%`;

    resultSection.style.display = 'block';
}

// Show error
function showError(message) {
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
}

// Hide results
function hideResults() {
    resultSection.style.display = 'none';
    errorSection.style.display = 'none';
}

// Reset upload
function resetUpload() {
    selectedFile = null;
    fileInput.value = '';
    uploadArea.style.display = 'block';
    previewSection.style.display = 'none';
    analyzeBtn.disabled = true;
    hideResults();
}

// New analysis button
newAnalysisBtn.addEventListener('click', resetUpload);

// Retry button
retryBtn.addEventListener('click', () => {
    hideResults();
    if (selectedFile) {
        analyzeBtn.disabled = false;
    }
});
