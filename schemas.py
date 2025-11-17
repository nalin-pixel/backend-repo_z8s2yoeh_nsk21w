"""
Database Schemas for Ruralytics

Each Pydantic model represents a collection in MongoDB. The collection name is the lowercase
of the class name.
"""
from pydantic import BaseModel, Field
from typing import Optional, List

class Panchayat(BaseModel):
    panchayat_id: str = Field(..., description="Unique Panchayat identifier")
    name: str = Field(..., description="Panchayat name")
    district: Optional[str] = Field(None, description="District name")
    state: Optional[str] = Field(None, description="State name")

class MetricHighlights(BaseModel):
    key: str
    value: float
    unit: Optional[str] = None

class EducationMetrics(BaseModel):
    enrollment_rate: float = Field(..., ge=0, le=100)
    literacy_rate: float = Field(..., ge=0, le=100)
    dropout_rate: float = Field(..., ge=0, le=100)
    highlights: Optional[List[MetricHighlights]] = None

class HealthcareMetrics(BaseModel):
    immunization_rate: float = Field(..., ge=0, le=100)
    maternal_mortality: float = Field(..., ge=0)
    infant_mortality: float = Field(..., ge=0)
    highlights: Optional[List[MetricHighlights]] = None

class AgricultureMetrics(BaseModel):
    yield_index: float = Field(..., ge=0)
    irrigation_coverage: float = Field(..., ge=0, le=100)
    organic_adoption: float = Field(..., ge=0, le=100)
    highlights: Optional[List[MetricHighlights]] = None

class FundsMetrics(BaseModel):
    allocated: float = Field(..., ge=0)
    utilized: float = Field(..., ge=0)
    pending: float = Field(..., ge=0)
    highlights: Optional[List[MetricHighlights]] = None

class Funds(BaseModel):
    panchayat_id: str
    year: int
    allocated: float
    utilized: float
    pending: float

class Complaint(BaseModel):
    name: str
    description: str
    sdg_tag: str
    panchayat_id: str

class AnalysisItem(BaseModel):
    title: str
    points: List[str]
    sdg_tag: str

# Auth models (mock, for client-side auth flow only)
class SignupModel(BaseModel):
    name: str
    email: str
    password: str

class LoginModel(BaseModel):
    email: str
    password: str
