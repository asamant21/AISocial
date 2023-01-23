"""Base Class for an Image Post."""
import urllib.request
from typing import Any, Optional

from IPython.display import display
from PIL import Image
from pydantic import BaseModel, Extra

from aisocial.Post.base import BasePost, ContentType


class ImagePost(BasePost, BaseModel):

    prompt: str

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    def content_type(self) -> ContentType:
        """Return Content Type."""
        return ContentType.IMAGE

    def show(self) -> None:
        """Show post."""
        super().show()
        post_name = f"data/{self.post_id}.png"
        urllib.request.urlretrieve(self.content, post_name)
        img = Image.open(post_name)
        display(img)
