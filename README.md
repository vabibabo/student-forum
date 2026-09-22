# Student Forum

A Flask coursework project for student discussions, with SQLAlchemy data models, Jinja templates, Bootstrap styling and MySQL integration.

## Features represented in the source
- Registration, password hashing, session-based login and logout.
- Topic creation and detail pages, discussion comments and replies.
- Keyword search across topic titles and content.
- Responsive page styling and human-readable timestamps.

## Structure
`app.py` contains routes; `models.py` defines users, topics, comments and replies; `templates/` and `static/` contain the interface. `config.py` reads local environment variables instead of the original embedded database credentials.

## Local setup
```sh
python -m venv .venv
# Activate the environment.
python -m pip install -r requirements.txt
```

Set `DATABASE_URL` and `SECRET_KEY` in your shell; `.env.example` documents their format and is not loaded automatically. MySQL was used in the coursework. A disposable SQLite database is the default for local investigation only. Create an empty schema using the SQLAlchemy models:

```sh
python -c "from app import app; from exts import db; app.app_context().push(); db.create_all()"
python app.py
```

Dependencies are inferred from imports, not a recovered lockfile. Compatibility and complete user journeys have not been verified against a newly installed environment.

## Historical limitations
- Comment creation does not populate the non-null `Claim.title` field.
- The reply POST redirects to an endpoint named `reply` that is absent from the supplied routes.
- The landing route does not explicitly query and supply topic data.
- Search uses an older ordering expression which may need migration for current SQLAlchemy.
- The legacy Flask-Script migration launcher was excluded because it contained an embedded database connection string; no original migration directory was supplied.

This repository preserves coursework for review. It is not a production deployment. Existing interface images are retained as coursework assets; no new reuse licence is assigned to third-party material.

## 中文简介
学生论坛课业，展示 Flask 路由、关系数据库、登录会话及网页开发。已清除数据库密码；保留原作并明确记录尚待修复的问题。
