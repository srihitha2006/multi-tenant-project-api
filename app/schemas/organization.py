from pydantic import BaseModel

# Used when creating an organization (POST request)
class OrganizationCreate(BaseModel):
    name: str


# Used when sending response back to client
class OrganizationResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True  # IMPORTANT for SQLAlchemy
