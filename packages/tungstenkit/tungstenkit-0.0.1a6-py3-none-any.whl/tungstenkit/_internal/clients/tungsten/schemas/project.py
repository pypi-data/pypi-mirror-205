from typing import Optional

from pydantic import BaseModel


class Project(BaseModel):
    id: int
    slug: str
    display_name: str
    description: Optional[str] = None
