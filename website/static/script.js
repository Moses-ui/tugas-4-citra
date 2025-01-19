const classifyBtn = document.getElementById('classifyBtn');
classifyBtn.addEventListener('click', () => {
    const image = get_image();
    if (!image) {
        return;
    }
    display_image(image);
    send_image(image, display_result);
})

function send_image(image, callback) {
    const url = classifyBtn.dataset.apiUrl;

    let formData = new FormData();
    formData.append('image', image);

    fetch(url, {
        method: 'POST',
        // headers: { 'Content-Type': 'application/json' },
        body: formData,
    })
    .then(response => response.json())
    .then(data => callback(data['prediction_default'], data['prediction_pretrained']))
    .catch(error => console.log(error));
}

function display_result(result_default, result_pretrained) {
    document.getElementById('classResultDefault').innerText = `default result: ${result_default}`;
    document.getElementById('classResultPretrained').innerText = `pretrained result: ${result_pretrained}`;
}

function toggle_visibility() {
    document.getElementById('userImg').style.visibility = 'visible';
}

function display_image(image) {
    toggle_visibility();
    let reader = new FileReader();
    reader.onload = (e) => {
        document.getElementById('userImg').src = e.target.result;
    }
    reader.readAsDataURL(image);
}

function get_image() {
    return document.getElementById('file').files[0];
}

