from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from referral import router as referral_router

app = FastAPI()

# اتصال روت‌های رفرال
app.include_router(referral_router, prefix="/referral")

# صفحه اصلی برای تست که فقط پیام خوشامدگویی می‌دهد
@app.get("/")
async def root():
    return {"message": "به مینی‌اپ ارز دیجیتال خوش آمدید!"}
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # اجازه دسترسی از هر جایی (مهم برای فرانت)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

COINGECKO_API = "https://api.coingecko.com/api/v3/coins/markets"

@app.get("/crypto")
def get_crypto():
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": False
    }
    response = requests.get(COINGECKO_API, params=params)
    data = response.json()
    result = [
        {
            "id": coin["id"],
            "symbol": coin["symbol"].upper(),
            "name": coin["name"],
            "price": coin["current_price"],
            "change": coin["price_change_percentage_24h"]
        } for coin in data
    ]
    return result
