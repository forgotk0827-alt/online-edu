# 在线教育平台

本项目按需求文档实现在线教育平台的基础可运行版本，包含 Django 后端、MySQL 建表 SQL、Vue + Element Plus 前台客户端和后台管理系统。

## 目录

- `backend`：Django 后端接口、模型、推荐算法、上传接口
- `backend/sql/schema.sql`：MySQL 建表 SQL
- `frontend`：Vue 客户端与后台管理页面

## 后端启动

```bash
cd backend
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

## 前端启动

```bash
cd frontend
npm install
npm run dev
```

访问前台：`http://127.0.0.1:5173/#/`

访问后台：`http://127.0.0.1:5173/#/admin`

## 已实现范围

- 用户注册、登录、Token 鉴权
- 课程资料、在线视频、学习交流、教育资讯、网站公告接口
- 教育资讯详情与评论接口
- 课程购买和协同过滤课程推荐
- 文件上传到本地 `media` 目录
- 前台统一粉紫风格响应式页面
- 后台统一蓝紫风格管理页面
- ECharts 购买资料统计图表
