"""
This type stub file was generated by pyright.
"""

import redis

from .commands import JSONCommands

class JSON(JSONCommands):
    """
    Create a client for talking to json.

    :param decoder:
    :type json.JSONDecoder: An instance of json.JSONDecoder

    :param encoder:
    :type json.JSONEncoder: An instance of json.JSONEncoder
    """

    def __init__(self, client, version=..., decoder=..., encoder=...) -> None:
        """
        Create a client for talking to json.

        :param decoder:
        :type json.JSONDecoder: An instance of json.JSONDecoder

        :param encoder:
        :type json.JSONEncoder: An instance of json.JSONEncoder
        """

    def pipeline(self, transaction=..., shard_hint=...):  # -> ClusterPipeline | Pipeline:
        """Creates a pipeline for the JSON module, that can be used for executing
        JSON commands, as well as classic core commands.

        Usage example:

        r = redis.Redis()
        pipe = r.json().pipeline()
        pipe.jsonset('foo', '.', {'hello!': 'world'})
        pipe.jsonget('foo')
        pipe.jsonget('notakey')
        """

class ClusterPipeline(JSONCommands, redis.cluster.ClusterPipeline):
    """Cluster pipeline for the module."""

class Pipeline(JSONCommands, redis.client.Pipeline):
    """Pipeline for the module."""
