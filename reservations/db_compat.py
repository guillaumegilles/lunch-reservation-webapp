def is_missing_column_error(error, column_name):
    message = str(error).lower()
    normalized_column = column_name.lower()
    return normalized_column in message and (
        "does not exist" in message or "no such column" in message or "unknown column" in message
    )
