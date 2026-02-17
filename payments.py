from typing import Dict
from datetime import datetime
from db import get_all_active_investments, get_user_by_id, update_user_balance, get_referrals_of

# This file contains a placeholder for M10 payments and the daily payout logic.
# Replace the placeholder `send_to_m10_card` with real API calls.

def send_to_m10_card(card_number: str, amount: float) -> Dict:
    # Placeholder: in production call M10 API here.
    print(f"[payments] Simulate sending {amount} AZN to card {card_number} at {datetime.utcnow().isoformat()}")
    return {"status": "ok", "tx_id": "SIMULATED"}

def daily_payouts():
    # For every active investment: pay daily profit 10% of invested amount to user's balance.
    investments = get_all_active_investments()
    for inv in investments:
        user = get_user_by_id(inv['user_id'])
        if not user:
            continue
        daily_profit = inv['amount'] * 0.10
        update_user_balance(user['id'], daily_profit)

    # Referral payouts: For each user, for each referral, give 1 AZN + 10% of referral's investments
    # This follows the user's spec: "hər referala görə 1 AZN və referalın yatırımının 10%-i + 1AZN"
    # Iterate users and their referrals.
    # Note: This is a simple approach and may give large payouts; adjust rules as needed.
    # Fetch all users by scanning referrals (inefficient but simple for small scale)
    from db import get_conn
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id FROM users')
    all_users = [r['id'] for r in cur.fetchall()]
    for uid in all_users:
        refs = get_referrals_of(uid)
        total_referral_payout = 0
        for r in refs:
            # sum active investments of referral
            cur.execute('SELECT amount FROM investments WHERE user_id=? AND active=1', (r['id'],))
            amounts = [row['amount'] for row in cur.fetchall()]
            for amt in amounts:
                total_referral_payout += (amt * 0.10) + 1.0
        if total_referral_payout > 0:
            update_user_balance(uid, total_referral_payout)

    print(f"[payments] Daily payouts completed at {datetime.utcnow().isoformat()}")
