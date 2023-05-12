from uuid import UUID


def is_uuid(uuid: str) -> bool:
    try:
        UUID(uuid)
    except ValueError:
        return False
    return True


def title_to_lowercase(title: str) -> str:
    lowercase_title = title.lower()

    return lowercase_title
