"""
This type stub file was generated by pyright.
"""

class Query:
    """
    Query is used to build complex queries that have more parameters than just
    the query string. The query string is set in the constructor, and other
    options have setter functions.

    The setter functions return the query object, so they can be chained,
    i.e. `Query("foo").verbatim().filter(...)` etc.
    """

    def __init__(self, query_string: str) -> None:
        """
        Create a new query object.
        The query string is set in the constructor, and other options have
        setter functions.
        """

    def query_string(self) -> str:
        """Return the query string of this query only."""

    def limit_ids(self, *ids) -> Query:
        """Limit the results to a specific set of pre-known document
        ids of any length.
        """

    def return_fields(self, *fields) -> Query:
        """Add fields to return fields."""

    def return_field(
        self,
        field: str,
        as_field: str | None = ...,
        decode_field: bool | None = ...,
        encoding: str | None = ...,
    ) -> Query:
        """
        Add a field to the list of fields to return.

        - **field**: The field to include in query results
        - **as_field**: The alias for the field
        - **decode_field**: Whether to decode the field from bytes to string
        - **encoding**: The encoding to use when decoding the field
        """

    def summarize(
        self,
        fields: list | None = ...,
        context_len: int | None = ...,
        num_frags: int | None = ...,
        sep: str | None = ...,
    ) -> Query:
        """
        Return an abridged format of the field, containing only the segments of
        the field which contain the matching term(s).

        If `fields` is specified, then only the mentioned fields are
        summarized; otherwise all results are summarized.

        Server side defaults are used for each option (except `fields`)
        if not specified

        - **fields** List of fields to summarize. All fields are summarized
        if not specified
        - **context_len** Amount of context to include with each fragment
        - **num_frags** Number of fragments per document
        - **sep** Separator string to separate fragments
        """

    def highlight(self, fields: list[str] | None = ..., tags: list[str] | None = ...) -> None:
        """
        Apply specified markup to matched term(s) within the returned field(s).

        - **fields** If specified then only those mentioned fields are
        highlighted, otherwise all fields are highlighted
        - **tags** A list of two strings to surround the match.
        """

    def language(self, language: str) -> Query:
        """
        Analyze the query as being in the specified language.

        :param language: The language (e.g. `chinese` or `english`)
        """

    def slop(self, slop: int) -> Query:
        """Allow a maximum of N intervening non matched terms between
        phrase terms (0 means exact phrase).
        """

    def timeout(self, timeout: float) -> Query:
        """Overrides the timeout parameter of the module"""

    def in_order(self) -> Query:
        """
        Match only documents where the query terms appear in
        the same order in the document.
        i.e. for the query "hello world", we do not match "world hello"
        """

    def scorer(self, scorer: str) -> Query:
        """
        Use a different scoring function to evaluate document relevance.
        Default is `TFIDF`.

        :param scorer: The scoring function to use
                       (e.g. `TFIDF.DOCNORM` or `BM25`)
        """

    def get_args(self) -> list[str]:
        """Format the redis arguments for this query and return them."""

    def paging(self, offset: int, num: int) -> Query:
        """
        Set the paging for the query (defaults to 0..10).

        - **offset**: Paging offset for the results. Defaults to 0
        - **num**: How many results do we want
        """

    def verbatim(self) -> Query:
        """Set the query to be verbatim, i.e. use no query expansion
        or stemming.
        """

    def no_content(self) -> Query:
        """Set the query to only return ids and not the document content."""

    def no_stopwords(self) -> Query:
        """
        Prevent the query from being filtered for stopwords.
        Only useful in very big queries that you are certain contain
        no stopwords.
        """

    def with_payloads(self) -> Query:
        """Ask the engine to return document payloads."""

    def with_scores(self) -> Query:
        """Ask the engine to return document search scores."""

    def limit_fields(self, *fields: list[str]) -> Query:
        """
        Limit the search to specific TEXT fields only.

        - **fields**: A list of strings, case sensitive field names
        from the defined schema.
        """

    def add_filter(self, flt: Filter) -> Query:
        """
        Add a numeric or geo filter to the query.
        **Currently only one of each filter is supported by the engine**

        - **flt**: A NumericFilter or GeoFilter object, used on a
        corresponding field
        """

    def sort_by(self, field: str, asc: bool = ...) -> Query:
        """
        Add a sortby field to the query.

        - **field** - the name of the field to sort by
        - **asc** - when `True`, sorting will be done in asceding order
        """

    def expander(self, expander: str) -> Query:
        """
        Add a expander field to the query.

        - **expander** - the name of the expander
        """

    def dialect(self, dialect: int) -> Query:
        """
        Add a dialect field to the query.

        - **dialect** - dialect version to execute the query under
        """

class Filter:
    def __init__(self, keyword: str, field: str, *args: list[str]) -> None: ...

class NumericFilter(Filter):
    INF = ...
    NEG_INF = ...
    def __init__(
        self,
        field: str,
        minval: int | str,
        maxval: int | str,
        minExclusive: bool = ...,
        maxExclusive: bool = ...,
    ) -> None: ...

class GeoFilter(Filter):
    METERS = ...
    KILOMETERS = ...
    FEET = ...
    MILES = ...
    def __init__(self, field: str, lon: float, lat: float, radius: float, unit: str = ...) -> None: ...

class SortbyField:
    def __init__(self, field: str, asc=...) -> None: ...
