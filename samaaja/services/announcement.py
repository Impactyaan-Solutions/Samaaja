import frappe
from frappe import _
from samaaja.utils.result import Result


class AnnouncementManager:
    media_base_url = frappe.conf.media_base_url

    @staticmethod
    def get_announcement(name: str) -> dict:
        return frappe.get_doc("Announcement", name).as_dict()

    
    @staticmethod
    def get_active_announcements() -> Result:
        try:
            now = frappe.utils.now_datetime()
            user = frappe.session.user
            announcement_records = frappe.db.sql(
                """
                SELECT
                    name,
                    title,
                    message,
                    url_link,
                    image,
                    valid_from,
                    valid_to,
                    target_audience
                    FROM `tabAnnouncement`
                    WHERE published = 1
                    AND (
                        valid_to IS NULL
                        OR valid_to >= %(now)s
                    )
                    AND (
                        %(user)s != 'Guest'
                        OR target_audience != 'Registered Users'
                        OR target_audience IS NULL
                    )
                """,
                {
                    "now": now,
                    "user": user
                },
                as_dict=True
            )

            announcements = []

            for doc in announcement_records:
                announcement = {
                    "name": doc.name,
                    "type": "Announcement",
                    "title": doc.title,
                    "message": doc.message,
                    "url_link": doc.url_link,
                    "image": (
                        f"{AnnouncementManager.media_base_url}{doc.image}"
                        if doc.image else ""
                    ),
                    "valid_from": doc.valid_from,
                    "valid_to": doc.valid_to,
                    "target_audience": doc.target_audience,
                }

                announcements.append(announcement)

            # 2. Fetch events and registration status using SQL
            events = []

            if user != "Guest":

                event_records = frappe.db.sql(
                    """
                    SELECT
                        e.name,
                        e.event_category,
                        e.event_type,
                        e.location,
                        e.custom_image,
                        e.starts_on,
                        e.ends_on,
                        e.status,
                        e.sender,
                        e.attending,
                        e.all_day,
                        e.description,

                        EXISTS (
                            SELECT 1
                            FROM `tabEvent Registration` er
                            WHERE er.event = e.name
                            AND er.user = %(user)s
                        ) AS registered

                    FROM `tabEvent` e
                    ORDER BY e.starts_on DESC
                    """,
                    {
                        "user": user
                    },
                    as_dict=True
                )

                for event in event_records:
                    event_data = {
                        "name": event.name,
                        "type": "Event",
                        "event_category": event.event_category,
                        "event_type": event.event_type,
                        "image":(
                        f"{AnnouncementManager.media_base_url}{doc.custom_image}"
                        if doc.image else ""
                        ),
                        "location": event.location,
                        "valid_from": event.starts_on,
                        "valid_to": event.ends_on,
                        "status": event.status,
                        "sender": event.sender,
                        "attending": event.attending,
                        "all_day": event.all_day,
                        "message": event.description,
                        "registered": bool(event.registered)
                    }

                    events.append(event_data)

            # 3. Combine announcements and events
            combined_data = announcements + events

            # 4. Sort by date (newest first)
            combined_data.sort(
                key=lambda x: x.get("valid_from") or x.get("starts_on") or "",
                reverse=True
            )

            return Result.success(
                "   Announcements and events fetched successfully",
                data=combined_data
            )

        except Exception:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to fetch announcements and events"
            )

            return Result.error(
                "Failed to fetch announcements and events"
            )

    
    @staticmethod
    def get_announcement_details(name: str) -> Result:
        try:
            now = frappe.utils.now_datetime()
            user = frappe.session.user

            if not name:
                return Result.bad_request("Announcement name is mandatory")

            if not frappe.db.exists("Announcement", name):
                return Result.not_found("Announcement not found")

            doc = frappe.get_doc("Announcement", name)

        
            if not doc.published:
                return Result.bad_request("Announcement is not published")

            # Validate announcement dates
            

            if doc.valid_to and doc.valid_to < now:
                return Result.bad_request("Announcement has expired")

            # Validate target audience
            if (
                doc.target_audience == "Registered Users"
                and frappe.session.user == "Guest"
            ):
                return Result.bad_request(
                    "Please login to view this announcement"
                )

        # Prepare announcement details
            announcement = {
                "name": doc.name,
                "title": doc.title,
                "message": doc.message,
                "url_link": doc.url_link,
                "image": (
                    f"{AnnouncementManager.media_base_url}{doc.image}"
                    if doc.image
                    else ""
                ),
                "valid_from": doc.valid_from,
                "valid_to": doc.valid_to,
                "target_audience": doc.target_audience,
            }
            return Result.success(
                "Announcement details fetched successfully",
                data=announcement,
            )

        except Exception:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to fetch announcement details",
            )
            return Result.bad_request(
                "Failed to fetch announcement details"
            )
       

    @staticmethod
    def record_interaction(announcement: str, interaction_type: str, contact_id: str = None) -> Result:
        if interaction_type not in ["View", "Click"]:
            return Result.bad_request("Invalid interaction type. Must be View or Click.")

        if not frappe.db.exists("Announcement", announcement):
            return Result.not_found(f"Announcement {announcement} not found.")

        frappe.get_doc({
            "doctype": "Announcement Interaction",
            "announcement": announcement,
            "interaction_type": interaction_type,
            "user": frappe.session.user,
            "contact_id": contact_id,
            "ip_address": frappe.local.request.remote_addr if hasattr(frappe.local, "request") else None
        }).insert(ignore_permissions=True)
        frappe.db.commit()

        return Result.success("Interaction recorded", data={"status": "success"})

    @staticmethod
    def process_scheduled_announcements():
        from frappe.utils import now_datetime, add_to_date, get_datetime
        now = now_datetime()

        scheduled = frappe.get_all("Announcement",
            filters={"published": 0, "publish_on": ["<=", now]},
            pluck="name"
        )
        for name in scheduled:
            doc = frappe.get_doc("Announcement", name)
            doc.published = 1
            doc.valid_from = now
            doc.save(ignore_permissions=True)
            AnnouncementManager.deliver_announcement(doc)
            frappe.db.commit()

        recurring = frappe.get_all("Announcement",
            filters={"published": 1, "is_recurring": 1},
            fields=["name", "frequency", "last_sent_on", "repeat_until", "total_repeat_times", "current_repeat_count"]
        )
        for r in recurring:
            if r.repeat_until and get_datetime(r.repeat_until) < now:
                continue
            if r.total_repeat_times and r.current_repeat_count >= r.total_repeat_times:
                continue

            should_send = not r.last_sent_on
            if not should_send:
                last_sent = get_datetime(r.last_sent_on)
                if r.frequency == "Hourly" and add_to_date(last_sent, hours=1) <= now:
                    should_send = True
                elif r.frequency == "Daily" and add_to_date(last_sent, days=1) <= now:
                    should_send = True
                elif r.frequency == "Weekly" and add_to_date(last_sent, weeks=1) <= now:
                    should_send = True
                elif r.frequency == "Monthly" and add_to_date(last_sent, months=1) <= now:
                    should_send = True

            if should_send:
                doc = frappe.get_doc("Announcement", r.name)
                AnnouncementManager.deliver_announcement(doc)
                doc.last_sent_on = now
                doc.current_repeat_count = (doc.current_repeat_count or 0) + 1
                doc.save(ignore_permissions=True)
                frappe.db.commit()

    @staticmethod
    def deliver_announcement(doc):
        for channel in (doc.delivery_channels or []):
            if not channel.enabled:
                continue
            if channel.channel_name == "Email":
                AnnouncementManager._send_email(doc)
            elif channel.channel_name == "App Notification":
                AnnouncementManager._send_app_notification(doc)
            elif channel.channel_name == "WhatsApp":
                frappe.log_error(f"WhatsApp delivery pending for {doc.name}", "WhatsApp")

    @staticmethod
    def _send_email(doc):
        users = AnnouncementManager._get_target_users(doc.target_audience)
        if users:
            frappe.sendmail(
                recipients=users,
                subject=doc.title,
                message=doc.message,
                reference_doctype=doc.doctype,
                reference_name=doc.name
            )

    @staticmethod
    def _send_app_notification(doc):
        for user in AnnouncementManager._get_target_users(doc.target_audience):
            frappe.get_doc({
                "doctype": "Notification Log",
                "for_user": user,
                "subject": doc.title,
                "email_content": doc.message,
                "document_type": doc.doctype,
                "document_name": doc.name,
                "type": "Alert"
            }).insert(ignore_permissions=True)

    @staticmethod
    def _get_target_users(audience: str) -> list:
        if audience == "All":
            return frappe.get_all("User", filters={"enabled": 1}, pluck="name")
        if audience == "Registered Users":
            return frappe.get_all("User", filters={"enabled": 1, "name": ["!=", "Guest"]}, pluck="name")
        return []
