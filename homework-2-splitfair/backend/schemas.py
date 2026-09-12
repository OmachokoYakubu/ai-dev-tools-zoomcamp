from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

class MemberBase(BaseModel):
    name: str
    email: str

class MemberCreate(MemberBase):
    pass

class MemberOut(MemberBase):
    id: int
    group_id: int
    model_config = ConfigDict(from_attributes=True)

class GroupBase(BaseModel):
    title: str
    description: Optional[str] = ""
    currency: Optional[str] = "USD"

class GroupCreate(GroupBase):
    pass

class GroupOut(GroupBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class GroupDetailOut(GroupOut):
    members: List[MemberOut] = []

class ExpenseCreate(BaseModel):
    title: str
    amount: float = Field(gt=0)
    category: Optional[str] = "General"
    payer_id: int
    split_member_ids: List[int]

class ExpenseOut(BaseModel):
    id: int
    group_id: int
    title: str
    amount: float
    category: str
    payer_id: int
    payer_name: Optional[str] = None
    split_member_ids: List[int] = []
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class MemberBalance(BaseModel):
    member_id: int
    member_name: str
    paid: float
    share: float
    net_balance: float

class SettlementRecommendation(BaseModel):
    from_member_id: int
    from_member_name: str
    to_member_id: int
    to_member_name: str
    amount: float

class BalanceReport(BaseModel):
    balances: List[MemberBalance]
    settlements: List[SettlementRecommendation]

class SettlementCreate(BaseModel):
    from_member_id: int
    to_member_id: int
    amount: float = Field(gt=0)

class SettlementOut(BaseModel):
    id: int
    group_id: int
    from_member_id: int
    to_member_id: int
    amount: float
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
