"""Google API, files and documents helpers."""
import os
import re
import time
import typing as t
from pathlib import Path

import googleapiclient.errors as err
import httplib2
import oauth2client
from googleapiclient import discovery
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials

from fw_gdrive import utils

DISCOVERY_DOC = "https://docs.googleapis.com/$discovery/rest?version=v1"


class GoogleAPIClient:
    """Instantiate Google API Client for Google Drive and Google Documents services.

    Args:
        service_cred_path: Path of the service account credential.
        scopes (Optional): Scopes to use when acquiring an access token.

    Attributes:
        svc_acc_cred (ServiceAccountCredentials): A Service Account credential object.
        drive_service (discovery.Resource): A Resource object for interacting with Google Drive service.
        doc_service (discovery.Resource): A Resource object for interacting with Google Document service.

    Returns:
        A basic GoogleAPIClient object that contains Google Service Account
        credentials and API client to access Google Drive and Google Documents.

    """

    def __init__(
        self,
        service_cred_path: t.Union[Path, str] = None,
        scopes: t.Union[t.List[str], str] = "",
    ):
        """Initialize Google API client."""
        if service_cred_path is None:
            # Try to retrieve the path from env variable
            try:
                service_cred_path = os.environ["SERVICE_ACCOUNT"]
            except KeyError:
                raise RuntimeError(
                    "$SERVICE_ACCOUNT is not set up as an environment variable. "
                    "Unable to locate service cred path."
                )

        self.svc_acc_cred = utils.login(service_cred_path, scopes)
        self.drive_service = self._get_api_client(
            svc_acc_cred=self.svc_acc_cred, service="drive", version="v3"
        )
        self.doc_service = self._get_api_client(
            svc_acc_cred=self.svc_acc_cred,
            service="docs",
            version="v1",
            discovery_uri=DISCOVERY_DOC,
            http=self.svc_acc_cred.authorize(Http()),
        )

    @staticmethod
    def _get_api_client(
        svc_acc_cred: ServiceAccountCredentials,
        service: str,
        version: str,
        discovery_uri: str = None,
        http: httplib2.Http = None,
        num_retries=7,
    ):
        """Construct a Resource for interacting with an API of the specified provided service and version.

        Returns:
          An authenticated api client Resource connection.
        """
        kwargs = {
            "serviceName": service,
            "version": version,
            "num_retries": num_retries,
        }
        if http:
            kwargs["http"] = http
        else:
            kwargs["credentials"] = svc_acc_cred
        kwargs["discoveryServiceUrl"] = discovery_uri if discovery_uri else None

        try:
            api_client = discovery.build(**kwargs)
            return api_client
        except oauth2client.client.HttpAccessTokenRefreshError as e:
            raise RuntimeError(f"Error occurred. Message: {e.message}")
        except HttpError as e:
            reason = str(e._get_reason).split('"')[-2]
            raise RuntimeError(f"Error occurred. Reason: {reason}")


