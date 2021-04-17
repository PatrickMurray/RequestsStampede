"""
All internal exceptions within the RequestStampede package.
"""


import schema


class InvalidRetryConfigFile(Exception):
    """
    Thrown when a retry configuration file's structure or contents are not
    valid.
    """

    def __init__(self, path: str, schema_error: schema.SchemaError):
        """
        TODO
        """
        super().__init__(
            f"Invalid retry configuration file: { path }, { schema_error }"
        )


class InvalidCustomRetryPolicy(Exception):
    """
    TODO
    """

    def __init__(self, policy_type: str):
        """
        TODO
        """
        super().__init__(f"Invalid retry policy type: { policy_type }")


class InvalidCustomBackoffPolicy(Exception):
    """
    TODO
    """

    def __init__(self, policy_type: str):
        """
        TODO
        """
        super().__init__(f"Invalid retry policy type: { policy_type }")


class UnsuccessfulRequestAttemptException(Exception):
    """
    Thrown when a RequestAttempt execution is unsuccessful.
    """
