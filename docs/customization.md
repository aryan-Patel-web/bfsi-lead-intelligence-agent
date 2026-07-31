# Customization

### Include Your Business Data

In the `/data` folder, you'll find the following files:

- **agency-description.md**: Contains information about your agency or business, including name, description, and contact details. Replace this with your own agency or business details.
- **case_studies**: Includes past case studies that will be referenced in reports, emails, and interviews. Update this file with your own case studies to personalize the generated content.

Ensure that these files are updated to reflect your own company's information and the specific details you want to highlight in your outreach and reports.

## Customizing CRM Integrations

### Overview
To integrate your custom CRM with the `LeadLoaderBase` class, you need to inherit from `LeadLoaderBase` and implement two methods:
- `fetch_records`: Fetches the leads matching the given status.
- `update_record`: Updates the lead record with new fields.

By default, the available statuses used in the `LeadLoaderBase` class are:
```python
available_statuses = ["NEW","CONTACTED"]
```

However, these statuses can be customized to match the specific lead status values in your CRM.

### Steps to Add a Custom CRM Integration

1. **Create a New Class for Your CRM**
   Inherit from `LeadLoaderBase` and implement the two abstract methods: `fetch_records` and `update_record`.

   ```python
   class CustomCRMLeadLoader(LeadLoaderBase):
       def __init__(self, api_key, custom_parameter):
           # Initialize any API clients or configurations here
           self.api_key = api_key
           self.custom_parameter = custom_parameter
    
    def fetch_records(self, lead_ids=None, status="NEW"):
        """
        Fetch leads from your CRM.
        - If `lead_ids` is provided, fetch those specific leads.
        - Otherwise, fetch leads matching the given status.
        """
        if lead_ids:
            leads = []
            for lead_id in lead_ids:
                lead = crm_api.get_lead(lead_id)  # Replace with your CRM API call
                if lead:
                    # Extract all fields provided by database
                    lead = {"id": record["id"], **record.get("fields", {})}
            return leads
        else:
            # Fetch leads matching the status
            records = crm_api.get_leads_by_status(status)  # Replace with your CRM API call
            return [
                {"id": record["id"], **record.get("fields", {})}  # Extract all fields provided by database dynamically
                for record in records
            ]

    def update_record(self, lead_id, updates: dict):
        """
        Update a single lead record in your CRM.

        Args:
            lead_id (str): ID of the lead to update.
            updates (dict): Dictionary of fields to update.

        Returns:
            dict: Updated lead record.
        """
        lead = crm_api.get_lead(lead_id)  # Replace with your CRM API call
        if not lead:
            raise ValueError(f"Lead with ID {lead_id} not found.")
        updated_lead = crm_api.update_lead(lead_id, updates)  # Replace with your CRM API call
        return updated_lead
   ```

2. **Customizing Lead Statuses**
   By default, the class uses the following statuses:
   ```python
   available_statuses = [
       "NEW",
       "UNQUALIFIED",
       "ATTEMPTED_TO_CONTACT"
   ]
   ```
   If your CRM uses different statuses or additional ones, you can customize this list to match your system. For example, if your CRM uses statuses such as `"IN_PROGRESS"` or `"CONTACTED"`, you can update the `available_statuses` like this:

   ```python
   available_statuses = [
       "NEW",
       "IN_PROGRESS",
       "CONTACTED"
   ]
   ```

   Make sure to update the `fetch_records` method to reflect these changes. For example, if you want to fetch leads with a status of `"IN_PROGRESS"`, you can call `fetch_records(status_filter="IN_PROGRESS")`.

---

## Customizing CRM Field Names

### Overview
By default, in the `nodes` function uses the fields names used in my own database. However, different CRMs or database schemas may use different field names or additional fields that need to be handled.

### Steps to Customize 

1. **Identify the Fields in Your CRM**
   Each CRM or database may have different field names or additional fields. Start by identifying which fields you need to map from your system to the CRM. This may include:
   - Custom field names (e.g., `lead_score` instead of `Score`)
   - Additional fields (e.g., `custom_field_1`, `custom_field_2`)

2. **Modify the `nodes::get_new_leads` Function**
   The `get_new_leads` function fetches lead data from a database and structures it using specific field names (e.g., "First Name", "Last Name", "Email", etc.). If your database uses different field names, you will need to modify this function accordingly.

   For example, if your database uses `first_name` instead of `First Name`, update the code like this:

   ```python
    def get_new_leads(self, lead_ids):
        ...

        # Fetch new leads using the provided loader
        raw_leads = self.lead_loader.fetch_records()
        
        # Structure the leads
        leads = [
            LeadData(
                id=lead["id"],
                name=f'{lead.get("first_name", "")} {lead.get("Last Name", "")}',
                email=lead.get("Email", ""),
                phone=lead.get("Phone", ""),
                address=lead.get("Address", ""),
                profile="" # will be constructed
            )
            for lead in raw_leads
        ]

        ...
   ```

   **IMPORTANT**: The provided field names are based on the structure I use for my own database. If your database uses different field names, just update the code to reflect that.

3. **Modify the `nodes::update_CRM` function**
   The `new_data` dictionary in the `update_CRM` function is where the lead data is prepared before updating the CRM. You can modify this dictionary to include your custom fields.

   For example, if your CRM has a custom field `custom_lead_score` instead of `Score`, you can modify the dictionary like this:

   ```python
   new_data = {
       "Status": "ATTEMPTED_TO_CONTACT",  # Set lead to attempted contact
       "Custom Lead Score": state["lead_score"],  # Updated field name
       "Analysis Reports": state["reports_folder_link"],
       "Outreach Report": state["custom_outreach_report_link"],
       "Last Contacted": get_current_date(),
       "Custom Field 1": state["custom_field_1"],  # Example of an additional field
   }
   ```

### Notes:
- **Field Names**: Always check the database to ensure that the field names you're using match the database schema (names are case-sensitive).

---

## Customizing Prompts

### Overview
In the `prompts.py` file, you will find predefined prompts used for various tasks in your outreach automation. These prompts can be customized to better fit your specific needs, whether for qualifying leads, generating reports, personalizing outreach emails, or preparing interview questions. This guide explains how to update and modify these prompts.

### 1. **Qualifying Leads**
   The prompt used for qualifying leads can be updated to reflect different criteria, depending on the business requirements. You can modify this prompt to suit your specific qualification process and the fields available in your CRM.

### 2. **Generating Reports**
   The report generation prompt can be customized to match different report formats, structures, or analysis points. You can add or remove sections, change the data fields, or adjust the language to fit your needs.

### 3. **Personalized Lead Outreach Email Template**
   The lead outreach email template can be modified to reflect your personalized messaging. This includes updating the language, structure, or including any unique data that you want to add to the email. You can tailor the subject lines, email body, or call-to-action based on your audience and goals.

### 4. **Generating Interview Preparation Questions**
   The interview preparation script and questions can be customized by modifying the following prompts:
   - `GENERATE_SPIN_QUESTIONS_PROMPT`: Tailor the questions to focus on specific aspects of the lead’s needs, role, or challenges.
   - `WRITE_INTERVIEW_SCRIPT_PROMPT`: Adjust the script to focus on the key areas you want to assess during the interview.