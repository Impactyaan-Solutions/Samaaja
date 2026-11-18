import frappe

from samaaja.utils.result import Result


class BrandingManager:

    @staticmethod
    def get_branding() -> Result:
        try:
            settings = frappe.get_cached_doc("Samaaja Settings")
            media_base_url = frappe.conf.media_base_url or ""

            return Result.success(
                "Branding fetched successfully",
                {
                    "app_name": settings.get("app_name") or "",
                    "app_logo": (
                        f"{media_base_url}{settings.app_logo}"
                        if settings.get("app_logo") else ""
                    ),
                    "tag_line": settings.get("tag_line") or "",
                },
            )

        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Failed to fetch branding")
            return Result.failure("Failed to fetch branding", error_data=str(e))
