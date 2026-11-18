
import frappe


def after_insert(doc, method=None):
    set_assigned_status(doc)


def set_assigned_status(doc):
    if doc.assignee and doc.status == "Open":
        doc.db_set("status", "Assigned")


@frappe.whitelist()
def claim_task(parent_name, task_name):
    """Assign an open project task to the logged-in user."""

    if frappe.session.user == "Guest":
        frappe.throw("Please log in to claim this task.")

    opportunity = frappe.get_doc("Volunteer Opportunity", parent_name)

    task = next(
        (row for row in opportunity.project_tasks if row.name == task_name),
        None,
    )

    if not task:
        frappe.throw("Task not found in this volunteer opportunity.")

    if task.status != "Open" or task.assignee:
        frappe.throw("This task is no longer available to claim.")

    task.assignee = frappe.session.user
    task.status = "Assigned"
    opportunity.save()

    return {
        "status": "success",
        "message": "Task claimed successfully.",
        "assignee": frappe.session.user,
        "task_status": task.status,
    }


@frappe.whitelist()
def complete_task(parent_name, task_name):
    """Allow only the assigned user to complete their task."""

    if frappe.session.user == "Guest":
        frappe.throw("Please log in to complete this task.")

    opportunity = frappe.get_doc("Volunteer Opportunity", parent_name)

    task = next(
        (row for row in opportunity.project_tasks if row.name == task_name),
        None,
    )

    if not task:
        frappe.throw("Task not found in this volunteer opportunity.")

    if task.assignee != frappe.session.user:
        frappe.throw("Only the assigned user can complete this task.")

    if task.status != "Assigned":
        frappe.throw("Only assigned tasks can be marked complete.")

    task.status = "Completed"
    opportunity.save()

    return {
        "status": "success",
        "message": "Task marked as completed.",
        "task_status": task.status,
    }
