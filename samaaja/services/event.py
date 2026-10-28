import frappe

from samaaja.utils.result import Result


class EventManager:
    @staticmethod
    def register_for_event(event: str) -> Result:
        try:
            user = frappe.session.user

            if user == "Guest":
                return Result.bad_request(
                    "Please log in to register for the event"
                )

            if not event:
                return Result.bad_request(
                    "Event is required"
                )

            if not frappe.db.exists("Event", event):
                return Result.not_found(
                    "Event not found"
                )

            # Prevent duplicate registrations
            if frappe.db.exists(
                "Event Registration",
                {
                    "event": event,
                    "user": user,
                },
            ):
                return Result.bad_request(
                    "You have already registered for this event"
                )

           

            registration = frappe.new_doc("Event Registration")
            registration.event = event
            registration.user = user
           
            registration.insert(ignore_permissions=True)

            return Result.success(
                "Event registration successful",
                data=registration,
            )

        except frappe.exceptions.ValidationError as e:
            return Result.bad_request(str(e))

        except Exception as e:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to register for event",
            )

            return Result.failure(
                "Failed to register for event",
                error_data=str(e),
            )

    @staticmethod
    def check_registered_event(event: str) -> Result:
        try:
            user = frappe.session.user

            if user == "Guest":
                return Result.bad_request("Please log in")

            if not event:
                return Result.bad_request("Event is required")

            if not frappe.db.exists("Event", event):
                return Result.not_found(
                    "Event not found"
                )    

            registration = frappe.db.exists(
                "Event Registration",
                {
                    "event": event,
                    "user": user,
                },
            )

            return Result.success(
                "Registration status fetched successfully",
                data={
                    "event": event,
                    "registered": bool(registration),
                },
            )

        except Exception as e:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to check event registration",
            )
            return Result.failure(
                "Failed to check event registration",
                error_data=str(e),
            )

    
    @staticmethod
    def check_in(event: str) -> Result:
        try:
            user = frappe.session.user

            if user == "Guest":
                return Result.bad_request("Please log in")

            if not event:
                return Result.bad_request("Event is required")

            # Check whether the event exists
            if not frappe.db.exists("Event", event):
                return Result.not_found("Event not found")

            # Fetch the event date
            event_details = frappe.db.get_value(
                "Event",
                event,
                ["starts_on","ends_on", "subject"],
                as_dict=True,
            )
            event_start_date = event_details.starts_on
            event_end_date = event_details.ends_on
            event_name = event_details.subject
            if not event_start_date or not event_end_date:
                return Result.bad_request(
                    "Event start date or end date is not configured"
                )
            # Allow check-in only on the event date
            today = frappe.utils.getdate()
            event_start_date = frappe.utils.getdate(event_start_date)
            event_end_date = frappe.utils.getdate(event_end_date)

            if  not (event_start_date <= today <= event_end_date):
                return Result.bad_request(
                    "Check-in is allowed only during the event dates"
                )

            # Find the user's registration
            registration_name = frappe.db.get_value(
                "Event Registration",
                {
                    "event": event,
                    "user": user,
                },
                "name",
            )

            # Automatically register if not registered
            if not registration_name:
                registration = frappe.new_doc("Event Registration")
                registration.event = event
                registration.user = user
                registration.insert(ignore_permissions=True)

                registration_name = registration.name

            # Fetch the existing registration
            registration = frappe.get_doc(
                "Event Registration",
                registration_name,
            )

            # Prevent duplicate check-ins
            if registration.checked_in:
                return Result.success(
                    "You have already checked in",
                    data={
                        "event": event,
                        "registered": True,
                        "checked_in": True,
                        "checked_in_on": registration.checked_in_on,
                        "event_name": event_name
                    },
                )

            # Mark attendance
            registration.checked_in = 1
            registration.checked_in_on = frappe.utils.now_datetime()
            registration.save(ignore_permissions=True)

            frappe.db.commit()

            return Result.success(
                "Check-in successful. Attendance marked.",
                data={
                    "event": event,
                    "registered": True,
                    "checked_in": True,
                    "checked_in_on": registration.checked_in_on,
                    "event_name": event_name,
                },
            )

        except frappe.exceptions.ValidationError as e:
            return Result.bad_request(str(e))

        except Exception as e:
            frappe.log_error(
                frappe.get_traceback(),
                "Event Check-In Error",
            )

            return Result.failure(
                "Unable to check in for the event",
                error_data=str(e),
            )
