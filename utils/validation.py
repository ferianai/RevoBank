def validate_transaction(data):
    if "account_id" not in data or "amount" not in data or "type" not in data:
        return False, "Missing required fields"
    if data["amount"] <= 0:
        return False, "Invalid transaction amount"
    return True, None
