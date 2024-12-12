"""
This type stub file was generated by pyright.
"""

from ssl import SSLContext
from typing import Any

from aiokafka.protocol.api import Response
from aiokafka.structs import OffsetAndMetadata, TopicPartition

from .config_resource import ConfigResource
from .new_partitions import NewPartitions
from .new_topic import NewTopic
from .records_to_delete import RecordsToDelete

log = ...

class AIOKafkaAdminClient:
    """A class for administering the Kafka cluster.

    .. note::

        This class is considered **experimental**, so beware that it is subject
        to changes even in patch releases.

    Keyword Arguments:
        bootstrap_servers: 'host[:port]' string (or list of 'host[:port]'
            strings) that the consumer should contact to bootstrap initial
            cluster metadata. This does not have to be the full node list.
            It just needs to have at least one broker that will respond to a
            Metadata API Request. Default port is 9092. If no servers are
            specified, will default to localhost:9092.
        client_id (str): a name for this client. This string is passed in
            each request to servers and can be used to identify specific
            server-side log entries that correspond to this client. Also
            submitted to GroupCoordinator for logging with respect to
            consumer group administration. Default: 'aiokafka-{version}'
        request_timeout_ms (int): Client request timeout in milliseconds.
            Default: 40000.
        connections_max_idle_ms: Close idle connections after the number of
            milliseconds specified by this config. The broker closes idle
            connections after connections.max.idle.ms, so this avoids hitting
            unexpected socket disconnected errors on the client.
            Default: 540000
        retry_backoff_ms (int): Milliseconds to backoff when retrying on
            errors. Default: 100.
        metadata_max_age_ms (int): The period of time in milliseconds after
            which we force a refresh of metadata even if we haven't seen any
            partition leadership changes to proactively discover any new
            brokers or partitions. Default: 300000
        security_protocol (str): Protocol used to communicate with brokers.
            Valid values are: PLAINTEXT, SSL, SASL_PLAINTEXT, SASL_SSL.
            Default: PLAINTEXT.
        ssl_context (ssl.SSLContext): Pre-configured SSLContext for wrapping
            socket connections. If provided, all other ssl_* configurations
            will be ignored. Default: None.
        api_version (str): Specify which kafka API version to use.
            AIOKafka supports Kafka API versions >=0.9 only.
            If set to 'auto', will attempt to infer the broker version by
            probing various APIs. Default: auto

    """

    def __init__(
        self,
        *,
        loop=...,
        bootstrap_servers: str | list[str] = ...,
        client_id: str = ...,
        request_timeout_ms: int = ...,
        connections_max_idle_ms: int = ...,
        retry_backoff_ms: int = ...,
        metadata_max_age_ms: int = ...,
        security_protocol: str = ...,
        ssl_context: SSLContext | None = ...,
        api_version: str = ...,
        sasl_mechanism: str = ...,
        sasl_plain_username: str | None = ...,
        sasl_plain_password: str | None = ...,
        sasl_kerberos_service_name: str = ...,
        sasl_kerberos_domain_name: str | None = ...,
        sasl_oauth_token_provider: str | None = ...,
    ) -> None: ...
    async def close(self):  # -> None:
        """Close the AIOKafkaAdminClient connection to the Kafka broker."""

    async def start(self):  # -> None:
        ...
    async def create_topics(
        self, new_topics: list[NewTopic], timeout_ms: int | None = ..., validate_only: bool = ...
    ) -> Response:
        """Create new topics in the cluster.

        :param new_topics: A list of NewTopic objects.
        :param timeout_ms: Milliseconds to wait for new topics to be created
            before the broker returns.
        :param validate_only: If True, don't actually create new topics.
            Not supported by all versions. Default: False
        :return: Appropriate version of CreateTopicResponse class.
        """

    async def delete_topics(self, topics: list[str], timeout_ms: int | None = ...) -> Response:
        """Delete topics from the cluster.

        :param topics: A list of topic name strings.
        :param timeout_ms: Milliseconds to wait for topics to be deleted
            before the broker returns.
        :return: Appropriate version of DeleteTopicsResponse class.
        """

    async def list_topics(self) -> list[str]: ...
    async def describe_topics(self, topics: list[str] | None = ...) -> list[Any]: ...
    async def describe_cluster(self) -> dict[str, Any]: ...
    async def describe_configs(
        self, config_resources: list[ConfigResource], include_synonyms: bool = ...
    ) -> list[Response]:
        """Fetch configuration parameters for one or more Kafka resources.

        :param config_resources: An list of ConfigResource objects.
            Any keys in ConfigResource.configs dict will be used to filter the
            result. Setting the configs dict to None will get all values. An
            empty dict will get zero values (as per Kafka protocol).
        :param include_synonyms: If True, return synonyms in response. Not
            supported by all versions. Default: False.
        :return: List of appropriate version of DescribeConfigsResponse class.
        """

    async def alter_configs(self, config_resources: list[ConfigResource]) -> list[Response]:
        """Alter configuration parameters of one or more Kafka resources.
        :param config_resources: A list of ConfigResource objects.
        :return: Appropriate version of AlterConfigsResponse class.
        """

    async def create_partitions(
        self, topic_partitions: dict[str, NewPartitions], timeout_ms: int | None = ..., validate_only: bool = ...
    ) -> Response:
        """Create additional partitions for an existing topic.

        :param topic_partitions: A map of topic name strings to NewPartition
         objects.
        :param timeout_ms: Milliseconds to wait for new partitions to be
            created before the broker returns.
        :param validate_only: If True, don't actually create new partitions.
            Default: False
        :return: Appropriate version of CreatePartitionsResponse class.
        """

    async def describe_consumer_groups(
        self, group_ids: list[str], group_coordinator_id: int | None = ..., include_authorized_operations: bool = ...
    ) -> list[Response]:
        """Describe a set of consumer groups.

        Any errors are immediately raised.

        :param group_ids: A list of consumer group IDs. These are typically the
            group names as strings.
        :param group_coordinator_id: The node_id of the groups' coordinator
            broker. If set to None, it will query the cluster for each group to
            find that group's coordinator. Explicitly specifying this can be
            useful for avoiding extra network round trips if you already know
            the group coordinator. This is only useful when all the group_ids
            have the same coordinator, otherwise it will error. Default: None.
        :param include_authorized_operations: Whether or not to include
            information about the operations a group is allowed to perform.
            Only supported on API version >= v3. Default: False.
        :return: A list of group descriptions. For now the group descriptions
            are the raw results from the DescribeGroupsResponse.
        """

    async def list_consumer_groups(self, broker_ids: list[int] | None = ...) -> list[tuple[Any, ...]]:
        """List all consumer groups known to the cluster.

        This returns a list of Consumer Group tuples. The tuples are
        composed of the consumer group name and the consumer group protocol
        type.

        Only consumer groups that store their offsets in Kafka are returned.
        The protocol type will be an empty string for groups created using
        Kafka < 0.9 APIs because, although they store their offsets in Kafka,
        they don't use Kafka for group coordination. For groups created using
        Kafka >= 0.9, the protocol type will typically be "consumer".

        As soon as any error is encountered, it is immediately raised.

        :param broker_ids: A list of broker node_ids to query for consumer
            groups. If set to None, will query all brokers in the cluster.
            Explicitly specifying broker(s) can be useful for determining which
            consumer groups are coordinated by those broker(s). Default: None
        :return list: List of tuples of Consumer Groups.
        :exception GroupCoordinatorNotAvailableError: The coordinator is not
            available, so cannot process requests.
        :exception GroupLoadInProgressError: The coordinator is loading and
            hence can't process requests.
        """

    async def find_coordinator(self, group_id: str, coordinator_type: int = ...) -> int:
        """Find the broker id for a given consumer group

        :param group_id: str the group id
        :param coordinator_type: int the type of coordinator:
        0 for group, 1 for transaction. Defaults to group.
        Only supported by version 1 and up

        :return int: the acting coordinator broker id
        """

    async def list_consumer_group_offsets(
        self, group_id: str, group_coordinator_id: int | None = ..., partitions: list[TopicPartition] | None = ...
    ) -> dict[TopicPartition, OffsetAndMetadata]:
        """Fetch Consumer Offsets for a single consumer group.

        Note:
        This does not verify that the group_id or partitions actually exist
        in the cluster.

        As soon as any error is encountered, it is immediately raised.

        :param group_id: The consumer group id name for which to fetch offsets.
        :param group_coordinator_id: The node_id of the group's coordinator
            broker. If set to None, will query the cluster to find the group
            coordinator. Explicitly specifying this can be useful to prevent
            that extra network round trip if you already know the group
            coordinator. Default: None.
        :param partitions: A list of TopicPartitions for which to fetch
            offsets. On brokers >= 0.10.2, this can be set to None to fetch all
            known offsets for the consumer group. Default: None.
        :return dictionary: A dictionary with TopicPartition keys and
            OffsetAndMetada values. Partitions that are not specified and for
            which the group_id does not have a recorded offset are omitted. An
            offset value of `-1` indicates the group_id has no offset for that
            TopicPartition. A `-1` can only happen for partitions that are
            explicitly specified.

        """

    async def delete_records(
        self, records_to_delete: dict[TopicPartition, RecordsToDelete], timeout_ms: int | None = ...
    ) -> dict[TopicPartition, int]:
        """Delete records from partitions.

        :param records_to_delete: A map of RecordsToDelete for each TopicPartition
        :param timeout_ms: Milliseconds to wait for the deletion to complete.
        :return: Appropriate version of DeleteRecordsResponse class.
        """
