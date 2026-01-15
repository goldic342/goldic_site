from datetime import datetime, timezone


def last_build(posts: list, time_format: str) -> str:
    if posts:
        last_build = posts[0].get("publish_date")
    else:
        last_build = datetime.now(timezone.utc).strftime(time_format)

    return last_build
