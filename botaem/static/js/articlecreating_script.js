function submitForms() {
    console.log('Кнопка кликнута !')
    const articleForm = document.getElementById('article_form');
    const articleParamsForm = document.getElementById('aricle_params_form');
    const validationErrors = document.getElementById('validation_errors');
    
    const formData = new FormData(articleForm);
    const paramsFormData = new FormData(articleParamsForm);

    for (const pair of paramsFormData.entries()){
        formData.append(pair[0], pair[1]);
    }
    fetch ('/articles/create/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
    .then(response => response.json())
    .then(data =>{
        console.log(data);
        if (data.errors) {
            constErrorsList =
            console.log(data.errors);
            Object.keys(data.errors).forEach(form => {
                Object.keys(data.errors[form]).forEach(field => {
                    validationErrors.insertAdjacentHTML('beforeend', `<li>${data.errors[form][field]}</li>`)
                })
            })
            validationErrors.style = 'display: block';
        }
        if (data.slug) {
            window.location.href = '/article/' + data.slug;
        }
    })
    .catch(error => console.log(error));
}
document.getElementById('submit_send').addEventListener('click', submitForms);