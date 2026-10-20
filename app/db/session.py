import ssl
from collections.abc import Iterator
from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy.engine import Engine
from sqlmodel import Session, create_engine

from app.core.config import get_settings


def _build_ssl_context() -> ssl.SSLContext:
    # Azure MySQL only accepts encrypted connections. This checks the server's certificate and hostname.
    ctx = ssl.create_default_context(cafile=get_settings().db_ssl_ca or None)
    # Python 3.13+ adds extra-strict certificate rules that some real chains fail (PyMySQL relaxes this too).
    # the certificate chain and hostname are still verified.
    ctx.verify_flags &= ~ssl.VERIFY_X509_STRICT
    return ctx


# built on first use and then reused, so importing this file never touches the database
@lru_cache
def get_engine() -> Engine:
    return create_engine(
        get_settings().database_url,
        connect_args={"ssl": _build_ssl_context()},
        pool_pre_ping=True,  # test a pooled connection before using it, replace it if it was dropped
        pool_recycle=1800,  # retire connections after 30 min so idle ones Azure drops aren't reused
    )


def get_session() -> Iterator[Session]:
    # one session per request, closed automatically afterwards
    with Session(get_engine()) as session:
        yield session


# use in routes as: def my_route(session: SessionDep)
SessionDep = Annotated[Session, Depends(get_session)]
