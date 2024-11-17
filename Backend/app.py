from flask import Flask
from Application.models import db, User, Role
from flask_security import Security, SQLAlchemyUserDatastore
from werkzeug.security import generate_password_hash
from flask_cors import CORS
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)

    # Use an in-memory db
    app.config ['SECRET_KEY'] = "sdgdfgvdsfgvdsfvd"
    app.config ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///model.db"
    app.config["SECURITY_PASSWORD_SALT"] = "ergesfgsdfsdff"
    app.config["JWT_SECRET_KEY"] = "asfsdvsdfvsdfsddsfv"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600
 
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app)


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

    from Application.routes import api

    app.register_blueprint(api)
    return app

app = create_app()

if __name__ == "__main__" :
    app.run(debug=True)
