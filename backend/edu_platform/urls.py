from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/register/", views.register),
    path("api/auth/login/", views.login),
    path("api/auth/me/", views.me),
    path("api/upload/", views.upload_file),
    path("api/courses/", views.course_list),
    path("api/courses/<int:pk>/", views.course_detail),
    path("api/courses/<int:pk>/buy/", views.buy_course),
    path("api/videos/", views.video_list),
    path("api/videos/<int:pk>/", views.video_detail),
    path("api/forums/", views.forum_list),
    path("api/forums/<int:pk>/", views.forum_detail),
    path("api/news/", views.news_list),
    path("api/news/<int:pk>/", views.news_detail),
    path("api/news/<int:pk>/comments/", views.news_comments),
    path("api/notices/", views.notice_list),
    path("api/banners/", views.banner_list),
    path("api/admin/banners/", views.banner_manage),
    path("api/interactions/", views.interaction_list),
    path("api/comments/", views.comment_list),
    path("api/recommendations/courses/", views.recommend_courses),
    path("api/admin/users/", views.admin_users),
    path("api/admin/statistics/", views.admin_statistics),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
