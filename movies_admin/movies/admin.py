from django.contrib import admin
from .models import Media, Genre, Person, PersonMedia, GenreMedia


class GenreMediaInline(admin.TabularInline):
    model = GenreMedia
    extra = 0


class PersonMediaInline(admin.TabularInline):
    model = PersonMedia
    extra = 0


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    # отображение полей в списке
    list_display = ("title", "creation_date", "rating")

    # порядок следования полей в форме создания/редактирования
    fields = ("title", "description", "creation_date", "certificate",
              "rating", "file_path", "type", "indexed")
    search_fields = ("title",)
    inlines = [GenreMediaInline, PersonMediaInline]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    search_fields = ("first_name", "last_name")
