from django.contrib import admin
from .models import Question , Visit , KindOfCounseling

admin.site.register(Question)
admin.site.register(Visit)
admin.site.register(KindOfCounseling)