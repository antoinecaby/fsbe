from typing import List
from sqlmodel import SQLModel, Field, Relationship

class Company(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    address: str
    users: "List[User]" = Relationship(back_populates="company")

    @classmethod
    def get_company(cls, session, company_id: int):
        return session.query(cls).filter(cls.id == company_id).first()

    @classmethod
    def get_companies(cls, session):
        return session.query(cls).all()
