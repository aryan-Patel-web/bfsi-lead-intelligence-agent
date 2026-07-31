from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from .lead_loader_base import LeadLoaderBase
from src.utils import get_google_credentials


class GoogleSheetLeadLoader(LeadLoaderBase):
    def __init__(self, spreadsheet_id, sheet_name=None):
        self.sheet_service = build("sheets", "v4", credentials=get_google_credentials())
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = sheet_name or self._get_sheet_name_from_id()
        
    def fetch_records(self, lead_ids=None, status_filter="NEW"):
        """
        Fetches leads from Google Sheets. If lead IDs are provided, fetch those specific records.
        Otherwise, fetch leads matching the given status.
        """
        try:
            result = self.sheet_service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id, range=self.sheet_name
            ).execute()
            rows = result.get("values", [])
            headers = rows[0]
            records = []

            for i, row in enumerate(rows[1:], start=2):  # Start from row 2 for data
                record = dict(zip(headers, row))
                record["id"] = f"{i}"  # Add row number as an ID

                if lead_ids:
                    if record["id"] in lead_ids:
                        records.append(record)
                # Fetch leads by status filter (based on "Status" field)
                # You can choose your own field for filter with different naming
                elif record.get("Status") == status_filter:
                    records.append(record)
                    
            return records
        except HttpError as e:
            print(f"Error fetching records from Google Sheets: {e}")
            return []

    def update_record(self, id, fields_to_update):
        try:
            # Fetch the header row to identify column indices
            result = self.sheet_service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id, range=self.sheet_name
            ).execute()
            rows = result.get("values", [])
            headers = rows[0]

            # Prepare the update body for all specified fields
            updates = []
            for field, value in fields_to_update.items():
                if field in headers:
                    col_index = headers.index(field)
                    col_letter = chr(65 + col_index)  # Convert index to column letter
                    range_ = f"{self.sheet_name}!{col_letter}{id}"
                    updates.append({
                        "range": range_,
                        "values": [[value]],
                    })

            # Execute batch update for efficiency
            if updates:
                body = {"valueInputOption": "RAW", "data": updates}
                self.sheet_service.spreadsheets().values().batchUpdate(
                    spreadsheetId=self.spreadsheet_id,
                    body=body
                ).execute()
            return {"id": id, "updated_fields": fields_to_update}
        except HttpError as e:
            print(f"Error updating Google Sheets record: {e}")
            return None

    def _get_sheet_name_from_id(self):
        try:
            result = self.sheet_service.spreadsheets().get(spreadsheetId=self.spreadsheet_id).execute()
            sheets = result.get("sheets", [])
            if not sheets:
                raise ValueError("No sheets found in the spreadsheet.")
            return sheets[0]["properties"]["title"]  # Default to the first sheet
        except HttpError as e:
            print(f"Error fetching sheet name: {e}")
            raise
