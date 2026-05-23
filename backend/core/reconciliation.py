from datetime import datetime, timedelta
from backend.core.database import SessionLocal
from backend.core.models import LedgerEntry

def generate_daily_report():
    db = SessionLocal()
    yesterday = datetime.utcnow() - timedelta(days=1)
    
    # Query all ledger entries for the last 24 hours
    reports = db.query(LedgerEntry).filter(LedgerEntry.timestamp >= yesterday).all()
    
    total_debit = sum(r.debit for r in reports)
    total_credit = sum(r.credit for r in reports)
    
    db.close()
    return {
        "date": yesterday.strftime("%Y-%m-%d"),
        "total_debit": total_debit,
        "total_credit": total_credit,
        "integrity_check": total_debit == total_credit
    }
