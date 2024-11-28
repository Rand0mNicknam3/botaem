import logging
from django.apps import AppConfig
from django.apps import apps
from django.dispatch import receiver
from django.db.models.signals import post_migrate


logger = logging.getLogger(__name__)


@receiver(post_migrate, sender=AppConfig)
def create_start_data_chat(sender, **kwargs):
    from initial_data import start_groupchat
    GroupChat = apps.get_model('chatapp', 'ChatGroup')
    if not GroupChat.objects.filter(group_name='base').exists():
        GroupChat.objects.create(**start_groupchat)
        logger.info("GroupChat created", extra={'group_name': start_groupchat['group_name']})
    else:
        logger.info("GroupChat already exists")


class ChatappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chatapp'

    def ready(self):
        post_migrate.connect(create_start_data_chat, sender=self)
