from samaaja.utils.result import Result
import frappe
from samaaja.services.user import UserManager
from samaaja.services.event import EventManager
class LeaderboardManager:
    @staticmethod
    def get_leaderboard(org_name: str = None) -> Result:
        try:
            leaderboard_data = []
            if org_name:
                leaderboard_data = frappe.db.get_list("User", fields=["name", "full_name", "email", "mobile_no", "gender", "user_image", "interest"], order_by="name", filters={"org_name": org_name})
            else:
                result = frappe.db.sql("""
                                            SELECT
                                            a.user,
                                            COUNT(a.name) AS action_count,
                                            COALESCE(SUM(a.hours_invested), 0) AS hours_invested,
                                            um.user_category
                                            FROM `tabAction` a
                                            INNER JOIN `tabUser` u
                                                ON a.user = u.name
                                            LEFT JOIN `tabUser Metadata` um
                                                ON um.user = a.user
                                            WHERE a.user IS NOT NULL
                                            GROUP BY a.user,  um.user_category
                                            ORDER BY action_count DESC, hours_invested DESC
                                            LIMIT 10
                                        """, as_dict=True)
                for row in result:
                    user = UserManager.get_profile(row["user"]).data
                    if user:
                        user["hours_invested"] = row["hours_invested"] or 0
                        user["action_count"] = row["action_count"]
                        user_category_name = frappe.db.get_value(
                        "User Category",
                        row["user_category"],
                        "category_name"
                        ) if row["user_category"] else ""

                        user["user_category"] = user_category_name or ""

                        leaderboard_data.append(user)
            return Result.success("Leaderboard fetched successfully", data=leaderboard_data)
        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Failed to fetch leaderboard")
            return Result.failure("Failed to fetch leaderboard", error_data=str(e))