from typing import TypedDict, List, Optional, TypeVar, Generic


PageResult = TypeVar("PageResult")


class Page(TypedDict, Generic[PageResult]):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[PageResult]


class MeData(TypedDict):
    i2a_user_id: int
    i2a_identifier: str
    username: str
    login_email: str
    email: str
    first_name: str
    last_name: str


class TokenData(TypedDict):
    access_token: str
    expires_in: int
    token_type: str
    scope: str
    refresh_token: str


class AppLessS2SAppUserRepresentation(TypedDict):
    email: str
    i2a_identifier: str
    application_name: str
    application_client_id: str
    application_user_group_identifier: str
    application_user_group_name: str


class AppLessS2SI2IdentityData(TypedDict):
    app_users: List[AppLessS2SAppUserRepresentation]
    username: str
    first_name: str
    last_name: str
    email: str
