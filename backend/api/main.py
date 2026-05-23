from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from backend.core.service import transfer_funds

app = FastAPI(title="Camtel MoMo Core API")

class TransferRequest(BaseModel):
    sender: str = Field(..., min_length=9, max_length=15)
    receiver: str = Field(..., min_length=9, max_length=15)
    amount: float = Field(..., gt=0)
    reference: str

@app.post("/api/v1/transfer")
async def execute_transfer(request: TransferRequest):
    try:
        transfer_funds(request.sender, request.receiver, request.amount, request.reference)
        return {"status": "success", "reference": request.reference}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Transaction failed")
