import logging
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from chatapp.models import ChatGroup
from chatapp.forms import ChatmessageCreateForm

logger = logging.getLogger(__name__)

@login_required
def chat_view(request, chatroom_name='base'):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    chat_messages = chat_group.chat_messages.all()[:25]
    form = ChatmessageCreateForm()
    return render(request, 'chatapp/main_page.html', {
        'chat_group': chat_group,
        'chat_messages': chat_messages,
        'form': form
    })