# router/companies_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from db.database import get_db, get_session
from internal.auth import check_admin, get_decoded_token, check_company_access
from model.models import Company, User
from model.schemas import CompanyCreate
from Security.SecurityManager import SecurityManager

router = APIRouter()
SECRET_KEY = "4gN94qiDdlB3bnlYVeHBaIPTGPgOildOrxnrPaKYSQM="
security_manager = SecurityManager(SECRET_KEY)

# CRUD operations for Companies

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
def get_companies(token: str = Depends(get_decoded_token), session: Session = Depends(get_db)):
    """
    Get all companies.
    """
    companies = session.query(Company).all()
    return companies

@router.get("/companies/{company_id}", response_model=Company)
def get_company(company_id: int, token: str = Depends(get_decoded_token), session: Session = Depends(get_session)):
    """
    Get a specific company by ID.
    """
    company = session.get(Company, company_id)

    if check_admin(token, session):  # Check if the user is admin
       return company
    
    if not check_company_access(token, company_id, session):  # Check access
        raise HTTPException(status_code=403, detail="You do not have access to view this company")
    
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

    if check_admin(token, session):  # Check if the user is admin
        for var, value in vars(company_update).items():
            setattr(db_company, var, value)
        session.add(db_company)
        session.commit()
        session.refresh(db_company)
        return db_company

    if not check_company_access(token, company_id, session):  # Check access
        raise HTTPException(status_code=403, detail="You do not have access to update this company")
        
    for var, value in vars(company_update).items():
        setattr(db_company, var, value)
    session.add(db_company)
    session.commit()
    session.refresh(db_company)
    return db_company



@router.delete("/companies/{company_id}", response_model=Company)
def delete_company(company_id: int, token: str = Depends(get_decoded_token), session: Session = Depends(get_db)):
    """
    Delete a company by ID.
    """
    # Check if the user is an admin or has access to delete the company
    if check_admin(token, session) or check_company_access(token, company_id, session):
        # Execute the raw SQL delete query
        query = text("DELETE FROM company WHERE id = :company_id")
        session.execute(query, {"company_id": company_id})
        session.commit()

        # Return a message indicating successful deletion
        return {"message": "Company deleted successfully"}
    
    # If the user is not admin and does not have access, raise 403 Forbidden
    raise HTTPException(status_code=403, detail="You do not have access to delete this company")
