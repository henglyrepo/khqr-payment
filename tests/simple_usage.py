import time
import qrcode
from khqr_payment import KHQRClient, Merchant

BANK_ACCOUNT = "hengly_ear@aclb"  # Your Bakong account

# 1. Initialize client with your token
client = KHQRClient(
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImlkIjoiODVmYmVhODM3YTlhNDVkNSJ9LCJpYXQiOjE3NzIxNTEzMjEsImV4cCI6MTc3OTkyNzMyMX0.rFgNo7UcNzY6Z78BL0PeZT1pyGkUVavNHKXnEhFQ2F0"
)

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
    bill_number="TRX01234567",
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
    bill_number="TRX019283775",
    terminal_label="Cashier-01",
    static=False,  # Static or Dynamic QR code (default: False)
)

# Show qr.string to customer (they scan it to pay)
print(f"QR String: {qr.string}")
print(f"MD5 Hash: {qr.md5}")  # Use this to verify payment later

# Generate and save QR image directly in one step (RECOMMENDED for banking apps)
# This generates QR from raw KHQR string - which is what banking apps scan!
saved_path = client.generate_qr_image(
    merchant="hengly_ear@aclb",
    merchant_name="Coffee Shop",
    merchant_city="Phnom Penh",
    amount=0.01,
    currency="USD",
    store_label="Coffee Shop",
    phone_number="85517272781",
    bill_number="TRX019283775",
    terminal_label="Cashier-01",
    static=False,
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

    # time.sleep(10)  # Wait before checking again


# Close connection when done
client.close()
print("Client connection closed.")
