from pydantic import BaseModel, Field


class URLSchema(BaseModel):
    url: str = Field(None, description="URL user wants to shorten")


