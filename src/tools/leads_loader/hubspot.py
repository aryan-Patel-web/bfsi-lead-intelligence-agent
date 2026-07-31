import os
import hubspot
from hubspot.crm.contacts import SimplePublicObjectInput, ApiException
from .lead_loader_base import LeadLoaderBase

HUBSPOT_CONTACTS_PROPERTIES = ["email", "firstname", "lastname", "hs_lead_status", "address", "phone"]

class HubSpotLeadLoader(LeadLoaderBase):
    def __init__(self, access_token=None):
        # Use access_token instead of environment variable for more flexibility
        self.client = hubspot.Client.create(access_token=access_token or os.getenv("HUBSPOT_API_KEY"))

    def fetch_records(self, lead_ids=None, status_filter="NEW"):
        """
        Fetches leads from HubSpot. If lead IDs are provided, fetch those specific records.
        Otherwise, fetch leads matching the given status.
        """
        try:
            if lead_ids:
                leads = []
                for lead_id in lead_ids:
                    contact = self.client.crm.contacts.basic_api.get_by_id(
                        contact_id=lead_id,
                        properties=HUBSPOT_CONTACTS_PROPERTIES
                    )
                    if contact:
                        # Merge id and properties into a single dictionary
                        lead = {"id": contact.id, **(contact.properties or {})}
                        leads.append(lead)
                return leads
            else:
                # Fetch leads by status filter (based on "Status" field)
                # You can choose your own field for filter with different naming
                api_response = self.client.crm.contacts.basic_api.get_page(
                    limit=100,
                    properties=HUBSPOT_CONTACTS_PROPERTIES,
                    archived=False,
                )
                records = []
                for contact in api_response.results:
                    lead_status = contact.properties.get("hs_lead_status")
                    if lead_status == status_filter:
                        # Merge id and properties into a single dictionary
                        lead = {"id": contact.id, **(contact.properties or {})}
                        records.append(lead)
                return records
        except ApiException as e:
            print(f"Error fetching records from HubSpot: {e}")
            return []

    def update_record(self, lead_id, fields_to_update):
        try:
            # Prepare the fields to update in HubSpot
            properties = fields_to_update
            simple_public_object_input = SimplePublicObjectInput(properties=properties)
            
            # Update the record in HubSpot
            self.client.crm.contacts.basic_api.update(
                contact_id=lead_id, simple_public_object_input=simple_public_object_input
            )
            return {"lead_id": lead_id, "updated_fields": fields_to_update}
        except ApiException as e:
            print(f"Error updating HubSpot record: {e}")
            return None

