from gql.transport.exceptions import TransportQueryError
import typing


class UserIsPrivate(TransportQueryError):
    
    def __init__(self, player: typing.Optional[str] = None, query_id: typing.Optional[int] = None, errors:  typing.Optional[typing.List[typing.Any]] = None, data: typing.Optional[typing.Any] = None, extensions: typing.Optional[typing.Any] = None):
        if player:
            msg = f"{player} Eva profile is set to private! It must be public."
        else:
            msg = "The user's Eva profile is set to private! It must be public."
        super().__init__(msg, query_id, errors, data, extensions)


class UserNotFound(TransportQueryError):
    
    def __init__(self, player: typing.Optional[str] = None, query_id: typing.Optional[int] = None, errors:  typing.Optional[typing.List[typing.Any]] = None, data: typing.Optional[typing.Any] = None, extensions: typing.Optional[typing.Any] = None):
        if player:
            msg = f"Player {player} doesn't exists."
        else:
            msg = "Player Eva doesn't exists."
        super().__init__(msg, query_id, errors, data, extensions)
