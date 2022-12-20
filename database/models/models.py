from decimal import Decimal
from datetime import datetime
from sqlalchemy import Numeric, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional, Union
from dataclasses import dataclass

from database.database import Base

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password: Mapped[str] = mapped_column(String)
    cash: Mapped[Decimal] = mapped_column(Numeric, default=10000.00)
    
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    
    def __init__(self, email: str, password: str):
        self.id
        self.email = email
        self.password = password
        self.cash
            
    # def __repr__(self) -> str:
    #     return f"User(id={self.id!r}, email={self.email!r}, cash={self.cash!r})" # f"Email: {self.email} \nPassword: {self.password}"
    
    # def to_dict(self):
    #     return vars(self)
    
class Transaction(Base):
    __tablename__ = "transactions"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    date: Mapped[datetime] = mapped_column(DateTime)
    transaction_type: Mapped[str] = mapped_column(String)
    ticker: Mapped[str] = mapped_column(String)
    shares: Mapped[int] = mapped_column(Integer)
    share_price: Mapped[Decimal] = mapped_column(Numeric)
    total_price: Mapped[Decimal] = mapped_column(Numeric)
    cash_balance: Mapped[Decimal] = mapped_column(Numeric)
    person_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    user: Mapped["User"] = relationship(back_populates="transactions")
    
    def __init__(self, 
            date: datetime, transaction_type: str, ticker: str, shares: int,
            share_price: Union[Decimal, float] , cash_balance: Union[Decimal, float], person_id: int):
        self.date = date
        self.transaction_type = transaction_type
        self.ticker = ticker
        self.shares = shares
        self.share_price = Decimal(share_price)
        self.cash_balance = Decimal(cash_balance)
        self.person_id = person_id
        
        self.total_price = Decimal(self.shares * self.share_price)
        
        
    def __repr__(self) -> str:
        return f"{self.person_id} bought {self.shares} {'share' if self.shares == 1 else 'shares'} on {self.date.date()} for a price of ${self.share_price} per share, totalling ${self.total_price}"
    
