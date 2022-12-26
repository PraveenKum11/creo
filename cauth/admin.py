from django.contrib import admin
from cauth import models

# Register your models here.
admin.site.register([
    models.Profile,
])