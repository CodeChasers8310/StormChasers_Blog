from django.contrib import admin
from .models import top_post, response_post, tags, image, alerts, user_alerts, Profile

admin.site.register(top_post)
admin.site.register(response_post)
admin.site.register(tags)
admin.site.register(image)
admin.site.register(alerts)
admin.site.register(user_alerts)
admin.site.register(Profile)
