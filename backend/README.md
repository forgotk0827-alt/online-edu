# 在线教育平台后端

## 快速启动

```bash
cd backend
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

默认使用 SQLite，便于本地直接运行。需要 MySQL 时设置环境变量：

```bash
set MYSQL_DATABASE=online_education
set MYSQL_USER=root
set MYSQL_PASSWORD=你的密码
set MYSQL_HOST=127.0.0.1
set MYSQL_PORT=3306
```

MySQL 建表脚本位于 `sql/schema.sql`。
