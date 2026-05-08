import json
import math
from collections import defaultdict

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from django.core.files.storage import default_storage
from django.db.models import Count, Q, Sum
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import (
    AuthToken,
    Banner,
    BehaviorRecord,
    CourseMaterial,
    EducationNews,
    Comment,
    Favorite,
    ForumPost,
    Like,
    NewsComment,
    Notice,
    OnlineVideo,
    Order,
)

User = get_user_model()


def ok(data=None, message="success"):
    return JsonResponse({"code": 200, "message": message, "data": data or {}}, json_dumps_params={"ensure_ascii": False})


def fail(message, code=400):
    return JsonResponse({"code": code, "message": message, "data": {}}, status=code, json_dumps_params={"ensure_ascii": False})


def body(request):
    if request.body:
        return json.loads(request.body.decode("utf-8"))
    return request.POST.dict()


def item_title(target_type, target_id):
    maps = {
        "course": CourseMaterial.objects.filter(course_materials_id=target_id).first(),
        "video": OnlineVideo.objects.filter(online_video_id=target_id).first(),
        "forum": ForumPost.objects.filter(forum_id=target_id).first(),
        "news": EducationNews.objects.filter(news_id=target_id).first(),
        "notice": Notice.objects.filter(id=target_id).first(),
    }
    target = maps.get(target_type)
    if not target:
        return ""
    return (
        getattr(target, "course_name", "")
        or getattr(target, "video_name", "")
        or getattr(target, "title", "")
        or getattr(target, "description", "")
    )


def serialize(obj, fields):
    data = {}
    for field in fields:
        value = getattr(obj, field)
        if hasattr(value, "strftime"):
            value = value.strftime("%Y-%m-%d %H:%M:%S")
        data[field] = value
    return data


def paginate(request, qs, fields):
    page = max(int(request.GET.get("page", 1)), 1)
    page_size = min(max(int(request.GET.get("page_size", 9)), 1), 100)
    total = qs.count()
    start = (page - 1) * page_size
    items = [serialize(item, fields) for item in qs[start : start + page_size]]
    return {"items": items, "total": total, "page": page, "page_size": page_size}


def current_user(request):
    auth = request.headers.get("Authorization", "")
    key = auth.replace("Token ", "").strip()
    if not key:
        return None
    token = AuthToken.objects.select_related("user").filter(key=key).first()
    return token.user if token else None


def require_user(request):
    user = current_user(request)
    if not user:
        return None, fail("请先登录", 401)
    return user, None


def require_admin(request):
    user, error = require_user(request)
    if error:
        return None, error
    if user.role != "admin" and not user.is_staff:
        return None, fail("无管理员权限", 403)
    return user, None


@csrf_exempt
def register(request):
    if request.method != "POST":
        return fail("只支持 POST", 405)
    data = body(request)
    username = data.get("username", "").strip()
    password = data.get("password", "")
    if not username or not password:
        return fail("账号和密码不能为空")
    if User.objects.filter(username=username).exists():
        return fail("账号已存在")
    user = User.objects.create(
        username=username,
        password=make_password(password),
        email=data.get("email", ""),
        nickname=data.get("nickname", username),
        role=data.get("role", "student"),
    )
    return ok({"id": user.id, "username": user.username, "role": user.role})


@csrf_exempt
def login(request):
    if request.method != "POST":
        return fail("只支持 POST", 405)
    data = body(request)
    user = authenticate(username=data.get("username", ""), password=data.get("password", ""))
    if not user:
        return fail("用户名或密码错误", 401)
    token = AuthToken.objects.create(user=user)
    return ok({"token": token.key, "user": {"id": user.id, "username": user.username, "nickname": user.nickname, "role": user.role}})


def me(request):
    user, error = require_user(request)
    if error:
        return error
    return ok({"id": user.id, "username": user.username, "nickname": user.nickname, "email": user.email, "role": user.role, "avatar": user.avatar})


@csrf_exempt
def upload_file(request):
    user, error = require_user(request)
    if error:
        return error
    file = request.FILES.get("file")
    if not file:
        return fail("未上传文件")

    ext = file.name.lower().rsplit(".", 1)[-1] if "." in file.name else ""
    video_exts = {"mp4", "webm", "ogg", "mov", "m4v"}
    allowed_exts = {"jpg", "jpeg", "png", "gif", "mp4", "webm", "ogg", "mov", "m4v", "pdf", "doc", "docx"}
    if ext not in allowed_exts:
        return fail("文件类型不支持")

    max_size = 500 * 1024 * 1024 if ext in video_exts else 20 * 1024 * 1024
    if file.size > max_size:
        return fail("视频文件不能超过 500MB" if ext in video_exts else "文件不能超过 20MB")

    folder = "videos" if ext in video_exts else "uploads"
    path = default_storage.save(f"{folder}/{timezone.now().strftime('%Y%m%d%H%M%S')}_{file.name}", file)
    url = default_storage.url(path)
    return ok({"path": request.build_absolute_uri(url), "name": file.name, "size": file.size})


