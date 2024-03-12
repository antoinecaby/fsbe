# router/companies_router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db, get_session
from internal.auth import get_decoded_token
from model.models import Company
from model.schemas import CompanyCreate
from Security.SecurityManager import SecurityManager

router = APIRouter()
SECRET_KEY = "4gN94qiDdlB3bnlYVeHBaIPTGPgOildOrxnrPaKYSQM="
security_manager = SecurityManager(SECRET_KEY)

# CRUD operations for Companys

@router.post("/companies", response_model=Company)
def create_company(company: CompanyCreate, token: str = Depends(get_decoded_token), session: Session = Depends(get_db)):
    """
    Create a new company.
    """
    db_company = Company(**company.dict())
    session.add(db_company)
    session.commit()
    session.refresh(db_company)
    return db_company

@router.get("/companies", response_model=List[Company])
def get_companies(token: str = Depends(get_decoded_token),skip: int = 0, limit: int = 10, session: Session = Depends(get_db)):
    """
    Get all companies.
    """
    companies = session.query(Company).offset(skip).limit(limit).all()
    return companies

@router.get("/companies/{company_id}", response_model=Company)
def get_company(company_id: int, token: str = Depends(get_decoded_token),session: Session = Depends(get_session)):
    """
    Get a specific company by ID.
    """
    company = session.get(Company, company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.put("/companies/{company_id}", response_model=Company)
def update_company(company_id: int, company_update: CompanyCreate, token: str = Depends(get_decoded_token), session: Session = Depends(get_db)):
    """
    Update a company by ID.
    """
    db_company = session.get(Company, company_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    for var, value in vars(company_update).items():
        setattr(db_company, var, value)
    session.add(db_company)
    session.commit()
    session.refresh(db_company)
    return db_company

@router.delete("/companies/{company_id}", response_model=Company)
def delete_company(company_id: int,token: str = Depends(get_decoded_token),session: Session = Depends(get_db)):
    """
    Delete a company by ID.
    """
    company = session.get(Company, company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    session.delete(company)
    session.commit()
    return company
