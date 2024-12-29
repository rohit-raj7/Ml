document.getElementById('upload-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const formData = new FormData();
    const imageInput = document.getElementById('image');
    formData.append('image', imageInput.files[0]);

    const response = await fetch('/predict', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    const outputDiv = document.getElementById('output');

    if (result.error) {
        outputDiv.innerHTML = `<p style="color: red;">Error: ${result.error}</p>`;
    } else {
        outputDiv.innerHTML = `<p>Class: <strong>${result.class}</strong></p>
                               <p>Confidence: <strong>${result.confidence}</strong></p>`;
    }
});
