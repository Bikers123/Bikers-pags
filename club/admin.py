from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import EmergencyContact, Friendship, Post, PostImage, RiderProfile, Trip, TripImage, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("Tipo", {"fields": ("user_type",)}),)
    list_display = ("username", "email", "first_name", "last_name", "user_type", "is_staff")


@admin.register(RiderProfile)
class RiderProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "document_id", "sex", "age", "blood_type", "updated_at")
    search_fields = ("user__username", "user__first_name", "user__last_name", "document_id")


admin.site.register(EmergencyContact)
admin.site.register(Friendship)
admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(Trip)
admin.site.register(TripImage)
