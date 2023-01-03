from dataclasses import dataclass, field
import dataclasses

from typing import Dict, List, Optional

@dataclass
class Review:
    """Review dataclass"""
    author : str = field(default="")
    rating : str = field(default="")
    title : str = field(default="")
    place : str = field(default="")
    date : str = field(default="")
    specifications : Optional[Dict] = field(default=None)
    verified_purchase : bool = field(default=False)
    content : str = field(default="")


@dataclass
class Product:
    """Product dataclass"""
    name : str
    price : float
    rating : float = field(default=0.0)
    color : str = field(default="")
    size : str = field(default="")
    global_ratings : int = field(default=0)
    reviews : List[Review] = field(default_factory=list)

    def serialize(self):
        """Serialize product to dict"""
        return dataclasses.asdict(self)


