from datetime import datetime, timedelta, timezone

import settings


def opt_in_expiration_date(offset_minutes: int = 0):
    return datetime.now(timezone.utc) - timedelta(
        minutes=settings.OPT_IN_RETRY_TIMEOUT + offset_minutes
    )
