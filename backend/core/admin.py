from django.contrib import admin

from .models import (
    Banner,
    BehaviorRecord,
    CourseMaterial,
    EducationNews,
    ForumPost,
    NewsComment,
    Notice,
    OnlineVideo,
    Order,
    StudentUser,
    TeacherUser,
    User,
)


admin.site.register(User)
admin.site.register(StudentUser)
admin.site.register(TeacherUser)
admin.site.register(CourseMaterial)
admin.site.register(OnlineVideo)
admin.site.register(ForumPost)
admin.site.register(EducationNews)
admin.site.register(NewsComment)
admin.site.register(Notice)
admin.site.register(Banner)
admin.site.register(Order)
admin.site.register(BehaviorRecord)
