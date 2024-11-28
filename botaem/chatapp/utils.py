from asgiref.sync import sync_to_async
from django.template.loader import render_to_string

async def get_html_for_online_users(online_users):
    context = {
        'online_users': online_users
    }
    html = await sync_to_async(render_to_string)("chatapp/users_gen.html", context=context)
    return html