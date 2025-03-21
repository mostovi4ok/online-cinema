"""
This type stub file was generated by pyright.
"""

import threading

log = ...

class Sender(threading.Thread):
    """
    The background thread that handles the sending of produce requests to the
    Kafka cluster. This thread makes metadata requests to renew its view of the
    cluster and then sends produce requests to the appropriate nodes.
    """

    DEFAULT_CONFIG = ...
    def __init__(self, client, metadata, accumulator, metrics, **configs) -> None: ...
    def run(self):  # -> None:
        """The main run loop for the sender thread."""

    def run_once(self):  # -> None:
        """Run a single iteration of sending."""

    def initiate_close(self):  # -> None:
        """Start closing the sender (won't complete until all data is sent)."""

    def force_close(self):  # -> None:
        """Closes the sender without sending out any pending messages."""

    def add_topic(self, topic):  # -> None:
        ...
    def wakeup(self):  # -> None:
        """Wake up the selector associated with this send thread."""

    def bootstrap_connected(self): ...

class SenderMetrics:
    def __init__(self, metrics, client, metadata) -> None: ...
    def add_metric(
        self, metric_name, measurable, group_name=..., description=..., tags=..., sensor_name=...
    ):  # -> None:
        ...
    def maybe_register_topic_metrics(self, topic):  # -> None:
        ...
    def update_produce_request_metrics(self, batches_map):  # -> None:
        ...
    def record_retries(self, topic, count):  # -> None:
        ...
    def record_errors(self, topic, count):  # -> None:
        ...
    def record_throttle_time(self, throttle_time_ms, node=...):  # -> None:
        ...
