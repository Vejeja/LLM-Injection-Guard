async function submitForm(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const response = await fetch('/submit', {
        method: 'POST',
        body: formData
    });

    const resultList = document.getElementById('chat');
    const newElement = document.createElement('div');
    const message = document.getElementById('input_field').value
    newElement.classList.add('d-flex', 'flex-row-reverse', 'p-3');
    newElement.innerHTML = `
        <img src="https://img.icons8.com/color/48/000000/circled-user-male-skin-type-7.png" width="30" height="30">
        <div class="bg-white mr-2 p-3"><span class="text-muted">${message}</span></div>
    `;
    resultList.appendChild(newElement);
    newElement.scrollIntoView({behavior: 'smooth'})
    document.getElementById('input_field').value = "";

    const result = await response.json();

    if (result.task_id) {
        await checkResult(result.task_id);
    }
}

async function checkResult(task_id) {
    const response = await fetch(`/result/${task_id}`);
    const result = await response.json();

    if (result.status === "completed") {
        const resultList = document.getElementById('chat');
        const newElement = document.createElement('div');
        newElement.classList.add('d-flex', 'flex-row', 'p-3');
        newElement.innerHTML = `
            <img src="https://img.icons8.com/color/48/000000/circled-user-female-skin-type-7.png" width="30" height="30">
            <div class="chat ml-2 p-3">${result.result.output_field}</div>
        `;
        resultList.appendChild(newElement);
        newElement.scrollIntoView({behavior: 'smooth'})
    } else if (result.status === "processing") {
        setTimeout(() => checkResult(task_id), 1000);
    }
}
