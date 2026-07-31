from pyairtable import Table
from pyairtable.formulas import match
from .lead_loader_base import LeadLoaderBase

class AirtableLeadLoader(LeadLoaderBase):
    def __init__(self, access_token, base_id, table_name):
        # Use the access_token instead of api_key
        self.table = Table(access_token, base_id, table_name)

    def fetch_records(self, lead_ids=None, status_filter="NEW"):
        """
        Fetches leads from Airtable. If lead IDs are provided, fetch those specific records.
        Otherwise, fetch leads matching the given status.
        """
        if lead_ids:
            leads = []
            for lead_id in lead_ids:
                record = self.table.get(lead_id)
                if record:
                    # Merge id and fields into a single dictionary
                    lead = {"id": record["id"], **record.get("fields", {})}
                    leads.append(lead)
            return leads
        else:
            # Fetch leads by status filter (based on "Status" field)
            # You can choose your own field for filter with different naming
            records = self.table.all(formula=match({"Status": status_filter}))
            return [
                {"id": record["id"], **record.get("fields", {})}
                for record in records
            ]

    def update_record(self, lead_id, updates: dict):
        """
        Updates a record in Airtable, adding new fields dynamically if they don't exist.

        Args:
            lead_id (str): The ID of the record to update.
            updates (dict): A dictionary of fields to update or add.
        
        Returns:
            dict: The updated record from Airtable.
        """
        # Fetch the current record to ensure it exists and get its fields
        record = self.table.get(lead_id)
        if not record:
            raise ValueError(f"Record with ID {lead_id} not found.")
        
        # Merge current fields with updates, adding any new fields
        current_fields = record.get("fields", {})
        updated_fields = {**current_fields, **updates}

        # Update the record in Airtable
        return self.table.update(lead_id, updated_fields)

