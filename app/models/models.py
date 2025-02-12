from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class User(BaseModel):
    UserID: Optional[int]
    UserName: str
    Email: str
    PasswordHash: str
    CreatedAt: Optional[datetime]

class Wallet(BaseModel):
    WalletID: Optional[int]
    UserID: int
    Balance: float
    Currency: str
    CreatedAt: Optional[datetime]

class Transaction(BaseModel):
    TransactionID: Optional[int]
    WalletID: int
    Amount: float
    TransactionType: str
    Timestamp: Optional[datetime]

class PaymentMethod(BaseModel):
    PaymentMethodID: Optional[int]
    UserID: int
    MethodName: str
    AccountNumber: str
    ExpiryDate: datetime
    IsDefault: Optional[bool]
    CreatedAt: Optional[datetime]

class TransactionCategory(BaseModel):
    CategoryID: Optional[int]
    CategoryName: str
    Description: Optional[str]
    CreatedAt: Optional[datetime]

class TransactionDetail(BaseModel):
    DetailID: Optional[int]
    TransactionID: int
    CategoryID: int
    SubAmount: float
    Note: Optional[str]
    CreatedAt: Optional[datetime]

# Agregar los otros modelos aquí