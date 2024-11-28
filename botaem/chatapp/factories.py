from chatapp.models import GroupMessage


class GroupMessageFactory:

    @staticmethod
    def create(group, author, body=None, file=None):
        return GroupMessage.objects.create(group=group, author=author, body=body, file=file)