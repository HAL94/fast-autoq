from decimal import Decimal, ROUND_HALF_UP
from pydantic import field_validator

class TwoDecimalPlacesMixin:
    @classmethod
    def configure_model(cls, config: dict) -> dict:
        config.setdefault('arbitrary_types_allowed', True)
        return config

    @field_validator('*')
    def validate_decimal_places(cls, value, field):
        if field.name in cls.__fields__:
            field_config = cls.__fields__[field.name]
            if 'two_decimal_places' in field_config.field_info.extra:
                if isinstance(value, (int, float)):
                    return Decimal(str(value)).quantize(Decimal('.01'), rounding=ROUND_HALF_UP)
        return value