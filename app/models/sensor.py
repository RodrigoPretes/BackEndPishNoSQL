from pydantic import BaseModel, Field
from datetime import datetime
from uuid import uuid4

def generate_id():
    return str(uuid4())

def generate_date():
    return str(datetime.now())

class Sensor(BaseModel):
    id: str = Field(default_factory=generate_id)
    sensor: str
    created_at: str = Field(default_factory=generate_date)
    updated_at: str = Field(default_factory=generate_date)

class GetSensor(BaseModel):
    sensor: str
    

