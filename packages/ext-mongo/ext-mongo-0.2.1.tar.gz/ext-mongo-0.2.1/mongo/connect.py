from .deps import me


def connect(
    db: str,
    host: str | None = None,
    password: str | None = None,
    user: str | None = None,
    port: int | None = None,
    timeout: int = 3,
) -> None:
    if password and user is None:
        user = "root"
    me.connect(
        db=db,
        host=host,
        username=user,
        password=password,
        port=port,
        serverSelectionTimeoutMS=timeout * 1000,
    )
