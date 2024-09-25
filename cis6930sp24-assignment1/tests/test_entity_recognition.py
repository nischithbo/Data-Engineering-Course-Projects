from unittest.mock import Mock, create_autospec
import spacy
from spacy.tokens import Doc, Span
from assignment1.entityresolver import find_all_date, find_all_address, find_all_phone_numbers, find_all_names

gcp_entities = [{'name': 'John Doe', 'type': 'PERSON', 'metadata': {}, 'salience': 0.6883193, 'mentions': [{'text': {'content': 'John Doe', 'beginOffset': 19}, 'type': 'PROPER'}]}, {'name': 'call', 'type': 'OTHER', 'metadata': {}, 'salience': 0.08096119, 'mentions': [{'text': {'content': 'call', 'beginOffset': 90}, 'type': 'COMMON'}]}, {'name': 'Anytown', 'type': 'LOCATION', 'metadata': {}, 'salience': 0.048171338, 'mentions': [{'text': {'content': 'Anytown', 'beginOffset': 60}, 'type': 'PROPER'}]}, {'name': 'CA', 'type': 'LOCATION', 'metadata': {'mid': '/m/01n7q', 'wikipedia_url': 'https://en.wikipedia.org/wiki/California'}, 'salience': 0.048171338, 'mentions': [{'text': {'content': 'CA', 'beginOffset': 69}, 'type': 'PROPER'}]}, {'name': 'Maple Street', 'type': 'LOCATION', 'metadata': {}, 'salience': 0.04759771, 'mentions': [{'text': {'content': 'Maple Street', 'beginOffset': 46}, 'type': 'PROPER'}]}, {'name': 'appointment', 'type': 'OTHER', 'metadata': {}, 'salience': 0.046882592, 'mentions': [{'text': {'content': 'appointment', 'beginOffset': 148}, 'type': 'COMMON'}]}, {'name': 'phone number', 'type': 'OTHER', 'metadata': {}, 'salience': 0.025026044, 'mentions': [{'text': {'content': 'phone number', 'beginOffset': 105}, 'type': 'COMMON'}]}, {'name': 'US', 'type': 'LOCATION', 'metadata': {'wikipedia_url': 'https://en.wikipedia.org/wiki/United_States', 'mid': '/m/09c7w0'}, 'salience': 0.014870489, 'mentions': [{'text': {'content': 'US', 'beginOffset': 102}, 'type': 'PROPER'}]}, {'name': 'March 15, 2023', 'type': 'DATE', 'metadata': {'month': '3', 'day': '15', 'year': '2023'}, 'salience': 0, 'mentions': [{'text': {'content': 'March 15, 2023', 'beginOffset': 3}, 'type': 'TYPE_UNKNOWN'}]}, {'name': 'CA 90210', 'type': 'ADDRESS', 'metadata': {'country': 'US', 'broad_region': 'California', 'postal_code': '90210'}, 'salience': 0, 'mentions': [{'text': {'content': 'CA 90210', 'beginOffset': 69}, 'type': 'TYPE_UNKNOWN'}]}, {'name': '2023', 'type': 'NUMBER', 'metadata': {'value': '2023'}, 'salience': 0, 'mentions': [{'text': {'content': '2023', 'beginOffset': 13}, 'type': 'TYPE_UNKNOWN'}]}, {'name': '90210', 'type': 'NUMBER', 'metadata': {'value': '90210'}, 'salience': 0, 'mentions': [{'text': {'content': '90210', 'beginOffset': 72}, 'type': 'TYPE_UNKNOWN'}]}, {'name': '1234', 'type': 'NUMBER', 'metadata': {'value': '1234'}, 'salience': 0, 'mentions': [{'text': {'content': '1234', 'beginOffset': 41}, 'type': 'TYPE_UNKNOWN'}]}, {'name': '15', 'type': 'NUMBER', 'metadata': {'value': '15'}, 'salience': 0, 'mentions': [{'text': {'content': '15', 'beginOffset': 9}, 'type': 'TYPE_UNKNOWN'}]}, {'name': '555', 'type': 'NUMBER', 'metadata': {'value': '555'}, 'salience': 0, 'mentions': [{'text': {'content': '555', 'beginOffset': 119}, 'type': 'TYPE_UNKNOWN'}]}, {'name': '123', 'type': 'NUMBER', 'metadata': {'value': '123'}, 'salience': 0, 'mentions': [{'text': {'content': '123', 'beginOffset': 124}, 'type': 'TYPE_UNKNOWN'}]}, {'name': '4567', 'type': 'NUMBER', 'metadata': {'value': '4567'}, 'salience': 0, 'mentions': [{'text': {'content': '4567', 'beginOffset': 128}, 'type': 'TYPE_UNKNOWN'}]}]
input_string = "On March 15, 2023, John Doe, residing at 1234 Maple Street, Anytown, CA 90210, received a call at his US phone number (555) 123-4567 to confirm his appointment."
# Function to create a mock Span


def mock_span(text, label):
    span = create_autospec(Span)
    span.text = text
    span.label_ = label
    return span


def mock_doc_with_entities():
    # Load Spacy language model to use its vocab for creating a Doc
    # This is necessary because Spacy checks for Vocab in some operations
    nlp = spacy.blank("en")

    # Create a mock for the Doc object
    mock_doc = create_autospec(Doc, instance=True, vocab=nlp.vocab)

    # Define the entities you want to mock
    entities = [
        mock_span("John Doe", "PERSON"),
        mock_span("March 15, 2023", "DATE"),
        mock_span("1234 Maple Street, Anytown, CA 90210", "GPE"),
        mock_span("(555) 123-4567", "PHONE")
    ]

    # Use the mocked entities in the Doc mock
    mock_doc.ents = entities

    return mock_doc


mock_doc = mock_doc_with_entities()


def test_name_recognition():
    names = find_all_names(input_string, mock_doc, gcp_entities)
    assert names == ['John Doe']


def test_address_recognition():
    address = find_all_address(input_string, mock_doc, gcp_entities)
    assert sorted(address) == sorted(['US', 'Anytown', '1234 Maple Street, Anytown, CA 90210', 'CA', 'Maple Street'])


def test_phone_number_recognition():
    phone_numbers = find_all_phone_numbers(input_string, mock_doc, gcp_entities)
    assert phone_numbers == ['(555) 123-4567']


def test_date_recognition():
    dates = find_all_date(input_string, mock_doc, gcp_entities)
    assert dates == ['March 15, 2023']



