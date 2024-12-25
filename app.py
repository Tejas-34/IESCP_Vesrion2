from flask import Flask

from flask_security import Security, SQLAlchemyUserDatastore
from werkzeug.security import generate_password_hash
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from Backend.Application.utils import celery_init_app
from Backend.Application.worker import daily_reminder, monthly_reminder
from celery.schedules import crontab

def create_app():
    from Backend.Application.cache import cache
    from Backend.Application.models import db, User, Role


    app = Flask(__name__)

    # Use an in-memory db
    app.config['SECRET_KEY'] = "sdgdfgvdsfgvdsfvd"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///model.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
   
    app.config["SECURITY_PASSWORD_SALT"] = "ergesfgsdfsdff"
    app.config["JWT_SECRET_KEY"] = "asfsdvsdfvsdfsddsfv"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600

    app.config["CELERY"] = {
    "broker_url": "redis://localhost:6379/1",
    "result_backend": "redis://localhost:6379/2",
    "broker_connection_retry_on_startup": True,
    }

    

 
    db.init_app(app)
    CORS(app)
    cache.init_app(app)
    jwt = JWTManager(app)


    datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, datastore)

    with app.app_context():
        db.create_all()
        if not app.security.datastore.find_user(username="admin"): 
            app.security.datastore.create_user(name="admin", username="admin",Email="admin@123", password=generate_password_hash("admin123"))
            app.security.datastore.create_role(name="admin")
            app.security.datastore.add_role_to_user(app.security.datastore.find_user(username="admin"),
                                                    app.security.datastore.find_role("admin"))
            db.session.commit()

    from Backend.Application.routes import api
    app.register_blueprint(api)
    
    return app






app = create_app()
celery = celery_init_app(app)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=18, minute=0), daily_reminder.s(), name="say hello")
    sender.add_periodic_task(40000, monthly_reminder.s(), name="monthly reminder") #crontab(day_of_month=1, hour=7, minute=0)


if __name__ == "__main__" :
    app.run(debug=True)