class GoogleDocsFile:
    """Class that provides helpers to interact with a Google Document.

    Args:
        file_id: Google Document file id.
        docs_service: Resource to interact with the Google Documents.

    Attributes:
        file_id: ID of Google Documents File.
        docs_service: Resource to interact with the Google Documents.

    Returns:
        A Google Docs file object with methods for interacting with Google Docs file.

    """

    def __init__(self, file_id: str, docs_service: discovery.Resource):
        """Initialize Google Documents file."""
        self.file_id = file_id
        self.docs_service = docs_service

    def get_file_content(
        self,
    ) -> t.List[t.Dict[t.Union[str, t.List[t.Dict[str, str]], t.Dict[str, str]], str]]:
        """Retrieve content of Google Document file."""
        body_obj = (
            self.docs_service.documents()
            .get(documentId=self.file_id, fields="body")
            .execute(num_retries=10)
        )
        doc_content = body_obj.get("body", {}).get("content", {})
        if not doc_content:
            raise ValueError(f"Unable to retrieve the content of file: {self.file_id}")
        return doc_content

    def update_document_request(
        self, request_call: t.List[t.Dict]
    ) -> t.Dict[t.Union[str, t.List[t.Dict[str, str]], t.Dict[str, str]], str]:
        """Update Google Document with specified request call."""
        try:
            result = (
                self.docs_service.documents()
                .batchUpdate(documentId=self.file_id, body={"requests": request_call})
                .execute()
            )
        except HttpError as err:
            raise RuntimeError(
                f"Exception occurred with HttpError error status: {err.resp.status}."
                f"Details: {utils.parse_error_message(err.error_details)}"
            )

        return result

    def find_index_range_by_paragraph_style(
        self, search_style_type: str
    ) -> t.List[t.Optional[t.Dict[str, int]]]:
        """Get the index range of the provided paragraph style.

        Args:
            search_style_type (str): Paragraph style type on Google Documents.

        Returns:
            (list[dict]) List of the index range that matches the specified style type.
        """
        mod_search_style_type = utils.validate_docs_obj(
            search_style_type, "PARAGRAPH_STYLE"
        )

        range_list: t.List[t.Optional[t.Dict[str, int]]] = list()
        doc_obj_content = self.get_file_content()
        for section in doc_obj_content:
            for v in section.values():
                if isinstance(v, dict) and all(
                    i in list(v.keys()) for i in ["elements", "paragraphStyle"]
                ):
                    p_style = v.get("paragraphStyle", {})
                    if mod_search_style_type == p_style.get("namedStyleType", ""):
                        elements_ = v.get("elements", [])
                        for e_ in elements_:
                            if e_.get("textRun"):
                                content = e_.get("textRun", {}).get("content", "")
                                # Avoid including empty spaces
                                if content != "\n":
                                    index_range = {
                                        "startIndex": section.get("startIndex"),
                                        "endIndex": section.get("endIndex"),
                                    }
                                    range_list.append(index_range)
        return range_list

    def find_index_range_by_content(
        self, search_content: str
    ) -> t.List[t.Optional[t.Dict[str, int]]]:
        """Get index range of provided text content.

        Args:
            search_content (str): Text that will be finding within the Google Document.

        Returns:
            (list[dict]) List of the index range that matches the specified content.
        """
        esc_search_content = re.escape(search_content.strip())

        regexp = re.compile(esc_search_content)
        range_list: t.List[t.Optional[t.Dict[str, int]]] = list()
        doc_obj_content = self.get_file_content()
        for section in doc_obj_content:
            for v in section.values():
                if isinstance(v, dict) and "elements" in v.keys():
                    elements = v.get("elements", [])
                    for e in elements:
                        for paragraph_element, value in e.items():
                            if paragraph_element == "textRun":
                                content = value.get("content").strip()
                                if bool(regexp.search(content)):
                                    index_range = {
                                        "startIndex": section.get("startIndex"),
                                        "endIndex": section.get("endIndex"),
                                    }
                                    range_list.append(index_range)

        return range_list

    def find_index_range_by_paragraph_element(
        self, targeted_paragraph_element: str
    ) -> t.List[t.Optional[t.Dict[str, int]]]:
        """Get the index range of the specified element within provided Google Document.

        Args:
            targeted_paragraph_element (str): Value of Google Docs ParagraphElement.

        Returns:
            (list[dict]) List of the index range that matches the specified element.
        """
        mod_targeted_paragraph_element = utils.validate_docs_obj(
            targeted_paragraph_element, "PARAGRAPH_ELEMENTS"
        )

        range_list: t.List[t.Optional[t.Dict[str, int]]] = list()

        doc_obj_content = self.get_file_content()

        for section in doc_obj_content:
            for v in section.values():
                if isinstance(v, dict) and "elements" in v.keys():
                    elements = v.get("elements", [])
                    for e in elements:
                        for paragraph_element, value in e.items():
                            if paragraph_element == mod_targeted_paragraph_element:
                                index_range = {
                                    "startIndex": section.get("startIndex"),
                                    "endIndex": section.get("endIndex"),
                                }

                                range_list.append(index_range)
        return range_list


