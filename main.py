import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from referral import router as referral_router

app = FastAPI()

# اتصال روت‌های رفرال
app.include_router(referral_router, prefix="/referral")

# صفحه اصلی برای تست که فقط پیام خوشامدگویی می‌دهد
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
    try:
        response = requests.get(COINGECKO_API, params=params)
        # بررسی وضعیت پاسخ
        response.raise_for_status()  # اگر خطایی وجود داشته باشد، استثنا پرتاب می‌کند

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

    except requests.exceptions.RequestException as e:
        # در صورت بروز خطا در دریافت داده‌ها
        return {"error": f"Unable to fetch data from CoinGecko: {e}"}
