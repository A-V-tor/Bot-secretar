from aiogram.types import Message
from aiogram.types.update import Update
from pydantic import ConfigDict


class MessageCustom(Message):
    model_config = ConfigDict(
        use_enum_values=True,
        extra='allow',
        validate_assignment=True,
        frozen=False,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        defer_build=True,
    )


class UpdateCustom(Update):
    model_config = ConfigDict(
        use_enum_values=True,
        extra='allow',
        validate_assignment=True,
        frozen=False,
        populate_by_name=True,
        arbitrary_types_allowed=True,
        defer_build=True,
    )
