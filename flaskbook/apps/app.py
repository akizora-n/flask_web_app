from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from apps.config import config

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
# login_view属性に未ログイン時にリダイレクトするエンドポイントを指定する
login_manager.login_view = "auth.signup"
# login_message属性にログイン後に表示するメッセージを指定する
# ここでは何も表示しないよう空を指定する
login_manager.login_message = ""


# create_app関数を作成する
def create_app(config_key):
    # Flaskインスタンス生成
    app = Flask(__name__)
    # config_keyにマッチする環境のコンフィグクラスを読み込む
    app.config.from_object(config[config_key])
    # SQLAlchemyとアプリを連携する
    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    # Migrateとアプリを連携する
    Migrate(app, db)
    # crud(create, read, update, delete)パッケージからviewsをimportする
    from apps.auth import views as auth_views
    from apps.crud import views as crud_views
    from apps.detector import views as dt_views

    # カスタムエラー画面を登録する
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    # register_blueprintを使いviewsのcrudをアプリへ登録する
    app.register_blueprint(crud_views.crud, url_prefix="/crud")
    # register_blueprintを使いviewsのauthをアプリへ登録する
    app.register_blueprint(auth_views.auth, url_prefix="/auth")
    # register_blueprintを使いviewのdtをアプリへ登録する
    app.register_blueprint(dt_views.dt)

    return app


def page_not_found(e):
    """404 Not Found"""
    return render_template("404.html"), 404


def internal_server_error(e):
    """500 Internal Server Error"""
    return render_template("500.html"), 500
