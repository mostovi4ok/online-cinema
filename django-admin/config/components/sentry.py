import django.db.models.signals
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from config import configs


if configs.sentry_on:
    sentry_sdk.init(
        dsn=configs.sentry_dsn,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        integrations=[
            DjangoIntegration(
                transaction_style="url",
                middleware_spans=True,
                signals_spans=True,
                signals_denylist=[
                    django.db.models.signals.pre_init,
                    django.db.models.signals.post_init,
                ],
                cache_spans=False,
                http_methods_to_capture=("GET",),
            ),
        ],
    )
