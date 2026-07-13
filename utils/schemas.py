from pydantic import BaseModel


class ChartType(BaseModel):
    chart_type: str