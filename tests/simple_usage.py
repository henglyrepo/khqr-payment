import time
from simple_config import api_token
from khqr_payment import KHQRClient, Merchant

BANK_ACCOUNT = "hengly_ear@aclb"  # Your Bakong account

# 1. Initialize client with your token
client = KHQRClient(api_token)

# Validate token before proceeding
if client.validate_token():
    print("Token is valid and working!")
else:
    print("Token is invalid or expired!")
    client.close()
    exit(1)

# Get account/merchant info (requires bank account)
try:
    merchant_info = client.get_merchant_info(BANK_ACCOUNT)
    print(f"Merchant Info: {merchant_info}")
except Exception as e:
    print(f"Could not get merchant info: {e}")

# Create merchant information with all available fields
merchant = Merchant(
    bank_account="hengly_ear@aclb",  # Your Bakong account
    name="FnDevX",  # Max 25 characters
    city="Phnom Penh",  # Your city
    store_label="Coffee Shop",
    phone_number="85566669999",
    bill_number="TRX987654321",
    terminal_label="Cashier-01",
    acquiring_bank="ACLB",  # Acquiring bank name
    account_information=None,  # For remittance (customer's account)
    purpose="Payment for coffee",
    language_preference="en",
    merchant_name_alternate=None,
    merchant_city_alternate=None,
    static=False,  # Static or Dynamic QR code (default: False)
)

# Create QR code for payment with new parameters
qr = client.create_qr_string(
    merchant="hengly_ear@aclb",  # Bank account (first param)
    merchant_name="Coffee Shop",  # Name of the receiver
    merchant_city="Phnom Penh",
    amount=0.01,  # 9800 Riel
    currency="USD",  # USD or KHR
    store_label="Coffee Shop",
    phone_number="85517272781",
    bill_number="TRX987654321",
    terminal_label="Cashier-01",
    static=False,  # Static or Dynamic QR code (default: False)
)

# Show qr.string to customer (they scan it to pay)
print(f"QR String: {qr.string}")
print(f"MD5 Hash: {qr.md5}")  # Use this to verify payment later

# Generate and save QR image from QRCode object (simplified!)
# This generates QR from raw KHQR string - which is what banking apps scan!
saved_path = client.generate_qr_image(
    qr,  # Pass the QRCode object directly!
    output_path="payment_qr.png",
)
print(f"QR image saved to: {saved_path}")

# Verify payment (after customer has paid)
for _ in range(5):  # Check payment status every 10 seconds, up to 10 times
    status = client.check_payment(qr.md5)
    if status.is_paid:
        print(f"Payment received! Amount: {status.amount}")
        print(f"Status: {status.status}")  # e.g., "paid", "pending"
    else:
        print("Payment not yet received")

    time.sleep(10)  # Wait before checking again


# Close connection when done
client.close()
print("Client connection closed.")

# ============================================
# Check Payment by MD5 Hash (Standalone Example)
# ============================================
# You can check payment using qr.md5 or a saved MD5 hash
# Example: MD5 Hash from a previous transaction

# Option 1: Use qr.md5 from current session
MD5_HASH = qr.md5

# Option 2: Use a saved MD5 hash string
# MD5_HASH = "af0fdac4a8e1e55c095f93e95eb5d0c5"

# Create new client for checking payment
check_client = KHQRClient(api_token)

try:
    # Check payment status by MD5 hash
    status = check_client.check_payment(MD5_HASH)

    print(f"\n=== Payment Check Result ===")
    print(f"MD5 Hash: {MD5_HASH}")
    print(f"Status: {status.status}")  # "paid", "pending", "failed"
    print(f"Is Paid: {status.is_paid}")
    print(f"Amount: {status.amount}")
    print(f"Currency: {status.currency}")

finally:
    check_client.close()
    print("Check client closed.")
