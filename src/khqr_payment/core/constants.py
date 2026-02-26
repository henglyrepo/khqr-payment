class APIConstants:
    BASE_URL = "https://api-bakong.nbc.gov.kh"
    SIT_BASE_URL = "https://sit-api-bakong.nbc.gov.kh"

    ENDPOINTS = {
        "create_qr": "/api/v1/khqr/create",
        "check_payment": "/api/v1/khqr/check-payment",
        "bulk_payment": "/api/v1/khqr/check-payment-bulk",
        "get_payment": "/api/v1/khqr/get-payment",
        "account_info": "/api/v1/khqr/account-info",
    }

    RELAY_BASE_URL = "https://bakongrelay.com/api"
    RELAY_ENDPOINTS = {
        "create_qr": "/v1/khqr/create",
        "check_payment": "/v1/khqr/check-payment",
        "bulk_payment": "/v1/khqr/check-payment-bulk",
        "get_payment": "/v1/khqr/get-payment",
    }


class QRConstants:
    CURRENCY_USD = "USD"
    CURRENCY_KHR = "KHR"
    CURRENCIES = [CURRENCY_USD, CURRENCY_KHR]

    TAG_PAYLOAD_FORMAT = "00"
    TAG_POINT_OF_INITIATION = "01"
    TAG_MERCHANT_ID = "02"
    TAG_MERCHANT_NAME = "03"
    TAG_MERCHANT_CITY = "04"
    TAG_POSTAL_CODE = "05"
    TAG_ADDITIONAL_DATA = "07"
    TAG_NATIONAL_INFO = "08"
    TAG_CRC = "63"

    TAG_BILL_NUMBER = "01"
    TAG_MOBILE_NUMBER = "02"
    TAG_STORE_LABEL = "03"
    TAG_TERMINAL_LABEL = "04"
    TAG_PURPOSE = "05"
    TAG_LOYALTY_NUMBER = "06"
    TAG_REFERENCE_ID = "07"
    TAG_CONSUMER_ID = "08"
    TAG_TERMINAL_TYPE = "09"
    TAG_PLANE_TYPE = "10"
    TAG_FRAUD_BASE = "11"

    MAX_AMOUNT_KHR = 999999999
    MAX_AMOUNT_USD = 999999.99

    DEFAULT_ENCODING = "UTF-8"
