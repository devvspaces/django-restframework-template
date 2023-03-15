from django.contrib import admin, messages

from .models import ProjectApiKey


class ProjectApiKeyAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "pub_key",
    )
    search_fields = ("user", "pub_key")

    def save_model(self, request, obj: ProjectApiKey, *args, **kwargs):
        created = not obj.pk

        if created:
            obj.save()

            # Get the cached pass_key
            key = obj.get_cached_pass_key()

            message = (
                "The API Secret key for {} is: {} ".format(obj.user, key) +
                "Please store it somewhere safe: " +
                "you will not be able to see it again."
            )
            messages.add_message(request, messages.WARNING, message)


admin.site.register(ProjectApiKey, ProjectApiKeyAdmin)
