from fastapi import APIRouter
import uuid

router = APIRouter()

# دیتابیس موقتی برای ذخیره‌سازی اطلاعات کاربران
users = {}

@router.get("/join")
async def join(user_id: str = "", ref: str = ""):
    if not user_id:
        return {"error": "user_id is required"}

    if user_id not in users:
        # ایجاد کاربر جدید و افزودن اطلاعات مربوط به آن
        users[user_id] = {
            "user_id": user_id,
            "ref": ref,
            "ref_code": str(uuid.uuid4())[:8],  # ایجاد کد رفرال یکتا
            "points": 0,
            "invited": []
        }
        # اگر کاربر از یک رفرال آمده باشد، به کاربر مرجع امتیاز داده می‌شود
        if ref in users:
            users[ref]["points"] += 10
            users[ref]["invited"].append(user_id)

    return users[user_id]

@router.get("/myref")
async def get_my_ref(user_id: str = ""):
    if user_id in users:
        return users[user_id]
    return {"error": "not registered"}
