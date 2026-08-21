import frappe
import json

def create_print_format():
    if not frappe.db.exists("Print Format", {"name": "User Profile"}):
        html = """
       <div class="hidden">
    {% set actions = frappe.get_all("Events", {"user": doc.name}, page_length=1, order_by="creation desc", pluck="creation") %}
    {% set all_actions = frappe.get_all("Events", {"user": doc.name}, pluck="hours_invested") %}
    {% set highlight = frappe.get_all("Events", {"user": doc.name, "highlight": 1}, page_length=1, pluck="description") %}
    {% set user_event_details_category = frappe.db.get_all('Events', fields=['count(name) as count', 'category'], filters={"user": doc.name}, group_by='category', order_by='count desc', page_length=3) %}
    {% set user_badges = frappe.db.get_all('User badge', filters={'user':doc.name},pluck='badge') %}
    {% set reviews = frappe.get_all("User Review", {"user": doc.name}, ["review_title", "reviewer_name", "designation", "comment", "organisation"], page_length=3) %}
    {% set superhero = [] %}
    {% set skills = [] %}
    {% set partners = [] %}
    {% set qr = frappe.get_doc("User Profile QR", doc.name) %}
    {% for badge in user_badges %}
        {% set badge = frappe.get_doc('Badge', badge) %}
        {% if badge.badge_type == 'Skill' %}
            {{ skills.append({"name": badge.title, "image": badge.icon}) }}
        {% endif %}
        {% if 'Partners' in badge_tags %}
            {{ partners.append({"name": badge.title, "image": badge.icon}) }}
        {% endif %}
    {% endfor %}
    {% for cat in user_event_details_category %}
        {% set cat = frappe.get_doc('Action Category', cat.category) %}
            {{ superhero.append({"name": cat.name, "image": cat.icon}) }}
    {% endfor %}
</div>
<div class="lb_wrapper_outer">
        <div class="lb_wrapper">
          <div class="lb_section_left">
            <div class="lb_left_content">
                <div class="user_badge">
                {% if doc.user_image %}
                    <img src="{{frappe.utils.get_url()}}{{ doc.user_image }}" title="{{ doc.full_name }}" />
                {% else %}
                    <img src="https://secure.gravatar.com/avatar/72810bb8f925ab4eae9a3e0b2f681fa5?d=mm&s=200" title="{{ doc.full_name }}" />
                {% endif %}
            </div>
              <div class="user_detail">
                <h3>{{ doc.full_name }}</h3>
                {% if doc.city %}
                    <p>
                      <svg viewBox="0 0 20 20">
                        <path
                          fill="#51A76A"
                          d="M10,1.375c-3.17,0-5.75,2.548-5.75,5.682c0,6.685,5.259,11.276,5.483,11.469c0.152,0.132,0.382,0.132,0.534,0c0.224-0.193,5.481-4.784,5.483-11.469C15.75,3.923,13.171,1.375,10,1.375 M10,17.653c-1.064-1.024-4.929-5.127-4.929-10.596c0-2.68,2.212-4.861,4.929-4.861s4.929,2.181,4.929,4.861C14.927,12.518,11.063,16.627,10,17.653 M10,3.839c-1.815,0-3.286,1.47-3.286,3.286s1.47,3.286,3.286,3.286s3.286-1.47,3.286-3.286S11.815,3.839,10,3.839 M10,9.589c-1.359,0-2.464-1.105-2.464-2.464S8.641,4.661,10,4.661s2.464,1.105,2.464,2.464S11.359,9.589,10,9.589"
                        ></path>
                      </svg>
    
                      <span>{{ doc.city }}</span>
                    </p>
                {% endif %}
                {% if doc.verified_by %}
                        <p>
                            <div class="verified_profile">
<svg id="Layer_1" data-name="Layer 1" viewBox="0 0 122.88 116.87"><polygon fill="#00ade9" points="61.37 8.24 80.43 0 90.88 17.79 111.15 22.32 109.15 42.85 122.88 58.43 109.2 73.87 111.15 94.55 91 99 80.43 116.87 61.51 108.62 42.45 116.87 32 99.08 11.73 94.55 13.73 74.01 0 58.43 13.68 42.99 11.73 22.32 31.88 17.87 42.45 0 61.37 8.24 61.37 8.24"/><path fill="#ffffff" d="M37.92,65c-6.07-6.53,3.25-16.26,10-10.1,2.38,2.17,5.84,5.34,8.24,7.49L74.66,39.66C81.1,33,91.27,42.78,84.91,49.48L61.67,77.2a7.13,7.13,0,0,1-9.9.44C47.83,73.89,42.05,68.5,37.92,65Z"/></svg>
                                <span>Verified Change Maker</span>
                            </div>
                        </p>
                {% endif %}
              </div>
              <div class="user_stats">
                <div class="user_stats_item">
                  <strong>Hours Invested</strong>
                  <span>{{ frappe.utils.flt(sum(all_actions)) }}</span>
                </div>
                <div class="user_stats_item">
                  <strong>Actions Taken</strong>
                  <span>{{ all_actions|length }}</span>
                </div>
              </div>

                {% if doc.bio %}
                    <div class="user_bio">
                        <h4>Bio</h4>
                        <p>
                          {{ doc.bio }}
                        </p>
                    </div>
                {% endif %}
              <div class="qr_scan">
                <p>To see the profile scan the code below:</p>
                <div class="qr_code">
                  <img
                    src="{{frappe.utils.get_url()}}{{ qr.qr }}"
                    alt=""
                  />
                </div>
              </div>
            </div>
          </div>
          <div class="lb_section_right">
            {% if skills %}
            <div class="skill-badges">
              <div class="title">Skill Badges</div>
              <div class="badges-wrapper">
                {% for skill in skills %}
                    <div class="badge">
                      <img src="{{frappe.utils.get_url()}}{{ skill.image }}" alt="" />
                      <span>{{ skill.name }}</span>
                    </div>
                {% endfor %}
              </div>
            </div>
            {% endif %}
            <div class="tabs-wrapper">
              <div class="title">Overview</div>
              <div class="tabs_content panels">
                <div class="overview_content panel">
                    <div class="hidden">
                        {% if highlight %}
                        <fieldset class="profile_fieldset">
                            <legend>Highlight</legend>
                            <p>{{ highlight[0] }}</p>
                        </fieldset>
                        {% endif %}    
                    </div>
                    {% if superhero %}
                        <fieldset class="profile_fieldset">
                            <legend>Interested in</legend>
                            <div class="shf_items">
                                {% for superhe in superhero %}
                                <div class="item">
                                    <img src="{{frappe.utils.get_url()}}{{ superhe.image }}" alt="" />
                                    <span>{{ superhe.name }}</span>
                                </div>
                                {% endfor %}
                            </div>
                        </fieldset>
                    {% endif %}
                    {% if reviews %}
                      <fieldset class="profile_fieldset profile_fieldset100" style="padding: 16px 16px 0">
                        <legend>Expert Review</legend>
                        <div class="expert_review">
                          <div class="content">
                            {% for review in reviews %}
                                <p>
                                  {{ review.comment }}
                                </p>
                                <strong>{{review.reviewer_name}}, {{review.designation}} {{review.organisation}}</strong>
                            {% endfor %}
                          </div>
                        </div>
                      </fieldset>
                    {% endif %}
                  {% if partners %}
                  <fieldset class="profile_fieldset profile_fieldset100">
                        <legend>Partners/Supporters</legend>
                        <div class="partners_wrapper">
                            {% for partner in partners %}
                                <div class="partners_content">
                                    <img src="{{frappe.utils.get_url()}}{{ partner.image }}" alt=""/>
                                </div>
                            {% endfor %}
                        </div>
                  </fieldset>
                  {% endif %}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
        """
        css = """
            .lb_wrapper_outer {
        width: 100%;
        background: linear-gradient(
          180deg,
          rgba(232, 255, 238, 0) 5.73%,
          #e8ffee 23.44%,
          #e7f5ff 100%
        );
      }
      .lb_wrapper {
        width: 100%;
        max-width: 1440px;
        padding: 25px 32px 55px;
        margin: 0 auto;
        box-sizing: border-box;
        display: flex;
        justify-content: space-between;
      }
      .lb_section_left {
        width: 40%;
      }
      .user_badge {
        width: 50px;
        height: 50px;
        margin: 0 auto;
        border-radius: 50%;
        overflow: hidden;
        position: relative;
        z-index: 100;
      }
      .user_badge img {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
      .lb_left_content {
        width: 100%;
        background: #fff;
        box-shadow: 4px 8px 30px 0px rgba(0, 0, 0, 0.12);
        border-radius: 32px;
        position: relative;
        z-index: 99;
        padding: 15px 0 0;
      }
      .edit_cta {
        position: absolute;
        top: 18px;
        right: 18px;
      }
      .edit_cta svg {
        width: 24px;
        height: 24px;
      }
      .user_detail{
        padding: 0 16px;
      }
      .user_detail h3 {
        margin: 0;
        font-size: 20px;
        font-weight: 700;
        color: #2b4754;
        text-align: center;
      }
      .user_detail p {
        margin: 8px 0 0;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #2b4754;
        font-size: 12px;
        font-weight: 400;
      }
      .user_detail svg {
        width: 16px;
        height: 16px;
        margin-right: 4px;
      }
      .last_activity {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 15px 0 0;
        padding: 0 16px;
        font-size: 12px;
      }
      .last_activity svg {
        width: 16px;
        height: 16px;
        margin-right: 5px;
      }
      .user_stats {
        background: #51a76a;
        padding: 6px 32px;
        margin: 17px 0 0;
        display: flex;
      }
      .user_stats_item {
        width: 50%;
        padding: 0 12px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        border-right: 1px solid #fff;
        box-sizing: border-box;
        text-align: center;
      }
      .user_stats_item:last-child {
        border-right: 0;
      }
      .user_stats_item strong {
        color: #2b4754;
        font-size: 12px;
        font-weight: 700;
      }
      .user_stats_item span {
        color: #fff;
        font-size: 16px;
        font-weight: 700;
      }
      .user_bio {
        padding: 20px 16px;
      }
      .user_bio h4 {
        margin: 0;
        padding: 0;
        color: #2b4754;
        font-size: 16px;
        font-weight: 700;
      }
      .user_bio p {
        margin: 8px 0 0;
        color: #2b4754;
        font-size: 12px;
        font-weight: 400;
      }
      .qr_scan{
        padding: 0 16px 20px;
      }
      .qr_scan p {
        color: #e59735;
        font-size: 12px;
        text-align: center;
      }
      .qr_code img {
        width: 100%;
      }
      .ctas_wrapper {
        padding: 48px 32px 0;
      }
      .btn {
        width: 100%;
        margin-bottom: 16px;
        background: transparent;
        outline: 0;
        padding: 18px 0;
        border-radius: 32px;
        box-sizing: border-box;
        font-size: 20px;
        font-weight: 700;
      }
      .btn_fill {
        background-color: #52a769;
        color: #fff;
        border: 0;
      }
      .btn_outline {
        color: #51a76a;
        border: 2px solid #51a76a;
      }
      .report_user {
        padding: 16px 0 32px;
        text-align: center;
      }
      .report_user a {
        color: #51a76a;
        font-size: 16px;
        text-decoration: none;
      }
      .lb_section_right {
        width: 58%;
      }
      .skill-badges {
        width: 100%;
        background: #fff;
        box-shadow: 4px 8px 30px 0px rgba(0, 0, 0, 0.12);
        padding: 15px 20px 0px;
        border-radius: 32px;
      }
      .profile_content .skill-badges {
        display: none;
      }
      .skill-badges .title {
        font-size: 16px;
        font-weight: 700;
        color: #2b4754;
      }
      .badges-wrapper {
        margin: 20px 0 0;
        display: flex;
        justify-content: flex-start;
        flex-wrap: wrap;
      }
      .badge {
        min-width: 18%;
        width: 30%;
        margin: 0 1% 16px;
        display: flex;
        flex-direction: column;
        align-items: center;
        border: 0;
        background-color: transparent !important;
      }
      .badge img {
        width: 40px;
      }
      .badge span {
        font-size: 11px;
        font-weight: 400;
        color: #2b4754;
        line-height: 1.3;
        white-space: break-spaces;
      }
      .badge small {
        font-size: 14px;
        font-weight: 600;
        color: #d85930;
        margin: 4px 0 0;
      }
      .tabs-wrapper {
        width: 100%;
        background: #fff;
        box-shadow: 4px 8px 30px 0px rgba(0, 0, 0, 0.12);
        padding: 15px 20px 0;
        margin: 24px 0 0;
        border-radius: 32px;
      }
      .tabs-wrapper .title{
        font-size: 16px;
        font-weight: 700;
        color: #2b4754;
      }
      .panels .panel {
        display: none;
      }
      .panels .panel:first-child {
        display: flex;
      }
      .overview_content {
        margin: 10px 0 0;
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
      }
      .overview_content fieldset {
        border-radius: 32px;
        border: 1px solid #edb550;
      }
      .overview_content legend {
        color: #51a76a;
        font-size: 16px;
        font-weight: 700;
        width: auto;
        padding: 0 8px;
        margin: 0;
      }
      .profile_fieldset {
        width: 100%;
        padding: 16px;
        margin: 0 0 16px;
        box-sizing: border-box;
      }
      .profile_fieldset h3 {
        padding: 0;
        margin: 0;
        color: #2b4754;
        font-size: 23px;
        font-weight: 700;
      }
      .profile_fieldset p {
        margin: 5px 0 0;
        color: #2b4754;
        font-size: 11px;
        font-weight: 400;
      }
      .shf_items {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
      }
      .shf_items .item {
        display: flex;
        flex-direction: column;
        align-items: center;
      }
      .shf_items .item span {
        font-size: 11px;
        white-space: break-spaces;
      }
      .shf_items .item img {
        width: 40px;
        margin: 0 0 4px;
      }
      .persona_content {
        display: flex;
        justify-content: flex-start;
        align-items: center;
      }
      .persona_content img {
        width: 212px;
      }
      .persona_content .content {
        margin: 0 0 0 60px;
      }
      .persona_content .content strong {
        color: #e59735;
        font-size: 20px;
        font-weight: 700;
        margin: 0 0 12px;
      }
      .persona_content .content p {
        margin: 0 0 24px;
      }
      .persona_content .content ul {
        padding: 0;
        margin: 12px 0 0 20px;
      }
      .expert_review .content p {
        margin: 0;
      }
      .expert_review .content strong {
        color: #e59735;
        font-size: 12px;
        font-weight: 600;
        margin: 0 0 10px;
        display: inline-block;
      }
      .partners_wrapper {
        display: flex;
        justify-content: flex-start;
        align-items: flex-start;
        flex-wrap: wrap;
      }
      .partners_content {
        display: flex;
        align-items: center;
        margin: 0 10px 10px 0;
      }
      .partners_content img {
        margin-right: 10px;
        width: 50px;
      }
      .sign-designation {
        display: flex;
        flex-direction: column;
      }
      .sign-designation strong {
        color: #e59735;
        font-size: 20px;
        font-weight: 600;
      }
      .sign-designation p {
        font-size: 16px;
        font-weight: 600;
      }
      .action_item {
        border-bottom: 1px solid #786b5a;
        padding: 24px 18px 0;
      }
      .action_item:last-child {
        border-bottom: 0;
        padding-bottom: 24px;
      }
      .action_item_head {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 0 24px;
      }
      .action_item_head a {
        color: #2b4754;
      }
      .action_item h3 {
        margin: -14px 0 10px;
        padding: 0;
        color: #2b4754;
        font-size: 24px;
        font-weight: 700;
        display: flex;
        justify-content: flex-start;
        align-items: center;
      }
      .action_item p svg {
        width: 20px;
        height: 20px;
      }
      .action_item_head p {
        color: #2b4754;
        font-size: 16px;
        font-weight: 400;
        display: flex;
        align-items: center;
        margin: 0;
      }
      .action_item_head svg {
        width: 20px;
        height: 20px;
        margin: 0 4px 0 0;
      }
      .dropdown-menu.show {
        right: 0 !important;
        left: inherit !important;
        top: 25px !important;
        transform: none !important;
      }
      .action_content {
        padding: 20px 0;
      }
      .verified_profile {
        font-size: 12px;
        font-weight: 600;
        color: #666666;
        text-align: center;
        padding: 0 15px;
        box-sizing: border-box;
        display: flex;
        align-items: center;
        justify-content: center;
      }
      .verified_profile svg,
      .vouched_by svg {
        width: 25px;
        height: 25px;
        margin-right: 4px;
      }
      .vouched_by svg {
        flex-shrink: 0;
        margin-top: 3px;
      }
      .vouched_by {
        font-size: 22px;
        font-weight: 600;
        color: #51a76a;
        display: flex;
        align-items: flex-start;
        justify-content: center;
        margin-left: 10px;
      }
        """
        print_format = frappe.get_doc({
            "doctype": "Print Format",
            "name": "User Profile",
            "doc_type": "User",
            "module": "Core",
            "custom_format": 1,
            "html": html,
            "css":css,
            "print_format_type":"Jinja"
        })

        print_format.insert(ignore_permissions=True)
        frappe.db.commit()

