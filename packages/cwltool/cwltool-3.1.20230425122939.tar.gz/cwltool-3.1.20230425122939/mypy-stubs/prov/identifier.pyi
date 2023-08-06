from typing import Any, Union

class Identifier:
    def __init__(self, uri: str) -> None: ...
    @property
    def uri(self) -> str: ...
    def __eq__(self, other: Any) -> bool: ...
    def __hash__(self) -> int: ...
    def provn_representation(self) -> str: ...

class QualifiedName(Identifier):
    def __init__(self, namespace: str, localpart: str) -> None: ...
    @property
    def namespace(self) -> str: ...
    @property
    def localpart(self) -> str: ...
    def __hash__(self) -> int: ...
    def provn_representation(self) -> str: ...

class Namespace:
    def __init__(self, prefix: str, uri: str) -> None: ...
    @property
    def uri(self) -> str: ...
    @property
    def prefix(self) -> str: ...
    def contains(self, identifier: Union[Identifier, str]) -> bool: ...
    def qname(self, identifier: Union[Identifier, str]) -> QualifiedName: ...
    def __eq__(self, other: Any) -> bool: ...
    def __ne__(self, other: Any) -> bool: ...
    def __hash__(self) -> int: ...
    def __getitem__(self, localpart: str) -> QualifiedName: ...
