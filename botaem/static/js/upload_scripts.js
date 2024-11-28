function uploadAvatar() {
  const button = document.getElementById('image-button');
  const fileInput = document.getElementById('image-upload');
  const url = '/myprofile/upload_avatar';

  button.addEventListener('click', (e) => {
    console.log('Кнопка кликнута!');
    fileInput.click();
  });

  fileInput.addEventListener('change', (e) => {
    console.log('Файл выбран!');
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append('image', file);
    const csrftoken = csrfToken;
    formData.append('csrfmiddlewaretoken', csrftoken);

    const request = new XMLHttpRequest();
    request.open('POST', url, true);
    request.onload = function() {
      if (request.status === 200) {
        console.log('Файл загружен успешно!');
        location.reload();
      } else {
        console.error('Ошибка загрузки файла!');
      }
    }
    request.send(formData);
  });
}

function uploadBio() {
  const button = document.getElementById('bio-button');
  const bioForm = document.getElementById('bio-form');
  const url = '/myprofile/upload_bio';

  button.addEventListener('click', (e) => {
    console.log('Кнопка кликнута! био');
    bioForm.style.display = 'block';
  });

  bioForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const text = document.getElementById('bio-input').value;
    const formData = new FormData();
    formData.append('bio', text);
    const csrftoken = csrfToken;
    formData.append('csrfmiddlewaretoken', csrftoken);

    const request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.onload = function() {
      if (request.status === 200) {
        console.log('Био загружен успешно!');
        bioForm.style.display = 'none';
        document.getElementById('bio-profile').innerText = text;
        bioForm.reset();
      } else {
        console.error('Ошибка загрузки био!');
      }
    }
    request.send(formData);
  });
}

function getReferralLink() {
  const url = '/myprofile/get_refcode';
  const button = document.getElementById('ref-button');
  const modal = document.querySelector('.modal');
  const modalBody = document.querySelector('.modal-body');

  button.addEventListener('click', (e) => {
    console.log('Кнопка кликнута! ссылка');
    const request = new XMLHttpRequest();
    const csrftoken = csrfToken;
    request.open('POST', url, true);
    request.setRequestHeader('X-CSRFToken', csrftoken);
    request.onload = function() {
      if (request.status === 200) {
        console.log('Ссылка получена успешно!');
        const responseData = JSON.parse(request.responseText);
        modal.style.display = 'block';
        modalBody.innerText = responseData.refcode;
      } else {
        console.error('Ошибка получения ссылки!');
      }
    }
    request.send();
  });
}

function copyOrCloseModal() {
  const copyButton = document.getElementById('copy_ref_button');
  const modal = document.querySelector('.modal');
  const modalBody = document.querySelector('.modal-body');
  const closeButton = document.getElementById('close_ref_button');

  copyButton.addEventListener('click', (e) => {
    navigator.clipboard.writeText(modalBody.innerText);
    alert('Ссылка скопирована!');
  });

  closeButton.addEventListener('click', (e) => {
    modal.style.display = 'none';
  });
}


document.addEventListener('DOMContentLoaded', function() {
  uploadAvatar();
  uploadBio();
  getReferralLink();
  copyOrCloseModal();
});