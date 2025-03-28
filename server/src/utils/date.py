from datetime import datetime, timedelta

def get_yesterday() -> str:
    """Get date of yesterday."""
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
