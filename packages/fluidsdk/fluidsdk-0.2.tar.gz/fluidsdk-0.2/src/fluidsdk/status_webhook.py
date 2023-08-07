from typing import TYPE_CHECKING, Dict

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from dataclasses import dataclass as _basemodel_decorator
else:
    _basemodel_decorator = lambda x: x


@_basemodel_decorator
class StatusWebhook(BaseModel):
    url: str = Field(
        None, title="Webhook URL", description="URL of the endpoint to push data to."
    )
    data: Dict[str, str] = Field(
        {},
        title="Data",
        description="Key value pairs of data to push, along with the dashboard status.",
    )


@_basemodel_decorator
class StatusIntentData(BaseModel):
    status: str = Field(
        None,
        title="Status",
        description="Status to be set.",
    )
    data: Dict[str, str] = Field(
        {},
        title="Data",
        description="Key value pairs of data to push, along with the dashboard status.",
    )
