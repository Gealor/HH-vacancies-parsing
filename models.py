from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class SalaryInfo(BaseModel):
    from_: Optional[int] = Field(default=None, alias='from')
    to: Optional[int] = Field(default=None)
    currency: Optional[str] = Field(default=None)
    gross: Optional[bool] = Field(default=None)


class VacancyData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str
    salary: Optional[SalaryInfo]
    url: str = Field(alias="alternate_url")

