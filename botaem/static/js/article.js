function readLater() {
    const readLater = document.getElementById('read_later')
    const url = `/articles/article_read_later/${articleSlug}`;
    const notification = document.getElementById('notification');
    const notificationMessage = document.getElementById('notification-message');
    readLater.addEventListener('click', (e) => {
        console.log('Click read later button!');
        const csrftoken = csrfToken
        const request = new XMLHttpRequest();
        request.open('GET', url, true);
        request.setRequestHeader('X-CSRFToken', csrftoken);
        request.onload = function() {
            if (request.status === 200) {
                const responseData = JSON.parse(request.responseText);
                console.log('Article added to read later!');
                if (responseData.status === 'success') {
                    notification.style.display = 'block';
                    notificationMessage.innerText = responseData.message;
                    setTimeout(() => {
                        notification.style.display = 'none';
                    }, 4000);
                }
            } else {
                console.error('Error adding article to read later!');
                notification.style.display = 'block';
                notificationMessage.innerText = 'Error adding article to read later!';
                setTimeout(() => {
                    notification.style.display = 'none';
                }, 4000);
            }
        };
        request.send();
    })
}
function likeArticle() {
    const likeButton = document.getElementById('like-button');
    const url = `/articles/article_like/${articleSlug}`;
    const notification = document.getElementById('notification');
    const notificationMessage = document.getElementById('notification-message');
    likeButton.addEventListener('click', (e) => {
        console.log('Click like button!');
        const csrftoken = csrfToken
        const request = new XMLHttpRequest();
        request.open('GET', url, true);
        request.setRequestHeader('X-CSRFToken', csrftoken);
        request.onload = function() {
            if (request.status === 200) {
                const responseData = JSON.parse(request.responseText);
                console.log('Article liked/unliked successfully!');
                if (responseData.status === 'success') {
                    notification.style.display = 'block';
                    notificationMessage.innerText = responseData.message;
                    if (responseData.message === 'Article unliked') {
                        const likesAmount = document.getElementById('likes_amount');
                        const currentLikes = parseInt(likesAmount.innerText);
                        likesAmount.innerText = (currentLikes - 1).toString();
                    }
                    if (responseData.message === 'Article liked') {
                        const likesAmount = document.getElementById('likes_amount');
                        const currentLikes = parseInt(likesAmount.innerText);
                        likesAmount.innerText = (currentLikes + 1).toString();
                    }
                    setTimeout(() => {
                        notification.style.display = 'none';
                    }, 4000);
                }
            } else {
                console.error('Error liking article!');
                notification.style.display = 'block';
                notificationMessage.innerText = 'Error liking article!';
                setTimeout(() => {
                    notification.style.display = 'none';
                }, 4000);
            }
        };
        request.send();
    })
}

document.addEventListener('DOMContentLoaded', function() {
    readLater();
    likeArticle();
  });