class GoogleDriveFolder:
    """Class that provides helpers to interact with a Google Drive Folder.

    Args:
        folder_id: Google Drive Folder ID.
        api_client: Resource to interact with the Google Documents

    Attributes:
        api_client: GoogleAPIClient object that contains Google Service Account
        credentials and API client to access Google Drive and Google Documents.
        folder_cred: Resource to interact with the Google Drive Folder.
        folder_id: ID of Google Drive Folder.

    Returns:
        A Google Drive Folder object with methods for interacting with Google Docs file.

    """

    def __init__(self, folder_id: str, api_client: GoogleAPIClient):
        """Initialize Google Drive Folder."""
        self.api_client = api_client
        self.folder_cred = api_client.drive_service
        self.folder_id = folder_id

    def upload_file(
        self,
        file_name: str,
        file_path: t.Union[Path, str],
    ) -> t.Optional[GoogleDocsFile]:
        """Upload file to Google Drive folder.

        Args:
            file_name (str): File name that is uploading to Google Drive.
            file_path (Union[Path, str]): Path to the file that will be uploaded.

        Returns:
            A GoogleDocsFile object.
        """
        # Upload a file
        file_metadata = {
            "name": file_name,
            "parents": [self.folder_id],
            "mimeType": "application/vnd.google-apps.document",
        }

        media_content = MediaFileUpload(
            file_path,
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            resumable=True,
        )
        retried = False
        uploaded = False
        while not uploaded:
            try:
                file = (
                    self.folder_cred.files()
                    .create(
                        supportsTeamDrives=True,
                        body=file_metadata,
                        media_body=media_content,
                        fields="id",
                    )
                    .execute(num_retries=10)
                )

            except HttpError as err:
                # If the error is a rate limit or connection error,
                # wait and try again.
                if err.resp.status in [403, 500, 503]:
                    if retried:
                        raise RuntimeError(
                            f"Retried once. Unable to retry again. Details: {utils.parse_error_message(err.error_details)}"
                        ) from err
                    else:
                        retried = True
                        time.sleep(5)
                        raise RuntimeError(
                            f"Error status: {err.resp.status}; Reason: {err.reason}"
                        )
                elif err.resp.status == 404:
                    raise ValueError(
                        f"Error status: {err.resp.status}; Reason: {err.reason}. Please check to "
                        f"verify the folder ID and/or your permission on the folder. "
                    )
                else:
                    raise RuntimeError(
                        f"Uncaught HttpError error status: {err.resp.status}."
                    ) from err
            except Exception as exc:
                raise RuntimeError("Uncaught Exception.") from exc
            else:
                uploaded = True
                file_id = file.get("id")
                return GoogleDocsFile(file_id, self.api_client.doc_service)
        return None

    def get_file_list_from_folder(self, sub_folder_id: str = None) -> t.List[t.Dict]:
        """Retrieve a list of file object that is stored in the Google Drive Folder."""
        file_list = list()
        # Access the files in folder
        if not sub_folder_id:
            # find files in the base level of the shared drive folder if not provided
            sub_folder_id = self.folder_id
        query = f"'{sub_folder_id}' in parents and mimeType = 'application/vnd.google-apps.file'"

        try:
            response = (
                self.folder_cred.files()
                .list(
                    q=query,
                    corpora="drive",
                    driveId=self.folder_id,
                    includeItemsFromAllDrives=True,
                    supportsAllDrives=True,
                )
                .execute()
            )

            file_list = response.get("files")
            nextPageToken = response.get("nextPageToken")

            while nextPageToken:
                response = (
                    self.folder_cred.files()
                    .list(
                        q=query,
                        corpora="drive",
                        driveId=self.folder_id,
                        includeItemsFromAllDrives=True,
                        supportsAllDrives=True,
                    )
                    .execute()
                )
                file_list.extend(response.get("files"))
                nextPageToken = response.get("nextPageToken")
        except HttpError as e:
            reason = str(e._get_reason).split('"')[-2]
            raise RuntimeError(f"Error occurred. Reason: {reason}")
        except Exception as exc:
            raise Exception("Uncaught Exception.") from exc

        return file_list

    def list_folders_in_folder(self, sub_folder_id: str = None):
        folders_list = list()
        # Access the files in folder
        if not sub_folder_id:
            # find files in original shared drive or shared folder if not provided
            sub_folder_id = self.folder_id

        query = f"'{sub_folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder'"

        page_token = None

        while True:
            try:
                response = (
                    self.folder_cred.files()
                    .list(
                        q=query,
                        corpora="drive",
                        driveId=self.folder_id,
                        includeItemsFromAllDrives=True,
                        supportsAllDrives=True,
                        fields="nextPageToken, " "files(id, name, mimeType)",
                        pageToken=page_token,
                    )
                    .execute()
                )
                folders_list.extend(response.get("files", []))
                page_token = response.get("nextPageToken", None)
                if page_token is None:
                    break
            except HttpError as e:
                reason = str(e._get_reason).split('"')[-2]
                raise RuntimeError(f"Error occurred. Reason: {reason}")
            except Exception as exc:
                raise Exception("Uncaught Exception.") from exc

        return folders_list

    def get_file_id_by_name(self, file_name: str, sub_folder_id: str = None) -> list:
        """Retrieve file ID based on provided file name."""
        # if sub_folder_id not provided it will look at the base level of the shared drive/folder (self.folder_id)
        file_list = self.get_file_list_from_folder(sub_folder_id)
        f_ids = list()
        for file in file_list:
            if file.get("name") == file_name:
                f_id = file.get("id")
                f_ids.append(f_id)
        return f_ids

    def delete_file_by_id(self, file_id: str) -> bool:
        """Delete file based on file id."""
        try:
            self.folder_cred.files().delete(
                fileId=file_id, supportsTeamDrives=True
            ).execute(num_retries=5)
        except err.HttpError as httperr:
            raise RuntimeError(
                f"Error occurred with {err.resp.status} status code; Reason: {err.reason}. "
            ) from httperr
        return True
