"""
This type stub file was generated by pyright.
"""

log = ...

class KafkaAdminClient:
    """A class for administering the Kafka cluster.

    Warning:
        This is an unstable interface that was recently added and is subject to
        change without warning. In particular, many methods currently return
        raw protocol tuples. In future releases, we plan to make these into
        nicer, more pythonic objects. Unfortunately, this will likely break
        those interfaces.

    The KafkaAdminClient class will negotiate for the latest version of each message
    protocol format supported by both the kafka-python client library and the
    Kafka broker. Usage of optional fields from protocol versions that are not
    supported by the broker will result in IncompatibleBrokerVersion exceptions.

    Use of this class requires a minimum broker version >= 0.10.0.0.

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
            consumer group administration. Default: 'kafka-python-{version}'
        reconnect_backoff_ms (int): The amount of time in milliseconds to
            wait before attempting to reconnect to a given host.
            Default: 50.
        reconnect_backoff_max_ms (int): The maximum amount of time in
            milliseconds to backoff/wait when reconnecting to a broker that has
            repeatedly failed to connect. If provided, the backoff per host
            will increase exponentially for each consecutive connection
            failure, up to this maximum. Once the maximum is reached,
            reconnection attempts will continue periodically with this fixed
            rate. To avoid connection storms, a randomization factor of 0.2
            will be applied to the backoff resulting in a random range between
            20% below and 20% above the computed value. Default: 1000.
        request_timeout_ms (int): Client request timeout in milliseconds.
            Default: 30000.
        connections_max_idle_ms: Close idle connections after the number of
            milliseconds specified by this config. The broker closes idle
            connections after connections.max.idle.ms, so this avoids hitting
            unexpected socket disconnected errors on the client.
            Default: 540000
        retry_backoff_ms (int): Milliseconds to backoff when retrying on
            errors. Default: 100.
        max_in_flight_requests_per_connection (int): Requests are pipelined
            to kafka brokers up to this number of maximum requests per
            broker connection. Default: 5.
        receive_buffer_bytes (int): The size of the TCP receive buffer
            (SO_RCVBUF) to use when reading data. Default: None (relies on
            system defaults). Java client defaults to 32768.
        send_buffer_bytes (int): The size of the TCP send buffer
            (SO_SNDBUF) to use when sending data. Default: None (relies on
            system defaults). Java client defaults to 131072.
        socket_options (list): List of tuple-arguments to socket.setsockopt
            to apply to broker connection sockets. Default:
            [(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)]
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
        ssl_check_hostname (bool): Flag to configure whether SSL handshake
            should verify that the certificate matches the broker's hostname.
            Default: True.
        ssl_cafile (str): Optional filename of CA file to use in certificate
            verification. Default: None.
        ssl_certfile (str): Optional filename of file in PEM format containing
            the client certificate, as well as any CA certificates needed to
            establish the certificate's authenticity. Default: None.
        ssl_keyfile (str): Optional filename containing the client private key.
            Default: None.
        ssl_password (str): Optional password to be used when loading the
            certificate chain. Default: None.
        ssl_crlfile (str): Optional filename containing the CRL to check for
            certificate expiration. By default, no CRL check is done. When
            providing a file, only the leaf certificate will be checked against
            this CRL. The CRL can only be checked with Python 3.4+ or 2.7.9+.
            Default: None.
        api_version (tuple): Specify which Kafka API version to use. If set
            to None, KafkaClient will attempt to infer the broker version by
            probing various APIs. Example: (0, 10, 2). Default: None
        api_version_auto_timeout_ms (int): number of milliseconds to throw a
            timeout exception from the constructor when checking the broker
            api version. Only applies if api_version is None
        selector (selectors.BaseSelector): Provide a specific selector
            implementation to use for I/O multiplexing.
            Default: selectors.DefaultSelector
        metrics (kafka.metrics.Metrics): Optionally provide a metrics
            instance for capturing network IO stats. Default: None.
        metric_group_prefix (str): Prefix for metric names. Default: ''
        sasl_mechanism (str): Authentication mechanism when security_protocol
            is configured for SASL_PLAINTEXT or SASL_SSL. Valid values are:
            PLAIN, GSSAPI, OAUTHBEARER, SCRAM-SHA-256, SCRAM-SHA-512.
        sasl_plain_username (str): username for sasl PLAIN and SCRAM authentication.
            Required if sasl_mechanism is PLAIN or one of the SCRAM mechanisms.
        sasl_plain_password (str): password for sasl PLAIN and SCRAM authentication.
            Required if sasl_mechanism is PLAIN or one of the SCRAM mechanisms.
        sasl_kerberos_service_name (str): Service name to include in GSSAPI
            sasl mechanism handshake. Default: 'kafka'
        sasl_kerberos_domain_name (str): kerberos domain name to use in GSSAPI
            sasl mechanism handshake. Default: one of bootstrap servers
        sasl_oauth_token_provider (AbstractTokenProvider): OAuthBearer token provider
            instance. (See kafka.oauth.abstract). Default: None
        kafka_client (callable): Custom class / callable for creating KafkaClient instances

    """

    DEFAULT_CONFIG = ...
    def __init__(self, **configs) -> None: ...
    def close(self):  # -> None:
        """Close the KafkaAdminClient connection to the Kafka broker."""

    def create_topics(self, new_topics, timeout_ms=..., validate_only=...):  # -> None:
        """Create new topics in the cluster.

        :param new_topics: A list of NewTopic objects.
        :param timeout_ms: Milliseconds to wait for new topics to be created
            before the broker returns.
        :param validate_only: If True, don't actually create new topics.
            Not supported by all versions. Default: False
        :return: Appropriate version of CreateTopicResponse class.
        """

    def delete_topics(self, topics, timeout_ms=...):  # -> None:
        """Delete topics from the cluster.

        :param topics: A list of topic name strings.
        :param timeout_ms: Milliseconds to wait for topics to be deleted
            before the broker returns.
        :return: Appropriate version of DeleteTopicsResponse class.
        """

    def list_topics(self):  # -> list[Any]:
        ...
    def describe_topics(self, topics=...): ...
    def describe_cluster(self): ...
    def describe_acls(self, acl_filter):  # -> tuple[list[Any], type[BrokerResponseError]]:
        """Describe a set of ACLs

        Used to return a set of ACLs matching the supplied ACLFilter.
        The cluster must be configured with an authorizer for this to work, or
        you will get a SecurityDisabledError

        :param acl_filter: an ACLFilter object
        :return: tuple of a list of matching ACL objects and a KafkaError (NoError if successful)
        """

    def create_acls(self, acls):  # -> dict[str, list[Any]]:
        """Create a list of ACLs

        This endpoint only accepts a list of concrete ACL objects, no ACLFilters.
        Throws TopicAlreadyExistsError if topic is already present.

        :param acls: a list of ACL objects
        :return: dict of successes and failures
        """

    def delete_acls(self, acl_filters):  # -> list[Any]:
        """Delete a set of ACLs

        Deletes all ACLs matching the list of input ACLFilter

        :param acl_filters: a list of ACLFilter
        :return: a list of 3-tuples corresponding to the list of input filters.
                 The tuples hold (the input ACLFilter, list of affected ACLs, KafkaError instance)
        """

    def describe_configs(self, config_resources, include_synonyms=...):  # -> list[Any]:
        """Fetch configuration parameters for one or more Kafka resources.

        :param config_resources: An list of ConfigResource objects.
            Any keys in ConfigResource.configs dict will be used to filter the
            result. Setting the configs dict to None will get all values. An
            empty dict will get zero values (as per Kafka protocol).
        :param include_synonyms: If True, return synonyms in response. Not
            supported by all versions. Default: False.
        :return: Appropriate version of DescribeConfigsResponse class.
        """

    def alter_configs(self, config_resources):  # -> None:
        """Alter configuration parameters of one or more Kafka resources.

        Warning:
            This is currently broken for BROKER resources because those must be
            sent to that specific broker, versus this always picks the
            least-loaded node. See the comment in the source code for details.
            We would happily accept a PR fixing this.

        :param config_resources: A list of ConfigResource objects.
        :return: Appropriate version of AlterConfigsResponse class.

        """

    def create_partitions(self, topic_partitions, timeout_ms=..., validate_only=...):  # -> None:
        """Create additional partitions for an existing topic.

        :param topic_partitions: A map of topic name strings to NewPartition objects.
        :param timeout_ms: Milliseconds to wait for new partitions to be
            created before the broker returns.
        :param validate_only: If True, don't actually create new partitions.
            Default: False
        :return: Appropriate version of CreatePartitionsResponse class.
        """

    def describe_consumer_groups(
        self, group_ids, group_coordinator_id=..., include_authorized_operations=...
    ):  # -> list[Any]:
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
            are the raw results from the DescribeGroupsResponse. Long-term, we
            plan to change this to return namedtuples as well as decoding the
            partition assignments.
        """

    def list_consumer_groups(self, broker_ids=...):  # -> list[Any]:
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

    def list_consumer_group_offsets(self, group_id, group_coordinator_id=..., partitions=...):  # -> dict[Any, Any]:
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

    def delete_consumer_groups(self, group_ids, group_coordinator_id=...):  # -> list[Any]:
        """Delete Consumer Group Offsets for given consumer groups.

        Note:
        This does not verify that the group ids actually exist and
        group_coordinator_id is the correct coordinator for all these groups.

        The result needs checking for potential errors.

        :param group_ids: The consumer group ids of the groups which are to be deleted.
        :param group_coordinator_id: The node_id of the broker which is the coordinator for
            all the groups. Use only if all groups are coordinated by the same broker.
            If set to None, will query the cluster to find the coordinator for every single group.
            Explicitly specifying this can be useful to prevent
            that extra network round trips if you already know the group
            coordinator. Default: None.
        :return: A list of tuples (group_id, KafkaError)

        """
