import sentry_sdk
from flask import Flask
from flask_jwt_extended import JWTManager
from sentry_sdk.integrations.flask import FlaskIntegration

from api.v1.analytics import analytics_bp
from core.config import configs


if configs.sentry_on:
    sentry_sdk.init(
        dsn=configs.sentry_dsn,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        integrations=[
            FlaskIntegration(
                transaction_style="url",
                http_methods_to_capture=("GET",),
            ),
        ],
    )


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = configs.jwt_secret_key
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

jwt = JWTManager(app)


app.register_blueprint(analytics_bp, url_prefix="/api/v1")
