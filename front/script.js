

const mathForm = document.querySelector('#mathForm');
const mathInput = document.getElementById('mathInput');
const submitButton = document.querySelector('#submitButton');
const resultDiv = document.getElementById('result');
const rootsList = document.getElementById('rootsList');
const points = document.getElementById('points');


let loading = false

mathForm.addEventListener('submit', (e) => {
    e.preventDefault();
    if (loading) return
    const expression = mathInput.value;
    if (!mathInput) {
        resultDiv.innerText = 'Error: Please enter a math expression.';
        return;
    }
    setLoading(true)
    solveMath(expression)
        .catch(error => {
            console.error(error);
            resultDiv.innerText = `Error: ${error}`
        })
        .finally(() => setLoading(false));
})

function setLoading(value) {
    loading = value;
    if (loading) {
        submitButton.classList.add('loading');
    } else {
        submitButton.classList.remove('loading');
    }
}

async function solveMath(expression) {
    // console.log(e)
    // e.preventDefault();
    // TODO: 3 * x / x
    // TODO:ПОЧЕМУ ТО НЕ СЧИТАЕТСЯ КОРЕНЬ X = 0 
    // TODO: x + y + z + 4*z
    // cкладывать числа
    // graph генерировать точки и для более 2х переменных


    // Проверка на пустое поле ввода


    // Отправка данных на бэкенд

    const controller = new AbortController();

    document.onkeydown = (event) => {
        if (event.key === "Escape" || event.key === "Esc") {
            controller.abort();
        }
    }

    const response = await fetch('/api/solve', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ expression: expression }),
        signal: controller.signal

    })

    const data = await response.json();

    if (data.error) {
        resultDiv.innerText = `Error: ${data.error}`;
    } else {

        const f_letter = data.f_letter ? data.f_letter :  `f(${data.vars.join(', ')})`
        const latexResult = convertToLatex(f_letter + ' = ' + data.result);
        resultDiv.innerHTML = `<strong>Result:</strong> $$${latexResult}$$`;

        // roots.innerText = `${JSON.stringify(data.roots)}`;
        // points.innerText = `Points: ${JSON.stringify(data.points)}`;

        rootsList.innerHTML = '';
        // if (data.roots.length === 0) {
        //     const li = document.createElement('li');
        //     li.innerText = 'No roots found';
        //     rootsList.appendChild(li);
        // }
        // ????????????????????
        data.roots.forEach(root => {
            const roundedRoot = root.map(value => roundRoot(value));
            const li = document.createElement('li');
            li.innerText = `Root: ${roundedRoot.join(', ')}`;
            rootsList.appendChild(li);
        });

        plotGraph(data.points, data.roots, f_letter, data.vars);

        MathJax.Hub.Queue(["Typeset", MathJax.Hub, resultDiv]);
    }

}

function convertToLatex(expression) {
    // expression = expression.replace(/^\((.*)\)$/, '$1'); // удаляем скобки по бокам
    // expression = expression.replace(/\(([^\s]+)\)/g, '$1');
    expression = expression.replace(/([0-9]+)\.0/g, '$1');
    // expression = expression.replace(/\(([^\+\-]+)\)/g, '$1');
    expression = expression.replace(/\*/g, '');
    return expression;
}
function roundRoot(value, eps = 1e-5) {
    return Math.abs(value - Math.round(value)) < eps ? Math.round(value) : value
}

function plotGraph(points, roots, f_letter, vars) {
    f_letter = f_letter ? f_letter : vars[0]

    const graph = document.getElementById('graph');
    const dimension = 1 +  vars?.length ?? 0;
    console.log(dimension, vars)

    const axis = Array.from(Array(dimension).keys()).map(i => points.map(point => point[i]))


    if (dimension == 2) {
        const trace = {
            x: axis[0],
            y: axis[1],
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
    } else if (dimension === 3) {
        const trace = {
            x: axis[0],
            y: axis[1],
            z: axis[2],
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