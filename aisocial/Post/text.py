"""Base Class for a Text Post."""
from pydantic import BaseModel, Extra
from aisocial.Post.base import BasePost, ContentType


class TextPost(BasePost, BaseModel):
    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    def content_type(self) -> ContentType:
        """Return Content Type."""
        return ContentType.TEXT

    def show(self) -> None:
        """Show post."""
        super().show()
        print(self.content)