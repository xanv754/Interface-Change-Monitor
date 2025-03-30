def format_ifStatus(value: str) -> str:
    """Format the ifAdminStatus or ifOperStatus of the interface."""
    if "(" in value:
        value = value.split("(")[0].strip()
    value = value.upper()
    return value
