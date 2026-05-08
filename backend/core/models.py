import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ("student", "学生"),
        ("teacher", "教师"),
        ("admin", "管理员"),
    )
    nickname = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")
    avatar = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=30, default="正常")


class AuthToken(models.Model):
    key = models.CharField(max_length=64, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)


class StudentUser(models.Model):
    student_users_id = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=100)
    student_gender = models.CharField(max_length=20, blank=True)
    student_id = models.FloatField(null=True, blank=True)
    examine_state = models.CharField(max_length=30, default="已通过")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class TeacherUser(models.Model):
    teacher_users_id = models.AutoField(primary_key=True)
    teachers_name = models.CharField(max_length=100)
    teaching_subjects = models.CharField(max_length=100, blank=True)
    teacher_id = models.FloatField(null=True, blank=True)
    examine_state = models.CharField(max_length=30, default="待审核")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class CourseMaterial(models.Model):
    course_materials_id = models.AutoField(primary_key=True)
    course_number = models.CharField(max_length=50, unique=True)
    teacher_users = models.IntegerField(default=0)
    teachers_name = models.CharField(max_length=100)
    teaching_semester = models.CharField(max_length=50, blank=True)
    course_name = models.CharField(max_length=150)
    teaching_type = models.CharField(max_length=80)
    course_prices = models.FloatField(default=0)
    course_highlights = models.CharField(max_length=255, blank=True)
    course_images = models.CharField(max_length=255, blank=True)
    course_introduction = models.TextField(blank=True)
    hits = models.IntegerField(default=0)
    praise_len = models.IntegerField(default=0)
    collect_len = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class OnlineVideo(models.Model):
    online_video_id = models.AutoField(primary_key=True)
    teacher_users = models.IntegerField(default=0)
    teachers_name = models.CharField(max_length=100)
    video_name = models.CharField(max_length=150)
    video_duration = models.CharField(max_length=50, blank=True)
    video_origin = models.CharField(max_length=80, blank=True)
    video_type = models.CharField(max_length=80)
    video_content = models.CharField(max_length=255, blank=True)
    video_poster = models.CharField(max_length=255, blank=True)
    video_url = models.CharField(max_length=500, blank=True)
    hits = models.IntegerField(default=0)
    praise_len = models.IntegerField(default=0)
    collect_len = models.IntegerField(default=0)
    comment_len = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class ForumPost(models.Model):
    forum_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    nickname = models.CharField(max_length=100)
    praise_len = models.IntegerField(default=0)
    hits = models.IntegerField(default=0)
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=150, blank=True)
    description = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=255, blank=True)
    tag = models.CharField(max_length=80, blank=True)
    img = models.TextField(blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    avatar = models.CharField(max_length=255, blank=True)
    type = models.CharField(max_length=80, blank=True)
    istop = models.IntegerField(default=0)


class EducationNews(models.Model):
    news_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=180)
    category = models.CharField(max_length=80, blank=True)
    tag = models.CharField(max_length=100, blank=True)
    cover_image = models.CharField(max_length=255, blank=True)
    summary = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    author = models.CharField(max_length=100, blank=True)
    hits = models.IntegerField(default=0)
    praise_len = models.IntegerField(default=0)
    comment_len = models.IntegerField(default=0)
    publish_state = models.CharField(max_length=30, default="已发布")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class NewsComment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    news = models.ForeignKey(EducationNews, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100)
    avatar = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_type = models.CharField(max_length=30)
    target_id = models.IntegerField()
    target_title = models.CharField(max_length=180, blank=True)
    nickname = models.CharField(max_length=100)
    avatar = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class Notice(models.Model):
    title = models.CharField(max_length=150)
    category = models.CharField(max_length=80, blank=True)
    content = models.TextField()
    publish_state = models.CharField(max_length=30, default="已发布")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class Banner(models.Model):
    title = models.CharField(max_length=120)
    image = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True)
    sort = models.IntegerField(default=0)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseMaterial, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    pay_state = models.CharField(max_length=30, default="已支付")
    create_time = models.DateTimeField(auto_now_add=True)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_type = models.CharField(max_length=30)
    target_id = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_type = models.CharField(max_length=30)
    target_id = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)


class BehaviorRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseMaterial, on_delete=models.CASCADE)
    behavior = models.CharField(max_length=20)
    weight = models.IntegerField(default=1)
    create_time = models.DateTimeField(auto_now_add=True)
