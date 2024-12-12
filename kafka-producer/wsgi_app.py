from gevent import monkey


monkey.patch_all()

from main import app as app  # noqa: E402, PLC0414
