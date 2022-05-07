from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# init SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    # 
    app.app_context().push()
    
    db.init_app(app)

    # handling user sessions
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login_post'
    login_manager.init_app(app)
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # auth routes
    from .routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # non-auth routes
    from .routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .routes.lyrics import lyrics as lyrics_blueprint
    app.register_blueprint(lyrics_blueprint)

    from .routes.reviews import reviews as reviews_blueprint
    app.register_blueprint(reviews_blueprint)

    from .routes.follow import follow as follow_blueprint
    app.register_blueprint(follow_blueprint)

    return app