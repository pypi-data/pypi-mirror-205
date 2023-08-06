from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class ImageInfo:
    Id: str
    ParentId: str
    Created: int
    Size: int
    VirtualSize: int
    SharedSize: int
    Labels: Dict[str, str]
    Containers: int
    RepoTags: Optional[List[str]] = None
    RepoDigests: Optional[List[str]] = None
