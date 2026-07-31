from abc import ABC, abstractmethod


class LeadLoaderBase(ABC):
    available_statuses = [
        "NEW",
        "UNQUALIFIED",
        "ATTEMPTED_TO_CONTACT"
    ]

    @abstractmethod
    def fetch_records(self, status_filter="NEW"):
        """
        Abstract method to fetch records. Must be implemented by subclasses.
        Should return a list of records matching the status_filter.
        """
        pass

    @abstractmethod
    def update_record(self, lead_id, status):
        """
        Abstract method to update a record's status. Must be implemented by subclasses.
        """
        pass

    def fetch_new_leads(self):
        """
        Get leads with status "NEW" by default.
        """
        try:
            return self.fetch_records(status_filter="NEW")
        except Exception as e:
            print(f"Error fetching new leads: {e}")
            return []

    def update_lead_status(self, lead_id, status):
        """
        Update the lead's status if it's valid.
        """
        if status not in self.available_statuses:
            print(f"Invalid status: {status}. Must be one of {self.available_statuses}.")
            return None
        try:
            return self.update_record(lead_id, status)
        except Exception as e:
            print(f"Error updating lead status: {e}")
            return None
