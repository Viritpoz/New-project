from pydantic import BaseModel

class SNMPData(BaseModel):
    time: str
    student: str  # e.g., "653xxxxx"
    type: str  # e.g., "MFUconnect"
    macAccespoint: str

