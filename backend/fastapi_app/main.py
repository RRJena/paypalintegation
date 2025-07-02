from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS config for frontend communication
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# PayPal API credentials from .env
CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")
BASE_URL = os.getenv("PAYPAL_API_BASE")

# Request models
class OneTimePaymentRequest(BaseModel):
    amount: float
    currency: str
    return_url: str
    cancel_url: str

class SubscriptionRequest(BaseModel):
    plan_name: str
    price: float
    currency: str
    return_url: str
    cancel_url: str

# Fetch PayPal access token
async def get_access_token():
    auth = (CLIENT_ID, CLIENT_SECRET)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/v1/oauth2/token", auth=auth, data=data, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="PayPal Auth Failed")

    return response.json()["access_token"]

# Create one-time payment
@app.post("/pay/one-time")
async def create_one_time_payment(req: OneTimePaymentRequest):
    token = await get_access_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": req.currency,
                "value": f"{req.amount:.2f}"
            }
        }],
        "application_context": {
            "return_url": req.return_url,
            "cancel_url": req.cancel_url
        }
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(f"{BASE_URL}/v2/checkout/orders", json=payload, headers=headers)

    if res.status_code != 201:
        raise HTTPException(status_code=500, detail="Failed to create PayPal Order")

    return res.json()

# Capture a payment after approval
@app.post("/pay/capture/{order_id}")
async def capture_payment(order_id: str):
    token = await get_access_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(f"{BASE_URL}/v2/checkout/orders/{order_id}/capture", headers=headers)

    if res.status_code != 201:
        raise HTTPException(status_code=500, detail=f"Failed to capture payment: {res.text}")

    return res.json()

# Create a recurring payment subscription
@app.post("/pay/recurring")
async def create_subscription(req: SubscriptionRequest):
    token = await get_access_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # Replace with your actual PayPal product ID
    plan_payload = {
        "product_id": "YOUR_PRODUCT_ID",
        "name": req.plan_name,
        "billing_cycles": [{
            "frequency": {
                "interval_unit": "MINUTE",
                "interval_count": 1
            },
            "tenure_type": "REGULAR",
            "sequence": 1,
            "total_cycles": 0,
            "pricing_scheme": {
                "fixed_price": {
                    "value": f"{req.price:.2f}",
                    "currency_code": req.currency
                }
            }
        }],
        "payment_preferences": {
            "auto_bill_outstanding": True,
            "setup_fee_failure_action": "CONTINUE",
            "payment_failure_threshold": 3
        }
    }

    async with httpx.AsyncClient() as client:
        plan_res = await client.post(f"{BASE_URL}/v1/billing/plans", json=plan_payload, headers=headers)

    if plan_res.status_code not in (200, 201):
        raise HTTPException(status_code=500, detail=f"Failed to create PayPal Plan: {plan_res.text}")

    plan_id = plan_res.json()["id"]

    sub_payload = {
        "plan_id": plan_id,
        "application_context": {
            "brand_name": "Your Brand",
            "user_action": "SUBSCRIBE_NOW",
            "return_url": req.return_url,
            "cancel_url": req.cancel_url
        }
    }

    async with httpx.AsyncClient() as client:
        sub_res = await client.post(f"{BASE_URL}/v1/billing/subscriptions", json=sub_payload, headers=headers)

    if sub_res.status_code != 201:
        raise HTTPException(status_code=500, detail=f"Failed to create subscription: {sub_res.text}")

    return sub_res.json()
