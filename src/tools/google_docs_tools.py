import os, re
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from src.utils import get_google_credentials

class GoogleDocsManager:
    def __init__(self):
        self.docs_service = build('docs', 'v1', credentials=get_google_credentials())
        self.drive_service = build('drive', 'v3', credentials=get_google_credentials())

    def add_document(self, content, doc_title, folder_name, make_shareable=False, folder_shareable=False, markdown=False):
        """
        Create a Google Document and save it in the specified folder.
        """
        try:
            # Ensure the folder exists
            folder_id, folder_url = self._get_or_create_folder(folder_name, make_shareable=folder_shareable)
            if not folder_id:
                raise ValueError("Failed to get or create the folder.")

            if markdown:
                # Convert Markdown to Google Doc
                doc_id = self._convert_markdown_to_google_doc(content, doc_title)
            else:
                # Create a new Google Document and add content
                doc = self.docs_service.documents().create(body={"title": doc_title}).execute()
                doc_id = doc.get('documentId')

                # Add content to the document
                requests = [{"insertText": {"location": {"index": 1}, "text": content}}]
                self.docs_service.documents().batchUpdate(documentId=doc_id, body={"requests": requests}).execute()

            # Move the document to the folder
            self.drive_service.files().update(
                fileId=doc_id,
                addParents=folder_id,
                removeParents="root",
                fields="id, parents"
            ).execute()

            shareable_url = None
            if make_shareable:
                shareable_url = self._make_document_shareable(doc_id)

            document_url = f"https://docs.google.com/document/d/{doc_id}"
            return {
                "document_url": document_url,  
                "shareable_url": shareable_url,
                "folder_url": folder_url
            }
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def get_document(self, doc_url):
        """
        Retrieve the content of a Google Document by its URL.
        """
        try:
            # Extract the document ID from the URL
            match = re.search(r"/d/([a-zA-Z0-9-_]+)", doc_url)
            if not match:
                raise ValueError("Invalid Google Docs URL format.")
            doc_id = match.group(1)

            # Fetch the document
            document = self.docs_service.documents().get(documentId=doc_id).execute()
            content = ""
            for element in document.get('body', {}).get('content', []):
                if 'paragraph' in element:
                    for text_run in element['paragraph'].get('elements', []):
                        content += text_run.get('textRun', {}).get('content', '')

            return content
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def _get_or_create_folder(self, folder_name, make_shareable=False):
        """
        Get the ID and link of an existing folder with the specified name, or create one if it doesn't exist.
        """
        try:
            # Search for the folder
            query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and trashed=false"
            results = self.drive_service.files().list(q=query, spaces='drive', fields="files(id, name, webViewLink)").execute()
            files = results.get('files', [])
            
            if files:
                # Folder exists
                folder = files[0]
                folder_id = folder['id']
                folder_link = folder.get('webViewLink')
            else:
                # Folder doesn't exist, create it
                file_metadata = {
                    'name': folder_name,
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                folder = self.drive_service.files().create(body=file_metadata, fields='id, webViewLink').execute()
                folder_id = folder['id']
                folder_link = folder.get('webViewLink')

            # Make the folder shareable if required
            if make_shareable:
                self.drive_service.permissions().create(
                    fileId=folder_id,
                    body={"type": "anyone", "role": "reader"},
                    fields="id"
                ).execute()

            return folder_id, folder_link
        except Exception as e:
            print(f"An error occurred while retrieving or creating the folder: {e}")
            return None, None

    def _make_document_shareable(self, doc_id):
        """Make a document shareable with anyone who has the link."""
        try:
            self.drive_service.permissions().create(
                fileId=doc_id,
                body={"type": "anyone", "role": "reader"},
                fields="id"
            ).execute()
            file_info = self.drive_service.files().get(fileId=doc_id, fields="webViewLink").execute()
            return file_info.get("webViewLink")
        except Exception as e:
            print(f"Failed to make document shareable: {e}")
            return None

    def _convert_markdown_to_google_doc(self, markdown_content, title):
        """Convert Markdown content to a Google Document."""
        try:
            # Save the Markdown content as a temporary file
            temp_file_path = "temp_markdown.md"
            with open(temp_file_path, "w") as file:
                file.write(markdown_content)

            # Upload the Markdown file to Google Drive
            file_metadata = {"name": title, "mimeType": "application/vnd.google-apps.document"}
            media = MediaFileUpload(temp_file_path, mimetype="text/markdown")
            file = self.drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()

            # Cleanup the temporary file
            os.remove(temp_file_path)

            return file.get("id")
        except Exception as e:
            print(f"Failed to convert Markdown to Google Doc: {e}")
            return None
