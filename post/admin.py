from django.contrib import admin
import models


class PostModelAdmin(admin.ModelAdmin):
	list_display = ["id", "title", "num_view"]
	search_fields = ["id", "title"]


class TagModelAdmin(admin.ModelAdmin):
	list_display = ["id", "name"]
	search_fields = ["id", "name"]
	filter_horizontal = ["linked_posts"]


admin.site.register(models.Post, PostModelAdmin)
admin.site.register(models.Tag, TagModelAdmin)