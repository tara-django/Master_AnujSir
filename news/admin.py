from django.contrib import admin
from news.models import News, Category

# Register your models here.


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    # readonly_fields = ("author",)


admin.site.register(Category)

