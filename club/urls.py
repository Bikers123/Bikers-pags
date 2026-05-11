from django.urls import path

from . import views

urlpatterns = [
    path("", views.info_view, name="info"),
    path("auth/login/", views.login_view, name="login"),
    path("auth/register/", views.register_view, name="register"),
    path("auth/logout/", views.logout_view, name="logout"),
    path("feed/", views.feed, name="feed"),
    path("posts/create/", views.post_create, name="post_create"),
    path("posts/<int:post_id>/delete/", views.post_delete, name="post_delete"),
    path("posts/<int:post_id>/comment/", views.post_comment, name="post_comment"),
    path("riders/", views.riders, name="riders"),
    path("riders/<str:username>/", views.rider_detail, name="rider_detail"),
    path("me/edit/", views.me_edit, name="me_edit"),
    # Panel de administración
    path("panel/", views.admin_panel, name="admin_panel"),
    path("panel/create-user/", views.admin_create_user, name="admin_create_user"),
    path("panel/toggle-active/", views.admin_toggle_active, name="admin_toggle_active"),
    path("panel/delete-user/<int:user_id>/", views.admin_delete_user, name="admin_delete_user"),
    # API
    path("api/search/", views.api_search, name="api_search"),
    path("api/friends/request/", views.api_friend_request, name="api_friend_request"),
    path("api/friends/accept/", views.api_friend_accept, name="api_friend_accept"),
    path("api/friends/updates/", views.api_friend_updates, name="api_friend_updates"),
    path("api/friends/incoming/", views.api_friend_incoming, name="api_friend_incoming"),
    path("api/notifications/check/", views.api_notifications_check, name="api_notifications_check"),
]
