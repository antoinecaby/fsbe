from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlmodel import select
from database import get_session
from model.models import Company
from schemas import CompanyCreate

router = APIRouter()


class CompaniesRouter:
    @router.post("/companies/", response_model=Company)
    def create_company(self, company: CompanyCreate, session: Session = Depends(get_session)):
        """
        Create a new company.
        """
        # Implementation

    @router.get("/companies/", response_model=List[Company])
    def get_companies(self, skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
        """
        Get all companies.
        """
        # Implementation

    @router.get("/companies/{company_id}", response_model=Company)
    def get_company(self, company_id: int, session: Session = Depends(get_session)):
        """
        Get a specific company by ID.
        """
        # Implementation

    @router.put("/companies/{company_id}", response_model=Company)
    def update_company(self, company_id: int, company_update: CompanyCreate, session: Session = Depends(get_session)):
        """
        Update a company by ID.
        """
        # Implementation

    @router.delete("/companies/{company_id}", response_model=Company)
    def delete_company(self, company_id: int, session: Session = Depends(get_session)):
        """
        Delete a company by ID.
        """
        # Implementation
