from fastapi import HTTPException
from datamodels import CreateBankPaymentRequest, CreateBankPaymentResponse, CheckBankPaymentResponse, CheckBankPaymentRequest
import httpx
from config import config as conf

class BankAPI:
    def __init__(self):
        self.url = conf.BANK_API_URL

    async def create_payment(self, order_id: str, amount: int) -> CreateBankPaymentResponse:
        async with httpx.AsyncClient() as client:
            headers = {'Content-Type': 'application/json'}
            post_url = self.url + conf.AQUIRING_START_URL
            data = CreateBankPaymentRequest(order_number=order_id, amount=amount)
            try:
                response = await client.post(post_url, headers=headers, json=data.dict(), timeout=20)
                response.raise_for_status()
                return CreateBankPaymentResponse(**response.json())
            except httpx.TimeoutException:
                raise HTTPException(status_code=504, detail="Bank timeout")
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=502, detail=f"Bank error: {e.response.text}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Bank unavailable: {str(e)}")

    async def check_payment(self, external_id: str) -> CheckBankPaymentResponse:
        async with httpx.AsyncClient() as client:
            check_url = self.url + conf.AQUIRING_CHECK_URL
            data = CheckBankPaymentRequest(payment_id=external_id)
            try:
                response = await client.get(check_url, json=data.dict(), timeout=10)
                if response.status_code == 404:
                    raise HTTPException(status_code=404, detail="Payment not found in bank")
                response.raise_for_status()
                return CheckBankPaymentResponse(**response.json())
            except httpx.TimeoutException:
                raise HTTPException(status_code=504, detail="Bank timeout")
            except httpx.HTTPStatusError as e:
                raise HTTPException(status_code=502, detail=f"Bank error: {e.response.text}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Bank unavailable: {str(e)}")