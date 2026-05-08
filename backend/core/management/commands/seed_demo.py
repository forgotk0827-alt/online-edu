import hashlib
import os
from html import escape

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import (
    Banner,
    CourseMaterial,
    EducationNews,
    ForumPost,
    Notice,
    OnlineVideo,
    Order,
    StudentUser,
    TeacherUser,
)


def image(text, bg="B377B3"):
    filename = hashlib.md5(f"{bg}-{text}".encode("utf-8")).hexdigest()[:12] + ".svg"
    folder = settings.MEDIA_ROOT / "placeholders"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / filename
    if not path.exists():
        color = bg if bg.startswith("#") else f"#{bg}"
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="640" height="360" viewBox="0 0 640 360">
  <rect width="640" height="360" rx="18" fill="{escape(color)}"/>
  <text x="320" y="195" text-anchor="middle" font-size="54" fill="#ffffff"
        font-family="Microsoft YaHei, PingFang SC, Noto Sans CJK SC, SimHei, sans-serif">{escape(text)}</text>
</svg>
"""
        path.write_text(svg, encoding="utf-8")
    media_base = os.getenv("MEDIA_BASE_URL", "http://127.0.0.1:8000/media").rstrip("/")
    return f"{media_base}/placeholders/{filename}"


class Command(BaseCommand):
    help = "Refresh the database with Chinese K12 demo data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--keep-users",
            action="store_true",
            help="Keep existing non-demo users. Demo users are still updated.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()

        admin, _ = User.objects.update_or_create(
            username="admin",
            defaults={
                "password": make_password("admin123"),
                "nickname": "系统管理员",
                "email": "admin@example.com",
                "role": "admin",
                "status": "正常",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        teacher, _ = User.objects.update_or_create(
            username="teacher",
            defaults={
                "password": make_password("teacher123"),
                "nickname": "陈老师",
                "email": "teacher@example.com",
                "role": "teacher",
                "status": "正常",
            },
        )
        student, _ = User.objects.update_or_create(
            username="student",
            defaults={
                "password": make_password("student123"),
                "nickname": "林同学",
                "email": "student@example.com",
                "role": "student",
                "status": "正常",
            },
        )

        StudentUser.objects.update_or_create(
            user=student,
            defaults={
                "student_name": "林同学",
                "student_gender": "女",
                "student_id": 20260001,
                "examine_state": "已通过",
            },
        )
        TeacherUser.objects.update_or_create(
            user=teacher,
            defaults={
                "teachers_name": "陈老师",
                "teaching_subjects": "小学数学",
                "teacher_id": 1001001,
                "examine_state": "已通过",
            },
        )

        Banner.objects.all().delete()
        CourseMaterial.objects.all().delete()
        OnlineVideo.objects.all().delete()
        ForumPost.objects.all().delete()
        EducationNews.objects.all().delete()
        Notice.objects.all().delete()

        Banner.objects.bulk_create(
            [
                Banner(title="中小学在线学习平台", image=image("中小学在线学习平台", "23372f"), link="/", sort=1),
                Banner(title="课程资料精选推荐", image=image("课程资料精选推荐", "993380"), link="/courses", sort=2),
                Banner(title="学习交流与教育资讯", image=image("学习交流与教育资讯", "B377B3"), link="/forum", sort=3),
            ]
        )

        courses = CourseMaterial.objects.bulk_create(
            [
                CourseMaterial(
                    course_number="K12-MATH-001",
                    teacher_users=teacher.id,
                    teachers_name="陈老师",
                    teaching_semester="2026 春季",
                    course_name="六年级数学应用题专项",
                    teaching_type="小学数学",
                    course_prices=29.9,
                    course_highlights="行程、工程、分数应用题集中训练",
                    course_images=image("小学数学"),
                    course_introduction="面向六年级学生，梳理常见应用题模型，配套例题讲解与练习。",
                    hits=230,
                    praise_len=28,
                    collect_len=16,
                ),
                CourseMaterial(
                    course_number="K12-CHN-002",
                    teacher_users=teacher.id,
                    teachers_name="王老师",
                    teaching_semester="2026 春季",
                    course_name="小学语文阅读理解提升",
                    teaching_type="小学语文",
                    course_prices=19.9,
                    course_highlights="阅读方法、答题模板、作文素材",
                    course_images=image("小学语文", "993380"),
                    course_introduction="围绕记叙文、说明文阅读题，训练审题、定位和归纳能力。",
                    hits=188,
                    praise_len=22,
                    collect_len=13,
                ),
                CourseMaterial(
                    course_number="K12-ENG-003",
                    teacher_users=teacher.id,
                    teachers_name="刘老师",
                    teaching_semester="2026 春季",
                    course_name="初一英语词汇与语法精讲",
                    teaching_type="初中英语",
                    course_prices=24.9,
                    course_highlights="高频词汇、核心句型、听说训练",
                    course_images=image("初中英语"),
                    course_introduction="覆盖初一英语重点词汇、时态和句型，适合课后巩固。",
                    hits=318,
                    praise_len=39,
                    collect_len=24,
                ),
                CourseMaterial(
                    course_number="K12-PHY-004",
                    teacher_users=teacher.id,
                    teachers_name="赵老师",
                    teaching_semester="2026 秋季",
                    course_name="初二物理力学基础",
                    teaching_type="初中物理",
                    course_prices=34.9,
                    course_highlights="力与运动、实验分析、错题讲评",
                    course_images=image("初中物理", "993380"),
                    course_introduction="通过实验现象和例题讲解理解力学基础概念。",
                    hits=410,
                    praise_len=45,
                    collect_len=30,
                ),
                CourseMaterial(
                    course_number="K12-CHE-005",
                    teacher_users=teacher.id,
                    teachers_name="孙老师",
                    teaching_semester="2026 秋季",
                    course_name="初三化学基础知识梳理",
                    teaching_type="初中化学",
                    course_prices=39.9,
                    course_highlights="元素化合物、实验题、计算题",
                    course_images=image("初中化学"),
                    course_introduction="系统整理初三化学核心知识点，配合阶段测试题。",
                    hits=276,
                    praise_len=31,
                    collect_len=20,
                ),
                CourseMaterial(
                    course_number="K12-HIS-006",
                    teacher_users=teacher.id,
                    teachers_name="周老师",
                    teaching_semester="2026 春季",
                    course_name="中考历史专题复习",
                    teaching_type="初中历史",
                    course_prices=30,
                    course_highlights="时间轴、材料题、专题归纳",
                    course_images=image("初中历史", "993380"),
                    course_introduction="按专题归纳中考历史高频考点，帮助学生形成知识框架。",
                    hits=198,
                    praise_len=18,
                    collect_len=14,
                ),
            ]
        )

        OnlineVideo.objects.bulk_create(
            [
                OnlineVideo(teacher_users=teacher.id, teachers_name="陈老师", video_name="小升初数学错题讲解", video_duration="18:20", video_origin="本校录制", video_type="小学数学", video_content="分数应用题和行程问题错题精讲。", video_poster=image("数学视频", "993380"), hits=230, praise_len=28, collect_len=15),
                OnlineVideo(teacher_users=teacher.id, teachers_name="王老师", video_name="记叙文阅读答题步骤", video_duration="20:10", video_origin="平台课程", video_type="小学语文", video_content="从审题、找关键词到组织答案完整演示。", video_poster=image("语文阅读"), hits=168, praise_len=19, collect_len=12),
                OnlineVideo(teacher_users=teacher.id, teachers_name="刘老师", video_name="初一英语自然拼读复习", video_duration="22:10", video_origin="平台课程", video_type="初中英语", video_content="自然拼读规律与常见单词记忆方法。", video_poster=image("英语视频", "993380"), hits=318, praise_len=39, collect_len=22),
                OnlineVideo(teacher_users=teacher.id, teachers_name="赵老师", video_name="初二物理力与运动", video_duration="25:45", video_origin="平台课程", video_type="初中物理", video_content="结合实验理解力、速度和运动状态变化。", video_poster=image("物理视频"), hits=410, praise_len=45, collect_len=27),
            ]
        )

        ForumPost.objects.bulk_create(
            [
                ForumPost(user_id=student.id, nickname="林同学", title="六年级数学应用题解题方法交流", description="分享行程、工程、浓度问题的常用思路。", tag="数学", img=image("学习交流"), type="学习经验", hits=230, praise_len=28),
                ForumPost(user_id=teacher.id, nickname="陈老师", title="中考数学压轴题资料整理", description="整理近期练习中的典型压轴题，欢迎同学补充。", tag="中考", img=image("中考数学", "993380"), type="课程讨论", hits=488, praise_len=52, istop=1),
                ForumPost(user_id=student.id, nickname="林同学", title="初一英语单词记忆打卡小组", description="每天十分钟，互相监督单词记忆。", tag="英语", img=image("英语打卡"), type="学习经验", hits=318, praise_len=39),
                ForumPost(user_id=student.id, nickname="赵同学", title="初二物理浮力实验现象讨论", description="记录实验过程中的现象和疑问，讨论如何画受力分析图。", tag="物理", img=image("物理实验", "993380"), type="问题求助", hits=410, praise_len=45),
            ]
        )

        EducationNews.objects.bulk_create(
            [
                EducationNews(title="义务教育阶段数字课堂建设持续推进", category="政策", tag="教育信息化", cover_image=image("教育新闻"), summary="多地推动数字课堂常态化应用。", content="各地中小学持续推进数字课堂建设，优化课堂互动和课后服务，帮助学生获得更加稳定的线上学习体验。", author="平台编辑", publish_state="已发布", hits=302, praise_len=12),
                EducationNews(title="多地中小学开展课后服务质量提升行动", category="校园", tag="课后服务", cover_image=image("校园动态", "993380"), summary="课后服务内容更加丰富。", content="学校通过社团活动、作业答疑和兴趣课程提升课后服务质量，满足学生个性化学习需求。", author="平台编辑", publish_state="已发布", hits=420, praise_len=22),
                EducationNews(title="小学科学实验课程资源包上线", category="小学", tag="科学实验", cover_image=image("科学实验"), summary="实验课程资源覆盖常见课堂主题。", content="资源包提供实验步骤、观察记录和安全提示，方便教师组织课堂演示与学生课后复习。", author="平台编辑", publish_state="已发布", hits=156, praise_len=9),
                EducationNews(title="初中教师信息化教学能力培训启动", category="教师", tag="教师培训", cover_image=image("教师培训", "993380"), summary="提升教师数字化教学设计能力。", content="培训围绕线上课堂组织、数据化学情分析和互动教学工具使用展开。", author="平台编辑", publish_state="已发布", hits=377, praise_len=31),
                EducationNews(title="AI 学习助手进入中小学个性化辅导场景", category="科技", tag="AI学习", cover_image=image("AI学习助手"), summary="智能推荐帮助学生查漏补缺。", content="AI 学习助手根据学生学习记录提供个性化练习建议，并为教师提供班级薄弱点分析。", author="平台编辑", publish_state="已发布", hits=520, praise_len=44),
            ]
        )

        Notice.objects.bulk_create(
            [
                Notice(title="小学数学思维训练课程资料更新通知", category="课程", content="小学数学思维训练资料已更新，请已购买的学生在个人中心查看最新资料。", publish_state="已发布"),
                Notice(title="期中复习专题直播安排公告", category="教学", content="本周期中复习专题直播将按年级分场进行，请学生提前进入在线视频模块查看安排。", publish_state="已发布"),
                Notice(title="家长端学习报告查看功能维护通知", category="系统", content="家长端学习报告功能将于今晚 22:00 至 23:00 维护，期间可能无法查看报告。", publish_state="已发布"),
                Notice(title="在线学习交流文明公约", category="交流", content="请同学们文明发帖、理性讨论，共同维护良好的学习交流氛围。", publish_state="已发布"),
            ]
        )

        courses_by_number = {
            item.course_number: item
            for item in CourseMaterial.objects.filter(
                course_number__in=["K12-MATH-001", "K12-ENG-003"]
            )
        }
        math_course = courses_by_number.get("K12-MATH-001")
        english_course = courses_by_number.get("K12-ENG-003")

        if math_course:
            Order.objects.update_or_create(
                user=student,
                course=math_course,
                defaults={"amount": math_course.course_prices, "pay_state": "已支付"},
            )
        if english_course:
            Order.objects.update_or_create(
                user=student,
                course=english_course,
                defaults={"amount": english_course.course_prices, "pay_state": "已支付"},
            )

        self.stdout.write(self.style.SUCCESS("中文演示数据已刷新到当前数据库。"))