def course_queryset(request):
    qs = CourseMaterial.objects.all().order_by("-course_materials_id")
    keyword = request.GET.get("keyword") or request.GET.get("course_name")
    teaching_type = request.GET.get("teaching_type")
    ordering = request.GET.get("ordering", "-course_materials_id")
    if keyword:
        qs = qs.filter(Q(course_name__icontains=keyword) | Q(teachers_name__icontains=keyword))
    if teaching_type:
        qs = qs.filter(teaching_type__icontains=teaching_type)
    if ordering.lstrip("-") in {"hits", "praise_len", "collect_len", "course_prices", "course_materials_id"}:
        qs = qs.order_by(ordering)
    return qs


@csrf_exempt
def course_list(request):
    fields = ["course_materials_id", "course_number", "teachers_name", "teaching_semester", "course_name", "teaching_type", "course_prices", "course_highlights", "course_images", "hits", "praise_len", "collect_len"]
    if request.method == "GET":
        return ok(paginate(request, course_queryset(request), fields))
    user, error = require_user(request)
    if error:
        return error
    if user.role not in {"teacher", "admin"}:
        return fail("只有教师或管理员可发布课程", 403)
    data = body(request)
    course = CourseMaterial.objects.create(**data)
    return ok(serialize(course, fields))


def course_detail(request, pk):
    course = CourseMaterial.objects.filter(pk=pk).first()
    if not course:
        return fail("课程不存在", 404)
    if request.method == "GET":
        course.hits += 1
        course.save(update_fields=["hits"])
        user = current_user(request)
        if user:
            BehaviorRecord.objects.create(user=user, course=course, behavior="browse", weight=1)
        return ok(serialize(course, ["course_materials_id", "course_number", "teachers_name", "teaching_semester", "course_name", "teaching_type", "course_prices", "course_highlights", "course_images", "course_introduction", "hits", "praise_len", "collect_len"]))
    user, error = require_user(request)
    if error:
        return error
    if user.role not in {"teacher", "admin"}:
        return fail("无操作权限", 403)
    if request.method in {"PUT", "PATCH"}:
        data = body(request)
        for key, value in data.items():
            if hasattr(course, key):
                setattr(course, key, value)
        course.save()
        return ok()
    if request.method == "DELETE":
        course.delete()
        return ok()
    return fail("请求方法不支持", 405)


@csrf_exempt
def buy_course(request, pk):
    user, error = require_user(request)
    if error:
        return error
    course = CourseMaterial.objects.filter(pk=pk).first()
    if not course:
        return fail("课程不存在", 404)
    order, _ = Order.objects.get_or_create(user=user, course=course, defaults={"amount": course.course_prices})
    BehaviorRecord.objects.create(user=user, course=course, behavior="purchase", weight=5)
    return ok({"order_id": order.id, "pay_state": order.pay_state})


VIDEO_FIELDS = ["online_video_id", "teachers_name", "video_name", "video_duration", "video_origin", "video_type", "video_content", "video_poster", "video_url", "hits", "praise_len", "collect_len", "comment_len"]


@csrf_exempt
def video_list(request):
    qs = OnlineVideo.objects.all().order_by("-online_video_id")
    keyword = request.GET.get("keyword") or request.GET.get("video_name")
    video_type = request.GET.get("video_type")
    if keyword:
        qs = qs.filter(video_name__icontains=keyword)
    if video_type:
        qs = qs.filter(video_type__icontains=video_type)
    if request.method == "GET":
        return ok(paginate(request, qs, VIDEO_FIELDS))
    user, error = require_user(request)
    if error:
        return error
    if user.role not in {"teacher", "admin"}:
        return fail("只有教师或管理员可以发布视频", 403)
    data = body(request)
    video = OnlineVideo.objects.create(
        teacher_users=user.id,
        teachers_name=data.get("teachers_name") or user.nickname or user.username,
        video_name=data.get("video_name", ""),
        video_duration=data.get("video_duration", ""),
        video_origin=data.get("video_origin", ""),
        video_type=data.get("video_type", ""),
        video_content=data.get("video_content", ""),
        video_poster=data.get("video_poster", ""),
        video_url=data.get("video_url", ""),
    )
    return ok(serialize(video, VIDEO_FIELDS))


