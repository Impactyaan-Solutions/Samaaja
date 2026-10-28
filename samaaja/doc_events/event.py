
import io

import frappe
import pyqrcode
from frappe.utils import get_url
from frappe.utils.file_manager import save_file


def generate_check_in_qr(self, method=None):
    """Generate a QR code for an Event if one does not already exist."""

    if self.get("custom_check_in_qr"):
        return

    event_name = self.name
    if not event_name:
        return

    check_in_url = get_url(f"/event-attend/{event_name}")

    qr = pyqrcode.create(check_in_url)

    buffer = io.BytesIO()
    qr.png(buffer, scale=8)
    buffer.seek(0)

    file_doc = save_file(
        fname=f"qr_{event_name}.png",
        content=buffer.getvalue(),
        dt="Event",
        dn=event_name,
        is_private=0,
        df="custom_check_in_qr",
    )

    self.custom_check_in_qr = file_doc.file_url
