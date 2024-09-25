import pytest
from unittest.mock import patch, MagicMock
from assignment1.hidestring import MaskString  # Adjust the import as needed

mocked_gcp_entities = [
    {
        'name': 'University of Florida',
        'type': 'ORGANIZATION',
        'metadata': {
            'mid': '/m/0j_sncb',
            'wikipedia_url': 'https://en.wikipedia.org/wiki/University_of_Florida'
        },
        'salience': 1,
        'mentions': [
            {
                'text': {
                    'content': 'University of Florida',
                    'beginOffset': 0
                },
                'type': 'PROPER'
            }
        ]
    }
]


@patch('assignment1.hidestring.spacy.load')
@patch('assignment1.hidestring.MaskString.gcp_nlp', return_value=mocked_gcp_entities)
def test_maskstring_with_mocked_spacy_and_gcp_nlp(mock_gcp_nlp, mock_spacy_load):
    # Set up a mock for the NLP model returned by spacy.load()
    mock_nlp = MagicMock()
    mock_spacy_load.return_value = mock_nlp

    # Now, both spacy.load() and MaskString.gcp_nlp are mocked
    mask_string_obj = MaskString()
    mask_string_obj.set_input_string("University of Florida.")

    # Assertions to ensure the mocks were called
    mock_spacy_load.assert_called_once_with("en_core_web_md")
    mock_gcp_nlp.assert_called_once()


