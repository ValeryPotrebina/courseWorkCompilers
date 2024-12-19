function solveMath() {


    // TODO:ПОЧЕМУ ТО НЕ СЧИТАЕТСЯ КОРЕНЬ X = 0 
    // cкладывать числа
    // graph генерировать точки и для более 2х переменных
    const mathInput = document.getElementById('mathInput').value;
    
    const resultDiv = document.getElementById('result');

    const rootsList = document.getElementById('rootsList');

    const points = document.getElementById('points');


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

            const latexResult = convertToLatex(data.result);
            resultDiv.innerHTML = `<strong>Result:</strong> $$${latexResult}$$`;

            // roots.innerText = `${JSON.stringify(data.roots)}`;
            // points.innerText = `Points: ${JSON.stringify(data.points)}`;

            rootsList.innerHTML = '';
            
            // ????????????????????
            data.roots.forEach(root => {
                const roundedRoot = root.map(value => roundRoot(value));
                const li = document.createElement('li');
                li.innerText = `Root: ${roundedRoot.join(', ')}`;
                rootsList.appendChild(li);
            });

            plotGraph(data.points, data.roots);

            MathJax.Hub.Queue(["Typeset", MathJax.Hub, resultDiv]);
        }
    })
    .catch(error => {
        resultDiv.innerText = 'Error: ' + error.message;
    });
}

function convertToLatex(expression) {
    expression = expression.replace(/^\((.*)\)$/, '$1'); // удаляем скобки по бокам
    expression = expression.replace(/\(([^\s]+)\)/g, '$1'); 
    expression = expression.replace(/([0-9]+)\.0/g, '$1');
    expression = expression.replace(/\(([^\+\-]+)\)/g, '$1');
    expression = expression.replace(/\*/g, '');
    return expression;
}
function roundRoot(value, eps=1e-5) {
    return Math.abs(value - Math.round(value)) < eps ? Math.round(value) : value
}

function plotGraph(points, roots) {
    const graph = document.getElementById('graph');
    const dimension = points[0].point.length;

    if (dimension == 1) {
        const xValues = points.map(point => point.point[0]);
        const yValues = points.map(point => point.value);
        const trace = {
            x: xValues,
            y: yValues,
            mode: 'lines',
            type: 'scatter'
        };

        const rootValues = roots.map(root => root[0]);
        const rootTrace = {
            x: rootValues,
            y: rootValues.map(() => 0),
            mode: 'markers',
            type: 'scatter',
            name: 'Roots',
            marker: { color: 'red' }
        }

        const layout = {
            title: '2D Graph',
            xaxis: { title: 'X' },
            yaxis: { title: 'Y' }
        };

        Plotly.newPlot(graph, [trace, rootTrace], layout);
    } else if (dimension === 2) {
        // Трехмерный график
        const xValues = points.map(point => point.point[0]);
        const yValues = points.map(point => point.point[1]);
        const zValues = points.map(point => point.value);

        const trace = {
            x: xValues,
            y: yValues,
            z: zValues,
            mode: 'markers',
            type: 'scatter3d',
            name: 'Function',
            marker: { size: 3 }
        };
        const layout = {
            title: '3D Graph',
            scene: {
                xaxis: { title: 'X' },
                yaxis: { title: 'Y' },
                zaxis: { title: 'Z' }
            }
        };

        Plotly.newPlot(graph, [trace], layout);
    } else {
        graph.innerText = 'Unsupported dimension';
    }



}