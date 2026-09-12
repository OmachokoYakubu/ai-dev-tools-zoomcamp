from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import engine, Base, get_db
import models
import schemas

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SplitFair API",
    description="Full-stack expense splitting backend built for AI Dev Tools Zoomcamp 2026",
    version="1.0.0"
)

# CORS Middleware to support local dev frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "app": "SplitFair API", "version": "1.0.0"}

@app.get("/api/groups", response_model=List[schemas.GroupOut])
def get_groups(db: Session = Depends(get_db)):
    return db.query(models.Group).order_by(models.Group.id.desc()).all()

@app.post("/api/groups", response_model=schemas.GroupOut, status_code=status.HTTP_201_CREATED)
def create_group(group_in: schemas.GroupCreate, db: Session = Depends(get_db)):
    group = models.Group(
        title=group_in.title,
        description=group_in.description or "",
        currency=group_in.currency or "USD"
    )
    db.add(group)
    db.commit()
    db.refresh(group)
    return group

@app.get("/api/groups/{group_id}", response_model=schemas.GroupDetailOut)
def get_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@app.post("/api/groups/{group_id}/members", response_model=schemas.MemberOut, status_code=status.HTTP_201_CREATED)
def add_member(group_id: int, member_in: schemas.MemberCreate, db: Session = Depends(get_db)):
    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    member = models.Member(
        group_id=group_id,
        name=member_in.name,
        email=member_in.email
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    return member

@app.get("/api/groups/{group_id}/expenses", response_model=List[schemas.ExpenseOut])
def list_expenses(group_id: int, db: Session = Depends(get_db)):
    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    expenses = db.query(models.Expense).filter(models.Expense.group_id == group_id).order_by(models.Expense.created_at.desc()).all()
    results = []
    for exp in expenses:
        split_ids = [s.member_id for s in exp.splits]
        results.append(schemas.ExpenseOut(
            id=exp.id,
            group_id=exp.group_id,
            title=exp.title,
            amount=exp.amount,
            category=exp.category,
            payer_id=exp.payer_id,
            payer_name=exp.payer.name if exp.payer else "Unknown",
            split_member_ids=split_ids,
            created_at=exp.created_at
        ))
    return results

@app.post("/api/groups/{group_id}/expenses", response_model=schemas.ExpenseOut, status_code=status.HTTP_201_CREATED)
def record_expense(group_id: int, expense_in: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    payer = db.query(models.Member).filter(models.Member.id == expense_in.payer_id, models.Member.group_id == group_id).first()
    if not payer:
        raise HTTPException(status_code=400, detail="Payer is not a member of this group")

    if not expense_in.split_member_ids:
        raise HTTPException(status_code=400, detail="Expense must be split among at least one member")

    expense = models.Expense(
        group_id=group_id,
        title=expense_in.title,
        amount=expense_in.amount,
        category=expense_in.category or "General",
        payer_id=expense_in.payer_id
    )
    db.add(expense)
    db.flush()

    per_person_share = expense_in.amount / len(expense_in.split_member_ids)
    for m_id in expense_in.split_member_ids:
        split = models.ExpenseSplit(
            expense_id=expense.id,
            member_id=m_id,
            share_amount=per_person_share
        )
        db.add(split)

    db.commit()
    db.refresh(expense)

    return schemas.ExpenseOut(
        id=expense.id,
        group_id=expense.group_id,
        title=expense.title,
        amount=expense.amount,
        category=expense.category,
        payer_id=expense.payer_id,
        payer_name=payer.name,
        split_member_ids=expense_in.split_member_ids,
        created_at=expense.created_at
    )

@app.get("/api/groups/{group_id}/balances", response_model=schemas.BalanceReport)
def get_balances(group_id: int, db: Session = Depends(get_db)):
    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    members = db.query(models.Member).filter(models.Member.group_id == group_id).all()
    expenses = db.query(models.Expense).filter(models.Expense.group_id == group_id).all()
    settlements = db.query(models.Settlement).filter(models.Settlement.group_id == group_id).all()

    member_map = {m.id: {"name": m.name, "paid": 0.0, "share": 0.0} for m in members}

    for exp in expenses:
        if exp.payer_id in member_map:
            member_map[exp.payer_id]["paid"] += exp.amount
        for split in exp.splits:
            if split.member_id in member_map:
                member_map[split.member_id]["share"] += split.share_amount

    # Factor in settlements
    for setl in settlements:
        if setl.from_member_id in member_map:
            member_map[setl.from_member_id]["paid"] += setl.amount
        if setl.to_member_id in member_map:
            member_map[setl.to_member_id]["share"] += setl.amount

    balances = []
    for m_id, stats in member_map.items():
        net = round(stats["paid"] - stats["share"], 2)
        balances.append(schemas.MemberBalance(
            member_id=m_id,
            member_name=stats["name"],
            paid=round(stats["paid"], 2),
            share=round(stats["share"], 2),
            net_balance=net
        ))

    # Debt Simplification Algorithm
    debtors = []
    creditors = []
    for b in balances:
        if b.net_balance < -0.01:
            debtors.append({"id": b.member_id, "name": b.member_name, "amount": -b.net_balance})
        elif b.net_balance > 0.01:
            creditors.append({"id": b.member_id, "name": b.member_name, "amount": b.net_balance})

    debtors.sort(key=lambda x: x["amount"], reverse=True)
    creditors.sort(key=lambda x: x["amount"], reverse=True)

    recommendations = []
    d_idx, c_idx = 0, 0
    while d_idx < len(debtors) and c_idx < len(creditors):
        debtor = debtors[d_idx]
        creditor = creditors[c_idx]
        settle_amt = min(debtor["amount"], creditor["amount"])

        if settle_amt > 0.01:
            recommendations.append(schemas.SettlementRecommendation(
                from_member_id=debtor["id"],
                from_member_name=debtor["name"],
                to_member_id=creditor["id"],
                to_member_name=creditor["name"],
                amount=round(settle_amt, 2)
            ))

        debtor["amount"] -= settle_amt
        creditor["amount"] -= settle_amt

        if debtor["amount"] <= 0.01:
            d_idx += 1
        if creditor["amount"] <= 0.01:
            c_idx += 1

    return schemas.BalanceReport(balances=balances, settlements=recommendations)

@app.post("/api/groups/{group_id}/settle", response_model=schemas.SettlementOut, status_code=status.HTTP_201_CREATED)
def record_settlement(group_id: int, settle_in: schemas.SettlementCreate, db: Session = Depends(get_db)):
    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    from_m = db.query(models.Member).filter(models.Member.id == settle_in.from_member_id, models.Member.group_id == group_id).first()
    to_m = db.query(models.Member).filter(models.Member.id == settle_in.to_member_id, models.Member.group_id == group_id).first()
    if not from_m or not to_m:
        raise HTTPException(status_code=400, detail="Invalid from or to member")

    settlement = models.Settlement(
        group_id=group_id,
        from_member_id=settle_in.from_member_id,
        to_member_id=settle_in.to_member_id,
        amount=settle_in.amount
    )
    db.add(settlement)
    db.commit()
    db.refresh(settlement)
    return settlement
