from django.forms import ModelForm
from django import forms
from chatapp.models import ChatGroup, GroupMessage


class ChatmessageCreateForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['body']
        labels = {'body': ''}
        widgets = {
            'body' : forms.TextInput(
                attrs={
                    'placeholder': 'Add message ...',
                    'class': 'form-control input-sm chat_input',
                    'maxlength' : '300',
                    'autofocus': True,
                    }
            ),
        }

     
class NewGroupForm(ModelForm):
    class Meta:
        model = ChatGroup
        fields = ['groupchat_name']
        widgets = {
            'groupchat_name' : forms.TextInput(attrs={
                'placeholder': 'Add name ...', 
                'class': 'p-4 text-black', 
                'maxlength' : '300', 
                'autofocus': True,
                }),
        }
        
        
class ChatRoomEditForm(ModelForm):
    class Meta:
        model = ChatGroup
        fields = ['groupchat_name']
        widgets = {
            'groupchat_name' : forms.TextInput(attrs={
                'class': 'p-4 text-xl font-bold mb-4', 
                'maxlength' : '300', 
                }),
        }
