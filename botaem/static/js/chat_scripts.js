function scrollToBottom(time=0) {
    setTimeout(function() {
        const container = document.getElementById('chat_container');
        container.scrollTop = container.scrollHeight;
    }, time);
}
let url = `ws://${window.location.host}/ws/chatroom/${chatGroupName}`;
                
const chatSocket = new WebSocket(url)

chatSocket.onopen = function(e){
    e.preventDefault()
    console.log('connected to websocket :)')
    chatSocket.send(JSON.stringify({
        'type': 'online_users'
    }))
}

chatSocket.onmessage = function (e){
    let data = JSON.parse(e.data)
    console.log('Data:', data)
    
    if(data.type === 'message_to_show'){
        console.log(data.message)
        let messages = document.getElementById('chat_container')
        messages.insertAdjacentHTML('beforeend',`${data.message}`)
        console.log('after instertion in chat!')
    }
    if(data.type === 'online_users'){
        let users = document.getElementById('online_users')
        users.innerHTML = ''
        console.log(`users html after 'reset': ${users.innerHTML}`)
        users.insertAdjacentHTML('beforeend',`${data.users}`)
        console.log(`users html after 'insert': ${users.innerHTML}`)
    }
}

let form = document.getElementById('form')
form.addEventListener('submit', (e)=> {
    e.preventDefault()
    let message = e.target.body.value
    chatSocket.send(JSON.stringify({
        'message': message,
        'type': 'chat_message'
}))
    form.reset()
})
scrollToBottom()