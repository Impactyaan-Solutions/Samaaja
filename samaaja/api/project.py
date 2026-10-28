import frappe
from samaaja.services.project import ProjectManager
from samaaja.utils.custom_response import custom_response


@frappe.whitelist(methods=["GET"])
def get_my_applications():
    try:
        if frappe.session.user == "Guest":
            return custom_response(
                message="Authentication required",
                status_code=401,
            )

        return ProjectManager.get_my_applications().to_custom_response()

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "Failed to fetch volunteer applications",
        )
        return custom_response(
            message="Failed to fetch volunteer applications",
            status_code=500,
        )


@frappe.whitelist(methods=["GET"])
def get_my_active_projects():
    try:
        if frappe.session.user == "Guest":
            return custom_response(
                message="Authentication required",
                status_code=401,
            )

        return ProjectManager.get_my_active_projects().to_custom_response()

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "Failed to fetch active projects",
        )
        return custom_response(
            message="Failed to fetch active projects",
            status_code=500,
        )


@frappe.whitelist(methods=["GET"])
def get_project(volunteer_opportunity):
    try:
        if frappe.session.user == "Guest":
            return custom_response(
                message="Authentication required",
                status_code=401,
            )

        return ProjectManager.get_project(
            volunteer_opportunity
        ).to_custom_response()

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "Failed to fetch project tasks",
        )
        return custom_response(
            message="Failed to fetch project tasks",
            status_code=500,
        )


@frappe.whitelist(methods=["POST"])
def claim_task(volunteer_opportunity, task_name):
    try:
        if frappe.session.user == "Guest":
            return custom_response(
                message="Authentication required",
                status_code=401,
            )

        return ProjectManager.claim_task(
            volunteer_opportunity=volunteer_opportunity,
            task_name=task_name,
        ).to_custom_response()

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "Failed to claim project task",
        )
        return custom_response(
            message="Failed to claim task",
            status_code=500,
        )


@frappe.whitelist(methods=["POST"])
def complete_task(volunteer_opportunity, task_name, action_name):
    try:
        if frappe.session.user == "Guest":
            return custom_response(
                message="Authentication required",
                status_code=401,
            )

        if not action_name:
            return custom_response(
                message="A successfully submitted action is required",
                status_code=400,
            )

        # Verify that the Action exists and belongs to the current user.
        action = frappe.db.get_value(
            "Action",
            action_name,
            ["name", "user"],
            as_dict=True,
        )

        if not action or action.user != frappe.session.user:
            return custom_response(
                message="The submitted action could not be verified",
                status_code=403,
            )

        return ProjectManager.complete_task(
            volunteer_opportunity=volunteer_opportunity,
            task_name=task_name,
            action_submitted=True,
        ).to_custom_response()

    except Exception:
        frappe.log_error(
            frappe.get_traceback(),
            "Failed to complete project task",
        )
        return custom_response(
            message="Failed to complete task",
            status_code=500,
        )