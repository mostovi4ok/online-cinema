"""
This type stub file was generated by pyright.
"""

class Result:
    """
    Represents the result of a search query, and has an array of Document
    objects
    """

    def __init__(
        self, res, hascontent, duration=..., has_payload=..., with_scores=..., field_encodings: dict | None = ...
    ) -> None:
        """
        - duration: the execution time of the query
        - has_payload: whether the query has payloads
        - with_scores: whether the query has scores
        - field_encodings: a dictionary of field encodings if any is provided
        """
