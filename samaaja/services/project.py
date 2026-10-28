
import frappe
from samaaja.utils.result import Result


class ProjectManager:
    @staticmethod
    def get_my_applications() -> Result:
        try:
            current_user = frappe.session.user

            if current_user == "Guest":
                return Result.failure(
                    "Please log in to view your applications"
                )

            applications = frappe.get_all(
                "Volunteer Application",
                filters={"user": current_user},
                fields=[
                    "name",
                    "volunteer_opportunity",
                    "workflow_state",
                    "creation",
                ],
                order_by="creation desc",
            )

            for application in applications:
                application["opportunity"] = frappe.db.get_value(
                    "Volunteer Opportunity",
                    application["volunteer_opportunity"],
                    ["title", "type", "category"],
                    as_dict=True,
                )

            return Result.success(
                "Your volunteer applications fetched successfully",
                data={"applications": applications},
            )

        except Exception:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to fetch volunteer applications",
            )
            return Result.failure(
                "Failed to fetch volunteer applications"
            )

    @staticmethod
    def get_project(volunteer_opportunity: str) -> Result:
        try:
            current_user = frappe.session.user

            if current_user == "Guest":
                return Result.failure(
                    "Please log in to view project tasks"
                )

            if not volunteer_opportunity:
                return Result.bad_request(
                    "Volunteer opportunity is required"
                )

            if not frappe.db.exists(
                "Volunteer Opportunity",
                volunteer_opportunity,
            ):
                return Result.not_found("Project not found")

            opportunity_doc = frappe.get_doc(
                "Volunteer Opportunity",
                volunteer_opportunity,
            )

            if not opportunity_doc.get("is_project"):
                return Result.bad_request(
                    "This volunteer opportunity is not a project"
                )

            # Fetch the city from Samaaja Location.
            location = frappe.db.get_value(
                "Samaaja Location",
                opportunity_doc.get("location"),
                "city",
            )

            # Fetch skills from the existing child table.
            skills = frappe.get_all(
                "Skill Child Table",
                filters={
                    "parent": volunteer_opportunity,
                    "parenttype": "Volunteer Opportunity",
                },
                fields=["skill"],
                pluck="skill",
            )

            # Fetch the current user's application and workflow state.
            current_application = frappe.db.get_value(
                "Volunteer Application",
                {
                    "user": current_user,
                    "volunteer_opportunity": volunteer_opportunity,
                },
                ["name", "workflow_state"],
                as_dict=True,
            )

            # Team capacity configured on the opportunity.
            team_size = int(
                opportunity_doc.get("team_size") or 0
            )

            # Fetch applications selected for this opportunity.
            selected_users = frappe.get_all(
                "Volunteer Application",
                filters={
                    "volunteer_opportunity": volunteer_opportunity,
                    "workflow_state": "Selected",
                },
                fields=["user"],
                pluck="user",
            )

            # Count each selected volunteer only once.
            selected_count = len(
                set(filter(None, selected_users))
            )

            # Keep availability within the configured team capacity.
            filled_positions = min(selected_count, team_size)
            remaining_positions = max(
                team_size - filled_positions,
                0,
            )

            opportunity = {
                "name": opportunity_doc.name,
                "title": opportunity_doc.get("title"),
                "description": opportunity_doc.get("description"),
                "is_project": opportunity_doc.get("is_project"),
                "location": location,
                "volunteer_format": opportunity_doc.get(
                    "volunteer_format"
                ),
                "category": opportunity_doc.get("category"),
                "start_date": opportunity_doc.get("start_date"),
                "end_date": opportunity_doc.get("end_date"),
                "expected_time_commitment": opportunity_doc.get(
                    "expected_time_commitment"
                ),
                "skills_needed": skills,
                "team_size": team_size,
                "selected_count": filled_positions,
                "remaining_positions": remaining_positions,
            }

            # Fetch project tasks.
            tasks = frappe.get_all(
                "Project Task",
                filters={
                    "parent": volunteer_opportunity,
                    "parenttype": "Volunteer Opportunity",
                    "parentfield": "project_tasks",
                },
                fields=[
                    "name",
                    "task",
                    "description",
                    "assignee",
                    "status",
                    "idx",
                ],
                order_by="idx asc",
            )

            for task in tasks:
                if task.get("status") == "Completed":
                    task["display_status"] = "Completed"
                elif not task.get("assignee"):
                    task["display_status"] = "Open"
                else:
                    task["display_status"] = "Assigned"

                task["is_assigned_to_current_user"] = (
                    task.get("assignee") == current_user
                )

                task["assignee_name"] = (
                    frappe.db.get_value(
                        "User",
                        task["assignee"],
                        "full_name",
                    )
                    if task.get("assignee")
                    else None
                )

            # Return project, tasks, and current user's application.
            application_data = None

            if current_application:
                application_data = {
                    "name": current_application.get("name"),
                    "workflow_state": current_application.get(
                        "workflow_state"
                    ),
                }

            return Result.success(
                "Project details fetched successfully",
                data={
                    "project": opportunity,
                    "tasks": tasks,
                    "application": application_data,
                },
            )

        except Exception:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to fetch project details",
            )
            return Result.failure(
                "Failed to fetch project details"
            )

    @staticmethod
    def claim_task(
        volunteer_opportunity: str,
        task_name: str,
    ) -> Result:
        """Atomically claim an open task for the current user."""
        try:
            current_user = frappe.session.user

            if current_user == "Guest":
                return Result.failure(
                    "Please log in to claim this task"
                )

            if not volunteer_opportunity or not task_name:
                return Result.bad_request(
                    "Volunteer opportunity and task are required"
                )

            opportunity = frappe.db.sql(
                """
                SELECT name, is_project
                FROM `tabVolunteer Opportunity`
                WHERE name = %s
                FOR UPDATE
                """,
                (volunteer_opportunity,),
                as_dict=True,
            )

            if not opportunity:
                return Result.not_found("Project not found")

            if not opportunity[0].get("is_project"):
                return Result.bad_request(
                    "This volunteer opportunity is not a project"
                )

            task = frappe.db.get_value(
                "Project Task",
                {
                    "name": task_name,
                    "parent": volunteer_opportunity,
                    "parenttype": "Volunteer Opportunity",
                    "parentfield": "project_tasks",
                },
                ["name", "assignee", "status"],
                as_dict=True,
            )

            if not task:
                return Result.not_found(
                    "Task not found in this volunteer opportunity"
                )

            if task.get("status") == "Completed":
                return Result.failure(
                    "This task is already completed"
                )

            if task.get("assignee") or task.get("status") != "Open":
                return Result.failure(
                    "This task is no longer available to claim"
                )

            frappe.db.set_value(
                "Project Task",
                task_name,
                {
                    "assignee": current_user,
                    "status": "Assigned",
                },
                update_modified=True,
            )

            return Result.success(
                "Task claimed successfully",
                data={
                    "task_name": task_name,
                    "assignee": current_user,
                    "status": "Assigned",
                },
            )

        except Exception:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to claim project task",
            )
            return Result.failure(
                "Failed to claim task. Please try again"
            )

    @staticmethod
    def complete_task(
        volunteer_opportunity: str,
        task_name: str,
        action_submitted: bool = False,
    ) -> Result:
        """Complete a task only after its assigned user submits an action."""
        try:
            current_user = frappe.session.user

            if current_user == "Guest":
                return Result.failure(
                    "Please log in to complete this task"
                )

            if not volunteer_opportunity or not task_name:
                return Result.bad_request(
                    "Volunteer opportunity and task are required"
                )

            if not action_submitted:
                return Result.bad_request(
                    "Submit a Log Action successfully before completing this task"
                )

            opportunity = frappe.db.sql(
                """
                SELECT name, is_project
                FROM `tabVolunteer Opportunity`
                WHERE name = %s
                FOR UPDATE
                """,
                (volunteer_opportunity,),
                as_dict=True,
            )

            if not opportunity:
                return Result.not_found("Project not found")

            if not opportunity[0].get("is_project"):
                return Result.bad_request(
                    "This volunteer opportunity is not a project"
                )

            task = frappe.db.get_value(
                "Project Task",
                {
                    "name": task_name,
                    "parent": volunteer_opportunity,
                    "parenttype": "Volunteer Opportunity",
                    "parentfield": "project_tasks",
                },
                ["name", "assignee", "status"],
                as_dict=True,
            )

            if not task:
                return Result.not_found(
                    "Task not found in this volunteer opportunity"
                )

            if task.get("assignee") != current_user:
                return Result.failure(
                    "Only the assigned user can complete this task"
                )

            if task.get("status") != "Assigned":
                return Result.failure(
                    "Only assigned, incomplete tasks can be completed"
                )

            frappe.db.set_value(
                "Project Task",
                task_name,
                "status",
                "Completed",
                update_modified=True,
            )

            return Result.success(
                "Task marked as completed",
                data={
                    "task_name": task_name,
                    "status": "Completed",
                },
            )

        except Exception:
            frappe.log_error(
                frappe.get_traceback(),
                "Failed to complete project task",
            )
            return Result.failure(
                "Failed to complete task. Please try again"
            )
