from django.contrib import admin

# Register your models here.
from .models import Tag, Trade, Execution

admin.site.register(Tag)
admin.site.register(Trade)
admin.site.register(Execution)
