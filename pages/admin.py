from django.contrib import admin
from .models import Question, Region, Accommodations ,Comment, Question, Image_table

admin.site.register(Region)
admin.site.register(Accommodations)
admin.site.register(Comment)
admin.site.register(Question)
admin.site.register(Image_table)
