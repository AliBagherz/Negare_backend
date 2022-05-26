from core.models import Content


def add_new_content(file):
    content = Content(file=file)
    content.save()
    return content.id
