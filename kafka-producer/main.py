import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration

from api.v1.producer import analytics_bp
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


app.register_blueprint(analytics_bp, url_prefix="/api/v1")