@csrf_exempt
def video_detail(request, pk):
    video = OnlineVideo.objects.filter(pk=pk).first()
    if not video:
        return fail("视频不存在", 404)
    video.hits += 1
    video.save(update_fields=["hits"])
    return ok(serialize(video, VIDEO_FIELDS))


@csrf_exempt
def forum_list(request):
    qs = ForumPost.objects.all().order_by("-istop", "-forum_id")
    keyword = request.GET.get("keyword")
    post_type = request.GET.get("type")
    if keyword:
        qs = qs.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword) | Q(tag__icontains=keyword))
    if post_type:
        qs = qs.filter(type__icontains=post_type)
    if request.method == "GET":
        return ok(paginate(request, qs, ["forum_id", "nickname", "praise_len", "hits", "title", "description", "tag", "img", "create_time", "avatar", "type", "istop"]))
    user, error = require_user(request)
    if error:
        return error
    data = body(request)
    post = ForumPost.objects.create(user_id=user.id, nickname=user.nickname or user.username, title=data["title"], description=data.get("description", ""), tag=data.get("tag", ""), type=data.get("type", ""), img=data.get("img", ""), avatar=user.avatar)
    return ok({"forum_id": post.forum_id})


def forum_detail(request, pk):
    post = ForumPost.objects.filter(pk=pk).first()
    if not post:
        return fail("帖子不存在", 404)
    post.hits += 1
    post.save(update_fields=["hits"])
    return ok(serialize(post, ["forum_id", "nickname", "praise_len", "hits", "title", "keywords", "description", "url", "tag", "img", "create_time", "update_time", "avatar", "type", "istop"]))


@csrf_exempt
def news_list(request):
    qs = EducationNews.objects.filter(publish_state="已发布").order_by("-news_id")
    keyword = request.GET.get("keyword") or request.GET.get("title")
    category = request.GET.get("category")
    ordering = request.GET.get("ordering", "-news_id")
    if keyword:
        qs = qs.filter(Q(title__icontains=keyword) | Q(summary__icontains=keyword) | Q(tag__icontains=keyword))
    if category:
        qs = qs.filter(category__icontains=category)
    if ordering.lstrip("-") in {"hits", "praise_len", "comment_len", "news_id"}:
        qs = qs.order_by(ordering)
    if request.method == "GET":
        return ok(paginate(request, qs, ["news_id", "title", "category", "tag", "cover_image", "summary", "author", "hits", "praise_len", "comment_len", "create_time"]))
    user, error = require_admin(request)
    if error:
        return error
    news = EducationNews.objects.create(**body(request))
    return ok({"news_id": news.news_id})


def news_detail(request, pk):
    news = EducationNews.objects.filter(pk=pk, publish_state="已发布").first()
    if not news:
        return fail("资讯不存在", 404)
    news.hits += 1
    news.save(update_fields=["hits"])
    comments = NewsComment.objects.filter(news=news).order_by("-comment_id")[:20]
    data = serialize(news, ["news_id", "title", "category", "tag", "cover_image", "summary", "content", "author", "hits", "praise_len", "comment_len", "create_time", "update_time"])
    data["comments"] = [serialize(item, ["comment_id", "nickname", "avatar", "content", "create_time"]) for item in comments]
    return ok(data)


@csrf_exempt
def news_comments(request, pk):
    news = EducationNews.objects.filter(pk=pk).first()
    if not news:
        return fail("资讯不存在", 404)
    if request.method == "GET":
        comments = NewsComment.objects.filter(news=news).order_by("-comment_id")
        return ok(paginate(request, comments, ["comment_id", "nickname", "avatar", "content", "create_time"]))
    user, error = require_user(request)
    if error:
        return error
    data = body(request)
    comment = NewsComment.objects.create(news=news, user=user, nickname=user.nickname or user.username, avatar=user.avatar, content=data.get("content", ""))
    news.comment_len = NewsComment.objects.filter(news=news).count()
    news.save(update_fields=["comment_len"])
    return ok(serialize(comment, ["comment_id", "nickname", "avatar", "content", "create_time"]))


