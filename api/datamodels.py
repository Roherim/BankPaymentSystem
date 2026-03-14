from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional
import re
import uuid


class OrderStatus(BaseModel):
    id:int
    name: str

class PaymentStatus(BaseModel):
    id:int
    name: str

class PaymentType(BaseModel):
    id:int
    name: str

class PaymentStatus(BaseModel):
    id:int
    name: str

class Order(BaseModel):
    id: uuid
    amount: float
    order_date: datetime
    status_id: int
    customer_id: str
    created_at: datetime
    updated_at: datetime
    
class Payment(BaseModel):
    id: uuid
    order_id: uuid
    payment_type_id: int
    amount: float
    payment_date: datetime
    status_id: int
    external_id: str
    created_at: datetime
    updated_at: datetime

class CreateBankPaymentRequest(BaseModel):
    order_id: uuid
    amount: float

class CreateBankPaymentResponse(BaseModel):
    payment_id: uuid
    external_id: str

class CheckBankPaymentRequest(BaseModel):
    payment_id: uuid

class CheckBankPaymentResponse(BaseModel):
    payment_id: str
    status_id: int
    amount: float
    payment_date: datetime
    