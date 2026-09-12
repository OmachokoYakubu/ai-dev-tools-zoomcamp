from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(500), default="")
    currency = Column(String(10), default="USD")
    created_at = Column(DateTime, default=datetime.utcnow)

    members = relationship("Member", back_populates="group", cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="group", cascade="all, delete-orphan")
    settlements = relationship("Settlement", back_populates="group", cascade="all, delete-orphan")

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False)

    group = relationship("Group", back_populates="members")
    paid_expenses = relationship("Expense", back_populates="payer")

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    title = Column(String(200), nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String(100), default="General")
    payer_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    group = relationship("Group", back_populates="expenses")
    payer = relationship("Member", back_populates="paid_expenses")
    splits = relationship("ExpenseSplit", back_populates="expense", cascade="all, delete-orphan")

class ExpenseSplit(Base):
    __tablename__ = "expense_splits"

    id = Column(Integer, primary_key=True, index=True)
    expense_id = Column(Integer, ForeignKey("expenses.id"), nullable=False)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    share_amount = Column(Float, nullable=False)

    expense = relationship("Expense", back_populates="splits")
    member = relationship("Member")

class Settlement(Base):
    __tablename__ = "settlements"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)
    from_member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    to_member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    group = relationship("Group", back_populates="settlements")
    from_member = relationship("Member", foreign_keys=[from_member_id])
    to_member = relationship("Member", foreign_keys=[to_member_id])
