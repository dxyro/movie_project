from django.contrib import admin
from movie_app.models import *

# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Movie, AuthorAdmin)
admin.site.register(MovieActor, AuthorAdmin)
admin.site.register(MovieRate, AuthorAdmin)
admin.site.register(MovieDirector, AuthorAdmin)
admin.site.register(Country, AuthorAdmin)
admin.site.register(Genre, AuthorAdmin)
