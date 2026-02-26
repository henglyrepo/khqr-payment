import hashlib

from khqr_payment.core.constants import QRConstants
from khqr_payment.models.qr import QRCodeRequest


class QRStringGenerator:
    """Generate QR string for Bakong KHQR standard."""

    @staticmethod
    def generate(request: QRCodeRequest) -> tuple[str, str]:
        """
        Generate QR string from request.
        
        Args:
            request: QRCodeRequest object
            
        Returns:
            Tuple of (qr_string, md5_hash)
        """
        tags = []

        tags.append(QRStringGenerator._create_tag(QRConstants.TAG_PAYLOAD_FORMAT, "01"))
        tags.append(QRStringGenerator._create_tag(QRConstants.TAG_POINT_OF_INITIATION,
                                                   "11" if not request.static else "12"))

        tags.append(QRStringGenerator._create_tag(QRConstants.TAG_MERCHANT_ID, request.bank_account))
        tags.append(QRStringGenerator._create_tag(QRConstants.TAG_MERCHANT_NAME, request.merchant_name))
        tags.append(QRStringGenerator._create_tag(QRConstants.TAG_MERCHANT_CITY, request.merchant_city))

        if request.postal_code:
            tags.append(QRStringGenerator._create_tag(QRConstants.TAG_POSTAL_CODE, request.postal_code))

        additional_data = {}
        if request.bill_number:
            additional_data[QRConstants.TAG_BILL_NUMBER] = request.bill_number
        if request.phone_number:
            additional_data[QRConstants.TAG_MOBILE_NUMBER] = request.phone_number
        if request.store_label:
            additional_data[QRConstants.TAG_STORE_LABEL] = request.store_label
        if request.terminal_label:
            additional_data[QRConstants.TAG_TERMINAL_LABEL] = request.terminal_label
        if request.purpose:
            additional_data[QRConstants.TAG_PURPOSE] = request.purpose

        if additional_data:
            additional_data_str = QRStringGenerator._build_additional_data(additional_data)
            tags.append(QRStringGenerator._create_tag(QRConstants.TAG_ADDITIONAL_DATA, additional_data_str))

        if request.currency:
            currency_tag = "5303734" if request.currency == "KHR" else "5303524"
            tags.append(currency_tag)

        if request.amount is not None:
            amount_str = QRStringGenerator._format_amount(request.amount, request.currency)
            tags.append(amount_str)

        qr_string = "".join(tags)

        crc = QRStringGenerator._calculate_crc(qr_string)
        qr_string += crc

        md5_hash = QRStringGenerator._calculate_md5(qr_string)

        return qr_string, md5_hash

    @staticmethod
    def _create_tag(tag_id: str, value: str) -> str:
        """Create a tag with ID and length prefix."""
        length = str(len(value)).zfill(2)
        return f"{tag_id}{length}{value}"

    @staticmethod
    def _build_additional_data(data: dict[str, str]) -> str:
        """Build additional data field."""
        result = []
        for key, value in data.items():
            length = str(len(value)).zfill(2)
            result.append(f"{key}{length}{value}")
        return "".join(result)

    @staticmethod
    def _format_amount(amount: float, currency: str) -> str:
        """Format amount according to currency."""
        if currency == "USD":
            formatted = f"{amount:.2f}"
        else:
            formatted = str(int(amount))

        return f"54{len(formatted):02d}{formatted}"

    @staticmethod
    def _calculate_crc(qr_string: str) -> str:
        """Calculate CRC for QR string."""
        crc = 0xFFFF

        for char in qr_string:
            crc ^= ord(char)
            for _ in range(8):
                if crc & 0x0001:
                    crc = (crc >> 1) ^ 0x8408
                else:
                    crc >>= 1

        crc ^= 0xFFFF
        crc = hex(crc)[2:].upper().zfill(4)

        return f"{QRConstants.TAG_CRC}{crc}"

    @staticmethod
    def _calculate_md5(qr_string: str) -> str:
        """Calculate MD5 hash of QR string."""
        return hashlib.md5(qr_string.encode(QRConstants.DEFAULT_ENCODING)).hexdigest()


def generate_qr_string(request: QRCodeRequest) -> tuple[str, str]:
    """
    Generate QR string from request.
    
    Args:
        request: QRCodeRequest object
        
    Returns:
        Tuple of (qr_string, md5_hash)
    """
    return QRStringGenerator.generate(request)
