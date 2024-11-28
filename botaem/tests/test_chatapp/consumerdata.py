async def get_headers_and_scope(instance, user):
    headers = [(b'origin', b'...'), (b'cookie', instance.client.cookies.output(header='', sep='; ').encode())]
    scope = {
        'type': 'websocket',
        'path': '/ws/chatroom/based_chat',
        'raw_path': b'/ws/chatroom/based_chat',
        'root_path': '',
        'headers': headers,
        'query_string': b'',
        'client': ['127.0.0.1', 63294],
        'server': ['127.0.0.1', 8000],
        'subprotocols': [],
        'asgi': {'version': '3.0'},
        'cookies': {'csrftoken': 'DdxSVjFW3vyaDixl6auICWpGijJU6SIv', 'sessionid': 'enrcif9mxwdrd9euizapw7ssy2y0l1u3'},
        'session': {},
        'user': user,
        'path_remaining': '',
        'url_route': {'args': (), 'kwargs': {'chatroom_name': 'based_chat'}}
    }
    return headers, scope


async def make_communicator_scope(communicator, scope):
    for key, value in scope.items():
        communicator.scope[key] = value
    return communicator