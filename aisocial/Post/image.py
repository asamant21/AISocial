"""Base Class for an Image Post."""
from pydantic import BaseModel, Extra
import urllib.request
from PIL import Image
from aisocial.Post.base import BasePost, ContentType
from IPython.display import display


class ImagePost(BasePost, BaseModel):
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


