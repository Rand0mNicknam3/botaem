function followProfile() {
  const button = document.getElementById('follow-button');
  const url = '/follower/follow/';

  button.addEventListener('click', (e) => {
    console.log(`Кнопка подписки кликнута пользователем ${followerUsername} в профиле ${profileSlug}`);
    const formData = new FormData();
    formData.append('followed', profileSlug);
    formData.append('follower', followerUsername);
    const csrftoken = csrfToken;
    formData.append('csrfmiddlewaretoken', csrftoken);

    const request = new XMLHttpRequest();
    console.error(formData);
    request.open('POST', url, true);
    request.onload = function() {
      if (request.status === 200) {
        const response = JSON.parse(request.responseText);
        if (response.status === 'success' && response.redirectUrl) {
          console.log(`Успешно подписали пользователя ${followerUsername} на профиль ${profileSlug}`);
        }
        else{
          console.error(`Ошибка с данными при попытке подписки пользователя ${followerUsername} на профиль ${profileSlug}`);
          window.location.href = response.redirectUrl;
        }
      } else {
        console.error(`Ошибка подписки пользователя ${followerUsername} на профиль ${profileSlug}`);
        const response = JSON.parse(request.responseText);
        window.location.href = response.redirectUrl;
      }
    }
    request.send(formData);
  });
}

function unfollowProfile() {
  const button = document.getElementById('unfollow-button');
  const url = '/follower/unfollow/';

  button.addEventListener('click', (e) => {
    console.log(`Кнопка отписки кликнута пользователем ${followerUsername} в профиле ${profileSlug}`);
    const formData = new FormData();
    formData.append('unfollowed', profileSlug);
    formData.append('unfollower', followerUsername);
    const csrftoken = csrfToken;
    formData.append('csrfmiddlewaretoken', csrftoken);

    const request = new XMLHttpRequest();
    console.error(formData);
    request.open('POST', url, true);
    request.onload = function() {
      if (request.status === 200) {
        console.log('Ответ от сервера:', request.responseText);
        const response = JSON.parse(request.responseText);
        if (response.status === 'success' && response.redirectUrl) {
          console.log(`Успешно отписали пользователя ${followerUsername} от профиля ${profileSlug}`);
        }
        else{
          console.error(`Ошибка с данными при попытке отписки пользователя ${followerUsername} от профиля ${profileSlug}`);
          window.location.href = response.redirectUrl;
        }
      } else {
        console.error(`Ошибка отписки пользователя ${followerUsername} от профиля ${profileSlug}`);
        const response = JSON.parse(request.responseText);
        window.location.href = response.redirectUrl;
      }
    }
    request.send(formData);
  });
}

const followButton = document.getElementById('follow-button');
const unfollowButton = document.getElementById('unfollow-button');
const followersAmount = document.getElementById('followers_amount');

function toggleFollowButton() {
  if (followButton.style.display === 'block') {
    followersAmount.innerHTML = parseInt(followersAmount.innerHTML) + 1;
    followButton.style.display = 'none';
    unfollowButton.style.display = 'block';
  } else {
    followersAmount.innerHTML = parseInt(followersAmount.innerHTML) - 1;
    followButton.style.display = 'block';
    unfollowButton.style.display = 'none';
  }
}

followButton.addEventListener('click', toggleFollowButton);
unfollowButton.addEventListener('click', toggleFollowButton);

document.addEventListener('DOMContentLoaded', function() {
  followProfile();
  unfollowProfile();
});