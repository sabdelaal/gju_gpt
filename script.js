// public/script.js
async function searchEmail() {
    const staffName = document.getElementById('staffName').value;
    const resultDiv = document.getElementById('result');

    try {
        const response = await fetch('http://127.0.0.1:5000/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ staffName }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        if (data.success) {
            resultDiv.innerText = `Email: ${data.email}`;
        } else {
            resultDiv.innerText = `Error: ${data.error}`;
        }
    } catch (error) {
        resultDiv.innerText = `Error: ${error.message}`;
    }
}
