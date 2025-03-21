"""
This type stub file was generated by pyright.
"""

from opentelemetry.exporter.jaeger.thrift.gen.jaeger import Collector as jaeger

UDP_PACKET_MAX_LENGTH = ...
logger = ...

class AgentClientUDP:
    """Implement a UDP client to agent.

    Args:
        host_name: The host name of the Jaeger server.
        port: The port of the Jaeger server.
        max_packet_size: Maximum size of UDP packet.
        client: Class for creating new client objects for agencies.
        split_oversized_batches: Re-emit oversized batches in smaller chunks.

    """

    def __init__(self, host_name, port, max_packet_size=..., client=..., split_oversized_batches=...) -> None: ...
    def emit(self, batch: jaeger.Batch):  # -> None:
        """
        Args:
            batch: Object to emit Jaeger spans.

        """

class Collector:
    """Submits collected spans to Jaeger collector in jaeger.thrift
    format over binary thrift protocol. This is recommend option in cases where
    it is not feasible to deploy Jaeger Agent next to the application,
    for example, when the application code is running as AWS Lambda function.
    In these scenarios the Jaeger Clients can be configured to submit spans directly
    to the Collectors over HTTP/HTTPS.

    Args:
        thrift_url: Endpoint used to send spans
            directly to Collector the over HTTP.
        auth: Auth tuple that contains username and password for Basic Auth.
        timeout_in_millis: timeout for THttpClient.

    """

    def __init__(self, thrift_url=..., auth=..., timeout_in_millis=...) -> None: ...
    def submit(self, batch: jaeger.Batch):  # -> None:
        """Submits batches to Thrift HTTP Server through Binary Protocol.

        Args:
            batch: Object to emit Jaeger spans.

        """
