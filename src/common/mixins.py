from typing import Annotated, Union

from pydantic import AfterValidator

def decimals_normalize(value: Union[float, int]) -> float:
    return round(float(value), 2)


TruncatedFloat = Annotated[
    float,
    AfterValidator(lambda x: round(x, 2)),
]