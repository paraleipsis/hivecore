from pydantic import Field
from typing import Generic, TypeVar, Optional
from pydantic.generics import GenericModel

DataT = TypeVar('DataT')


class GenericResponseModel(GenericModel, Generic[DataT]):
    success: bool = Field(True)
    error_msg: Optional[str] = Field(None, alias='errorMsg')
    data: Optional[DataT] = Field(None)
    total: Optional[int] = Field(None)

    class Config:
        allow_population_by_field_name = True
