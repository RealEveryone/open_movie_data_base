from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model

from open_movie_data_base.movie.forms import AddMovieForm
from open_movie_data_base.user.forms import AppUserForm
from open_movie_data_base.user.models import Actor, MovieDirector, RegularUser

UserModel = get_user_model()


@admin.register(UserModel)
class AdminUser(auth_admin.UserAdmin):
    add_form = AppUserForm
    list_display = ['username', 'email', 'date_joined']
    readonly_fields = ('date_joined', 'last_login')
    list_filter = ()
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("email",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        ('User Type', {'fields': ('type_of_user',)})
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", 'email', "password1", "password2", 'type_of_user'),
            },
        ),
    )

#
# @admin.register(Actor)
# class ActorAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(MovieDirector)
# class MovieDirectorAdmin(admin.ModelAdmin):
#     pass
#
#
# @admin.register(RegularUser)
# class AdminRegularUser(admin.ModelAdmin):
#     pass