@csrf_exempt
def notice_list(request):
    qs = Notice.objects.filter(publish_state="已发布").order_by("-id")
    fields = ["id", "title", "category", "content", "publish_state", "create_time", "update_time"]
    if request.method == "GET":
        return ok(paginate(request, qs, fields))
    user, error = require_admin(request)
    if error:
        return error
    if request.method == "POST":
        data = body(request)
        notice = Notice.objects.create(
            title=data.get("title", ""),
            category=data.get("category", ""),
            content=data.get("content", ""),
            publish_state=data.get("publish_state", "已发布"),
        )
        return ok(serialize(notice, fields))
    return fail("请求方法不支持", 405)


@csrf_exempt
def notice_detail(request, pk):
    notice = Notice.objects.filter(pk=pk).first()
    if not notice:
        return fail("公告不存在", 404)
    user, error = require_admin(request)
    if error:
        return error
    fields = ["id", "title", "category", "content", "publish_state", "create_time", "update_time"]
    if request.method in {"PUT", "PATCH"}:
        data = body(request)
        for key in ["title", "category", "content", "publish_state"]:
            if key in data:
                setattr(notice, key, data[key])
        notice.save()
        return ok(serialize(notice, fields))
    if request.method == "DELETE":
        notice.delete()
        return ok()
    return fail("请求方法不支持", 405)


def banner_list(request):
    qs = Banner.objects.all().order_by("sort", "-id")
    return ok({"items": [serialize(item, ["id", "title", "image", "link", "sort"]) for item in qs]})


@csrf_exempt
def banner_manage(request):
    if request.method == "GET":
        return banner_list(request)
    user, error = require_admin(request)
    if error:
        return error
    if request.method == "POST":
        data = body(request)
        banner = Banner.objects.create(
            title=data.get("title", "轮播图"),
            image=data.get("image", ""),
            link=data.get("link", ""),
            sort=int(data.get("sort", 0) or 0),
        )
        return ok(serialize(banner, ["id", "title", "image", "link", "sort"]))
    if request.method == "DELETE":
        data = body(request)
        ids = data.get("ids", [])
        Banner.objects.filter(id__in=ids).delete()
        return ok()
    return fail("请求方法不支持", 405)


@csrf_exempt
def interaction_list(request):
    user, error = require_user(request)
    if error:
        return error
    kind = request.GET.get("kind", "like")
    model = Like if kind == "like" else Favorite
    if request.method == "GET":
        qs = model.objects.filter(user=user).order_by("-id")
        return ok({"items": [{"id": item.id, "target_type": item.target_type, "target_id": item.target_id, "target_title": item_title(item.target_type, item.target_id), "create_time": item.create_time.strftime("%Y-%m-%d %H:%M:%S")} for item in qs]})
    data = body(request)
    target_type = data.get("target_type", "")
    target_id = int(data.get("target_id", 0) or 0)
    existing = model.objects.filter(user=user, target_type=target_type, target_id=target_id).first()
    if request.method == "POST":
        if existing:
            return ok({"id": existing.id, "created": False})
        item = model.objects.create(user=user, target_type=target_type, target_id=target_id)
        return ok({"id": item.id, "created": True})
    if request.method == "DELETE":
        if existing:
            existing.delete()
        return ok()
    return fail("请求方法不支持", 405)


@csrf_exempt
def comment_list(request):
    user, error = require_user(request)
    if error:
        return error
    if request.method == "GET":
        qs = Comment.objects.filter(user=user).order_by("-comment_id")
        target_type = request.GET.get("target_type")
        target_id = request.GET.get("target_id")
        if target_type:
            qs = qs.filter(target_type=target_type)
        if target_id:
            qs = qs.filter(target_id=target_id)
        return ok({"items": [serialize(item, ["comment_id", "target_type", "target_id", "target_title", "nickname", "avatar", "content", "create_time"]) for item in qs]})
    if request.method == "POST":
        data = body(request)
        comment = Comment.objects.create(
            user=user,
            target_type=data.get("target_type", ""),
            target_id=int(data.get("target_id", 0) or 0),
            target_title=data.get("target_title") or item_title(data.get("target_type", ""), int(data.get("target_id", 0) or 0)),
            nickname=user.nickname or user.username,
            avatar=user.avatar,
            content=data.get("content", ""),
        )
        return ok(serialize(comment, ["comment_id", "target_type", "target_id", "target_title", "nickname", "avatar", "content", "create_time"]))
    if request.method == "DELETE":
        Comment.objects.filter(comment_id=body(request).get("id"), user=user).delete()
        return ok()
    return fail("请求方法不支持", 405)


