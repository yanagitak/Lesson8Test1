# app.py
import os
from datetime import datetime

from flask import Flask, request, redirect, url_for, render_template
from sqlalchemy import create_engine, Integer, String, Text, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# .env を読み込む（存在しなければ無視）
load_dotenv()

# -------------------------
# DB 接続設定
# -------------------------
database_url = os.environ.get("DATABASE_URL")
if not database_url:
    raise RuntimeError("DATABASE_URL が設定されていません")

# postgres:// → postgresql+psycopg://
if database_url.startswith("postgres://"):
    url = database_url.replace(
        "postgres://",
        "postgresql+psycopg://",
        1,
    )


engine = create_engine(database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False)


# -------------------------
# SQLAlchemy モデル
# -------------------------
class Base(DeclarativeBase):
    pass


class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )


Base.metadata.create_all(engine)

# -------------------------
# Flask
# -------------------------
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    form = {}

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        minutes_raw = request.form.get("minutes", "").strip()
        description = request.form.get("description", "").strip()

        form = {
            "title": title,
            "minutes": minutes_raw,
            "description": description,
        }

        # バリデーション
        if not title:
            error = "タイトルは必須です。"
        else:
            try:
                minutes = int(minutes_raw)
                if minutes < 1:
                    raise ValueError
            except ValueError:
                error = "所要分数は 1 以上の整数で入力してください。"

        if not error:
            try:
                with SessionLocal() as session:
                    session.add(
                        Recipe(
                            title=title,
                            minutes=minutes,
                            description=description or None,
                        )
                    )
                    session.commit()
                return redirect(url_for("index"))
            except SQLAlchemyError:
                error = "データベースエラーが発生しました。"

    with SessionLocal() as session:
        recipes = (
            session.query(Recipe)
            .order_by(Recipe.created_at.desc())
            .all()
        )

    return render_template(
        "index.html",
        recipes=recipes,
        error=error,
        form=form,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    debug = os.environ.get("DEBUG", "false").lower() == "true"

    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug,
    )
