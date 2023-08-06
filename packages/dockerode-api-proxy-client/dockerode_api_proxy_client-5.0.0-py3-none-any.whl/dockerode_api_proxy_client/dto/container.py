from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union


@dataclass
class Port:
    IP: str
    PrivatePort: int
    PublicPort: int
    Type: str


@dataclass
class NetworkInfo:
    Links: Any
    Aliases: Any
    NetworkID: str
    EndpointID: str
    Gateway: str
    IPAddress: str
    IPPrefixLen: int
    IPv6Gateway: str
    GlobalIPv6Address: str
    GlobalIPv6PrefixLen: int
    MacAddress: str
    IPAMConfig: Optional[Any] = None


@dataclass
class Mount:
    Type: str
    Source: str
    Destination: str
    Mode: str
    RW: bool
    Propagation: str
    Driver: Optional[str] = None
    Name: Optional[str] = None


@dataclass
class ContainerInfo:
    Id: str
    Names: List[str]
    Image: str
    ImageID: str
    Command: str
    Created: int
    Ports: List[Port]
    Labels: Dict[str, str]
    State: str
    Status: str
    HostConfig: Dict[str, str]
    NetworkSettings: Dict[str, Dict[str, NetworkInfo]]
    Mounts: List[Mount]


@dataclass
class ContainerInspectInfo:
    Id: str
    Created: str
    Path: str
    Args: List[str]
    State: Dict[
        str, Union[str, Dict[str, Union[str, int, List[Dict[str, Union[str, int]]]]]]
    ]
    Image: str
    ResolvConfPath: str
    HostnamePath: str
    HostsPath: str
    LogPath: str
    Name: str
    RestartCount: int
    Driver: str
    Platform: str
    MountLabel: str
    ProcessLabel: str
    AppArmorProfile: str
    HostConfig: Dict[str, Any]
    GraphDriver: Dict[str, Union[str, Dict[str, str]]]
    Mounts: List[Dict[str, Union[str, bool, Optional[str]]]]
    Config: Dict[str, Union[str, bool, List[str], Dict[str, str], Optional[Any]]]
    NetworkSettings: Dict[str, Union[str, bool, int, Dict[str, List[Dict[str, str]]]]]
    ExecIDs: Optional[List[str]] = None