def recommend_courses(request):
    user, error = require_user(request)
    if error:
        hot = CourseMaterial.objects.order_by("-hits", "-collect_len")[:8]
        return ok({"items": [serialize(item, ["course_materials_id", "course_name", "teaching_type", "course_images", "course_prices", "hits"]) for item in hot]})
    records = BehaviorRecord.objects.select_related("course", "user").all()
    matrix = defaultdict(dict)
    for item in records:
        matrix[item.user_id][item.course_id] = matrix[item.user_id].get(item.course_id, 0) + item.weight
    target = matrix.get(user.id, {})
    if len(target) < 2:
        qs = CourseMaterial.objects.exclude(course_materials_id__in=target.keys()).order_by("-hits", "-collect_len")[:8]
        return ok({"items": [serialize(item, ["course_materials_id", "course_name", "teaching_type", "course_images", "course_prices", "hits"]) for item in qs]})
    scores = defaultdict(float)
    for other_user, other in matrix.items():
        if other_user == user.id:
            continue
        common = set(target) & set(other)
        if not common:
            continue
        dot = sum(target[c] * other[c] for c in common)
        norm1 = math.sqrt(sum(v * v for v in target.values()))
        norm2 = math.sqrt(sum(v * v for v in other.values()))
        similarity = dot / (norm1 * norm2) if norm1 and norm2 else 0
        for course_id, weight in other.items():
            if course_id not in target:
                scores[course_id] += similarity * weight
    ids = [course_id for course_id, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:8]]
    qs = CourseMaterial.objects.filter(course_materials_id__in=ids)
    return ok({"items": [serialize(item, ["course_materials_id", "course_name", "teaching_type", "course_images", "course_prices", "hits"]) for item in qs]})


def admin_users(request):
    _, error = require_admin(request)
    if error:
        return error
    qs = User.objects.all().order_by("-id")
    keyword = request.GET.get("keyword")
    if keyword:
        qs = qs.filter(Q(username__icontains=keyword) | Q(nickname__icontains=keyword))
    return ok(paginate(request, qs, ["id", "username", "nickname", "email", "role", "status", "avatar", "date_joined"]))


def admin_statistics(request):
    _, error = require_admin(request)
    if error:
        return error
    return ok(
        {
            "users": User.objects.count(),
            "courses": CourseMaterial.objects.count(),
            "videos": OnlineVideo.objects.count(),
            "news": EducationNews.objects.count(),
            "orders": Order.objects.count(),
            "sales": Order.objects.aggregate(total=Sum("amount"))["total"] or 0,
            "course_sales": list(Order.objects.values("course__course_name").annotate(total=Count("id")).order_by("-total")[:10]),
        }
    )


@csrf_exempt
def video_detail(request, pk):
    video = OnlineVideo.objects.filter(pk=pk).first()
    if not video:
        return fail("视频不存在", 404)
    if request.method == "DELETE":
        _, error = require_admin(request)
        if error:
            return error
        video.delete()
        return ok()
    if request.method in {"PUT", "PATCH"}:
        _, error = require_admin(request)
        if error:
            return error
        data = body(request)
        for key in ["teachers_name", "video_name", "video_duration", "video_origin", "video_type", "video_content", "video_poster", "video_url"]:
            if key in data:
                setattr(video, key, data[key])
        video.save()
        return ok(serialize(video, VIDEO_FIELDS))
    video.hits += 1
    video.save(update_fields=["hits"])
    return ok(serialize(video, VIDEO_FIELDS))


def forum_detail(request, pk):
    post = ForumPost.objects.filter(pk=pk).first()
    if not post:
        return fail("帖子不存在", 404)
    if request.method == "DELETE":
        _, error = require_admin(request)
        if error:
            return error
        post.delete()
        return ok()
    post.hits += 1
    post.save(update_fields=["hits"])
    return ok(serialize(post, ["forum_id", "nickname", "praise_len", "hits", "title", "keywords", "description", "url", "tag", "img", "create_time", "update_time", "avatar", "type", "istop"]))


def news_detail(request, pk):
    news = EducationNews.objects.filter(pk=pk, publish_state="已发布").first()
    if not news:
        return fail("资讯不存在", 404)
    if request.method == "DELETE":
        _, error = require_admin(request)
        if error:
            return error
        news.delete()
        return ok()
    news.hits += 1
    news.save(update_fields=["hits"])
    comments = NewsComment.objects.filter(news=news).order_by("-comment_id")[:20]
    data = serialize(news, ["news_id", "title", "category", "tag", "cover_image", "summary", "content", "author", "hits", "praise_len", "comment_len", "create_time", "update_time"])
    data["comments"] = [serialize(item, ["comment_id", "nickname", "avatar", "content", "create_time"]) for item in comments]
    return ok(data)
