"""Utilities for accessing Google API."""
import copy
import re
import typing as t
from pathlib import Path

from oauth2client.service_account import ServiceAccountCredentials

# Elements and Styling that represent paragraph in for Google Docs.
DOCS_OBJ = {
    "PARAGRAPH_ELEMENTS": [
        "autoText",
        "columnBreak",
        "equation",
        "footnoteReference",
        "horizontalRule",
        "inlineObjectElement",
        "pageBreak",
        "textRun",
    ],
    "PARAGRAPH_STYLE": [
        "NAMED_STYLE_TYPE_UNSPECIFIED",
        "NORMAL_TEXT",
        "TITLE",
        "SUBTITLE",
        "HEADING_1",
        "HEADING_2",
        "HEADING_3",
        "HEADING_4",
        "HEADING_5",
        "HEADING_6",
    ],
}


def login(
    service_cred_path: t.Union[Path, str], scopes: t.Union[t.List[str], str]
) -> ServiceAccountCredentials:
    """Login to Google API via Service Account credentials."""
    # The credentials must be a Service Account JSON file, which can be
    # created and downloaded using the Google Cloud Platform console. See
    # https://cloud.google.com/storage/docs/authentication#generating-a-private-key
    service_cred_path = Path(service_cred_path)
    # Verify path is valid
    if not service_cred_path.is_file():
        raise FileNotFoundError(
            f"{service_cred_path} is not a file and does not exist."
        )

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        service_cred_path, scopes=scopes
    )
    return creds


def parse_error_message(err_details: t.List[t.Dict[str, str]]) -> t.Optional[str]:
    """Parse error message from GoogleAPI call."""
    msg: list = list()
    for details in err_details:
        if details.get("message"):
            msg.append(details.get("message"))

    return " ".join([m.strip() for m in msg])


def validate_docs_obj(search_obj: str, obj_category: str) -> t.Optional[str]:
    """Validate requests for specify google docs object category."""
    if obj_category not in list(DOCS_OBJ.keys()):
        raise ValueError(
            f"{obj_category} is not valid. Only {', '.join(DOCS_OBJ.keys())} accepted"
        )

    obj_list = DOCS_OBJ.get(obj_category)
    valid = False

    corrected_search_obj = None
    for i in obj_list:  # type: ignore
        if bool(re.fullmatch(i, search_obj, re.I)):
            corrected_search_obj = i

    if not valid and not corrected_search_obj:
        raise ValueError(
            f"{search_obj} is an invalid style type. "
            f"Only the following value is allowed (case sensitive):{str(obj_list)[1:-1]}"
        )
    return corrected_search_obj


def replace_text(targeted_text: str, replacement_text: str) -> t.Dict:  # noqa: D103
    return {
        "replaceAllText": {
            "containsText": {"text": targeted_text, "matchCase": "true"},
            "replaceText": replacement_text,
        }
    }


def update_paragraph_style(
    range_dict: t.Dict, paragraph_style_dict: t.Dict
) -> t.Dict:  # noqa: D103
    updated_range_dict = validate_range_dict(range_dict, "range")
    # Populate fields for paragraph style
    fields = populate_fields_string(paragraph_style_dict.keys())
    return {
        "updateParagraphStyle": {
            "range": updated_range_dict,
            "paragraphStyle": paragraph_style_dict,
            "fields": fields,
        }
    }


def update_text_style(
    text_style_dict: t.Dict, range_dict: t.Dict
) -> t.Dict:  # noqa: D103
    updated_range_dict = validate_range_dict(range_dict, "range")
    # Populate fields for paragraph style
    fields = populate_fields_string(text_style_dict.keys())

    return {
        "updateTextStyle": {
            "range": updated_range_dict,
            "textStyle": text_style_dict,
            "fields": fields,
        }
    }


def update_document_style(doc_style_dict: t.Dict) -> t.Dict:  # noqa: D103
    """Used for header."""
    fields = populate_fields_string(doc_style_dict.keys())

    return {"updateDocumentStyle": {"documentStyle": doc_style_dict, "fields": fields}}


def insert_page_break(index: t.Union[int, str]) -> t.Dict:  # noqa: D103
    try:
        mod_index = int(index)
    except ValueError:
        raise ValueError(
            f"Invalid index. Expecting index to be number. Got {index} instead."
        )
    return {
        "insertPageBreak": {
            "location": {"index": mod_index},
        }
    }


def insert_text(
    index: t.Union[int, str], doc_content: str, format_str: tuple = ()
) -> t.Dict:  # noqa: D103
    try:
        mod_index = int(index)
    except ValueError:
        raise ValueError(
            f"Invalid index. Expecting index to be number. Got {index} instead."
        )
    assert isinstance(
        format_str, tuple
    ), f"Expecting {format_str} to be Tuple instead of {type(format_str)}"
    format_count = re.findall("{}", doc_content)
    if format_count:
        assert len(format_count) == len(format_str), (
            f"Found {len(format_count)} "
            f"format string but only {len(format_str)} was provided"
        )

    return {
        "insertText": {
            "location": {
                "index": mod_index,
            },
            "text": doc_content.format(*format_str),
        }
    }


def delete_content(range_dict: t.Dict) -> t.Dict:  # noqa: D103
    updated_range_dict = validate_range_dict(range_dict, "range")

    return {"deleteContentRange": {"range": updated_range_dict}}


def populate_fields_string(dict_keys):  # noqa: D103
    """Populate requests fields for GoogleAPI call."""
    return ",".join(list(dict_keys))


def validate_range_dict(range_dict: t.Dict, index_type: str) -> t.Dict:  # noqa: D103
    """Validate range dictionary for GoogleAPI request."""
    if index_type == "range":
        dict_keys = ["startIndex", "endIndex"]
    else:
        raise ValueError(
            f"Invalid index type. Expecting index or range but got {index_type}."
        )
    range_dict_copy = copy.deepcopy(range_dict)
    for k, v in range_dict.items():
        if k not in dict_keys:
            raise ValueError(
                f"{k} is not a valid key value. Only accept startIndex or endIndex. (case sensitive) "
            )
        if not isinstance(v, int):
            try:
                mod_v = int(v)
            except ValueError:
                raise ValueError(
                    f"Invalid index. Expecting index to be number. Got {v} instead."
                )
            else:
                range_dict_copy[k] = mod_v

    return range_dict_copy
