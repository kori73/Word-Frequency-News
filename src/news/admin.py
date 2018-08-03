from django.contrib import admin

from .models import Headline, UserProfile, WordAndCount

admin.site.register(Headline)
admin.site.register(UserProfile)
admin.site.register(WordAndCount)
