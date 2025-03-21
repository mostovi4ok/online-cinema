"""
This type stub file was generated by pyright.
"""

class Heartbeat:
    DEFAULT_CONFIG = ...
    def __init__(self, **configs) -> None: ...
    def poll(self):  # -> None:
        ...
    def sent_heartbeat(self):  # -> None:
        ...
    def fail_heartbeat(self):  # -> None:
        ...
    def received_heartbeat(self):  # -> None:
        ...
    def time_to_next_heartbeat(self):  # -> float:
        """Returns seconds (float) remaining before next heartbeat should be sent"""

    def should_heartbeat(self):  # -> bool:
        ...
    def session_timeout_expired(self):  # -> bool:
        ...
    def reset_timeouts(self):  # -> None:
        ...
    def poll_timeout_expired(self):  # -> bool:
        ...