def create_discussions_web_page():
    if frappe.db.exists("Web Page", "discussions"):
        print("Web Page already exists.")
        return

    doc = frappe.get_doc({
        "doctype": "Web Page",
        "title": "Discussions",
        "route": "discussions",
        "published": 1,
        "content_type": "Page Builder",
        "full_width": 1,
        "show_title": 0,
        "show_sidebar": 0,
        "enable_comments": 0,
        "page_blocks": [
            {
                "doctype": "Web Page Block",
                "web_template": "Discussions",
                "web_template_values": json.dumps({
                    "title": "Samaaja conversations",
                    "cta_title": "New conversation",
                    "docname": "discussions",
                    "single_thread": 0
                }),
                "add_container": 1,
                "add_top_padding": 1,
                "add_bottom_padding": 1
            }
        ]
    })

    doc.insert(ignore_permissions=True)
    frappe.db.commit()

def website_settings():
    settings = frappe.get_single("Website Settings")
    settings.home_page = "index"  # samaaja/www/index.html - the Vue app
    settings.banner_image = "/assets/samaaja/images/Samaaja.png"
    settings.save()
    frappe.db.commit()

def create_samaaja_settings():
    meta = frappe.get_meta("Samaaja Settings")

    def has_field(fieldname: str) -> bool:
        return bool(meta.get_field(fieldname))

    # Populate Samaaja Settings (single) with default values.
    data = {
        # Hero / leaderboard page config
        "samaaja_icon": "/assets/samaaja/images/Samaaja.png",
        "hero_bg_color": "#FFFFF5",
        "hero_text_color": "#090909",
        "tagline": "Samaaja: Where Changemakers Grow Together",
        "blurb": "#GrowWithSamaaja",
        "summary": "An open-source platform for non-profits to design, activate, and scale changemaker communities",
        "show_cta_1": 1,
        "cta1_label": "Join Samaaja",
        "cta1_link": "/discussions",
        "show_cta_2": 1,
        "cta2_label": "Join Samaaja Forum",
        "cta2_link": "/discussions",
        "show_opportunities_section_": 1,
        "show_campaign_section_": 1,

        # Leaderboard section labels
        "total_members_label": "Total Members",
        "actions_taken_label": "Actions Taken",
        "hours_invested_label": "Hours Invested",
        "verified_members_label": "Verified Members",
        "verified_members_summary": "Members who have been vetted and verified.",
        "most_active_members_label": "Most Active Members",
        "most_active_members_summary": "Top contributors who lead the change.",
        "most_active_cities_label": "Most Active Cities",
        "most_active_cities_summary": "Cities showing the greatest participation.",

        # Other settings commonly used by pages/APIs
        "location_field_name": "District",
        "user_profile_location_field": "district",

        # Child table
        "samaaja_feature_list": [
            {"feature_name": "Dynamic Portfolio", "icon": "/assets/samaaja/images/build_skills.png"},
            {"feature_name": "Leaderboards", "icon": "/assets/samaaja/images/access_mentorship.png"},
            {"feature_name": "Build Expertise", "icon": "/assets/samaaja/images/land_internships.png"},
            {"feature_name": "Funding Opportunities", "icon": "/assets/samaaja/images/seeds_funds.png"},
        ],
    }

    # Load the single doc (or create if doesn't exist — handled by frappe.get_single)
    doc = frappe.get_single("Samaaja Settings")

    # Set scalar fields (only if field exists)
    for field, value in data.items():
        if field == "samaaja_feature_list":
            continue
        if has_field(field):
            doc.set(field, value)

    # Clear and set feature list (child table)
    if has_field("samaaja_feature_list"):
        doc.set("samaaja_feature_list", [])
        for feature in data.get("samaaja_feature_list", []):
            doc.append(
                "samaaja_feature_list",
                {"feature_name": feature.get("feature_name"), "icon": feature.get("icon")},
            )

    # Save the document
    doc.save(ignore_permissions=True)
    frappe.db.commit()

def enable_energy_points():
    ss = frappe.get_single("Energy Point Settings")
    ss.enabled = 1  # the field really is called `enabled`; the old name was silently ignored
    ss.save()
    frappe.db.commit()

def after_install():
    """Runs automatically when the app is installed on a site.

    Configuration and reference data only - never demo content.
    The demo users, demo events, demo campaigns and demo opportunities that
    used to live in this file were removed deliberately. See git history if
    you ever need them back for a sales or training environment.
    """
    from samaaja.utils.temp_sync_options import sync_options

    print("Setting up Samaaja...")

    # First, because every screen after signup depends on these records:
    # signup needs the genders and user categories, Log Action needs the
    # action types and categories.
    sync_options()

    website_settings()
    create_samaaja_settings()
    enable_energy_points()
    create_print_format()
    create_discussions_web_page()

    print("Samaaja setup complete.")
