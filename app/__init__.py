from flask import Flask, render_template
from flask_login import LoginManager
from flask_user import UserManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging

# init SQLAlchemy so we can use it later in our models

db = SQLAlchemy()


def page_not_found(e):
    return render_template('404.html'), 404


def create_app():
    app = Flask(__name__)
    app.register_error_handler(404, page_not_found)
    app.config.from_object('config.DevelopmentConfig')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    db.init_app(app)

    migrate = Migrate(app, db)

    login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    # Customize Flask-User
    class CustomUserManager(UserManager):

        # Override the default password validator
        def password_validator(self, field):
            return True

        # Override or extend the default login view method
        def login_view(self):
            return render_template('login.html')

    # Setup Flask-User and specify the User data-model
    user_manager = CustomUserManager(app, db, User)

    # user_manager.login_view = 'auth.login'

    # @app.context_processor
    # def context_processor():
    #     return dict(user_manager=user_manager)

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    @app.cli.command("import-repo")
    def import_repo():
        print(' Start job import cli -->')
        from app.services.repo_orm import read_json
        read_json()
        print(' <-- End job import cli')

    @app.cli.command("import-repo-csv")
    def import_repo_csv():
        print(' Start job import repo csv -->')
        from app.services.import_csv_orm import import_repo_csv
        import_repo_csv()
        print(' <-- End job import repo csv')

    @app.cli.command("import-title-csv")
    def import_title_csv():
        print(' Start job import title csv -->')
        from app.services.import_csv_orm import import_title_log_csv
        import_title_log_csv()
        print(' <-- End job import title csv')

    @app.cli.command("import-pif-csv")
    def import_pif_csv():
        print(' Start job import pif csv -->')
        from app.services.import_csv_orm import import_pif_log_csv
        import_pif_log_csv()
        print(' <-- End job import pif csv')

    @app.cli.command("import-ext-csv")
    def import_ext_csv():
        print(' Start job import ext csv -->')
        from app.services.import_csv_orm import import_ext_log_csv
        import_ext_log_csv()
        print(' <-- End job import ext csv')

    @app.cli.command("import-pif")
    def import_pif():
        from app.services.repo_orm import import_pif_json
        import_pif_json()

    @app.cli.command("import-title")
    def import_title():
        from app.services.repo_orm import import_tf_json
        import_tf_json()

    @app.cli.command("import-extension")
    def import_extension():
        from app.services.repo_orm import import_ext_json
        import_ext_json()

    @app.cli.command('real-disc-to-nrv')
    def real_disc_to_nrv():
        from app.services.repo_orm import load_nrv
        load_nrv()

    @app.cli.command('val-allow')
    def val_allow():
        from app.services.repo_orm import load_val_allow
        load_val_allow()

    @app.cli.command("bootstrap")
    def bootstrap_data():
        print('Start job load categories -->')
        from app.services.repo_orm import load_categories, load_default_user, load_test_users
        load_categories()
        print('<-- End job load categories')
        print('Start job load_default_user -->')
        # load_default_user()
        # load_test_users()
        print('End job load_default_user -->')

    @app.cli.command("import-all")
    def import_all():
        print('import all')
        print('Start job load categories -->')
        from app.services.repo_orm import load_categories, \
            load_default_user, read_json, \
            import_pif_json, import_tf_json, import_ext_json, \
            load_nrv, load_val_allow
        load_categories()
        print('<-- End job load categories')
        print('Start job load_default_user -->')
        load_default_user()
        print('End job load_default_user -->')
        read_json()
        import_pif_json()
        import_tf_json()
        import_ext_json()
        load_nrv()
        load_val_allow()

    return app
