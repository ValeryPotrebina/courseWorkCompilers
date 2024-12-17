function solveMath() {
    const mathInput = document.getElementById('mathInput').value;
    
    const resultDiv = document.getElementById('result');

    // Проверка на пустое поле ввода
    if (!mathInput) {
        resultDiv.innerText = 'Error: Please enter a math expression.';
        return;
    }

    // Отправка данных на бэкенд
    fetch('http://127.0.0.1:5000/solve', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ expression: mathInput })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            resultDiv.innerText = `Error: ${data.error}`;
        } else {
            resultDiv.innerText = `Result: ${data.result}`;
        }
    })
    .catch(error => {
        resultDiv.innerText = 'Error: ' + error.message;
    });
}
