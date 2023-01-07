from main import models

def tags_processor(request):
    tags = models.Tag.objects.all().distinct()
    return {"tags" : tags}