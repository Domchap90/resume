from django.contrib import admin

from .models import Subscriber


class SubscriberAdmin(admin.ModelAdmin):

    list_display = ('id', 'name', 'email', 'number')

    ordering = ('name', 'email')


admin.site.register(Subscriber, SubscriberAdmin)
