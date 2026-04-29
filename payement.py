import razorpay
from database import get_db


RAZORPAY_KEY_ID = "YOUR_KEY_ID"
RAZORPAY_KEY_SECRET = "YOUR_KEY_SECRET"

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

def create_razorpay_order(amount: int, plan_name: str):
    """Amount paison mein hota hai (e.g., $4 = 400 cents/paise)"""
    data = {
        "amount": amount * 100,  # Razorpay amounts in smallest currency unit
        "currency": "INR", # Ya USD jo bhi tum use karo
        "receipt": f"receipt_{plan_name}",
        "notes": {
            "plan": plan_name
        }
    }
    order = client.order.create(data=data)
    return order

def verify_payment_signature(params_dict):
    """Verify ki payment genuine hai ya nahi"""
    try:
        client.utility.verify_payment_signature(params_dict)
        return True
    except:
        return False

def update_user_plan_in_db(email: str, plan_name: str):
    """Payment success hone par DB update karna"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET plan_type = ? WHERE email = ?", (plan_name, email))
    conn.commit()
    conn.close()