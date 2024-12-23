from unittest import TestCase
from unittest.mock import patch, MagicMock

from main.utils import format_utc_date, has_access, ask_anthropic


class TestUtils(TestCase):

    def test_format_utc_date_valid(self):
        date_str = '2023-10-22T14:30:00.000Z'
        expected = '22 October 2023 14:30'
        self.assertEqual(format_utc_date(date_str), expected)

    def test_format_utc_date_invalid(self):
        date_str = 'invalid-date'
        self.assertEqual(format_utc_date(date_str), date_str)

    @patch('main.utils.session', {'user_name': 'John Doe', 'email': 'john.doe@example.com'})
    def test_has_access_true(self):
        call = {
            'call_metadata': {
                'parties': [
                    {'name': 'John Doe', 'email': 'john.doe@example.com'}
                ]
            }
        }
        self.assertTrue(has_access(call))

    @patch('main.utils.session', {'user_name': 'John Doe', 'email': 'john.doe@example.com'})
    def test_has_access_false(self):
        call = {
            'call_metadata': {
                'parties': [
                    {'name': 'Jane Doe', 'email': 'jane.doe@example.com'}
                ]
            }
        }
        self.assertFalse(has_access(call))

    @patch('main.utils.anthropic_client.messages.create')
    def test_ask_anthropic_success(self, mock_create):
        mock_response = MagicMock()
        mock_response.content = [
            MagicMock(text='Mocked response', type='text')
        ]
        mock_create.return_value = mock_response

        question = 'What is the call about?'
        transcript = 'This is a test transcript.'
        expected = ('Mocked response', 200)
        self.assertEqual(ask_anthropic(question, transcript), expected)

    @patch('main.utils.anthropic_client.messages.create')
    def test_ask_anthropic_failure(self, mock_create):
        mock_create.side_effect = Exception('API error')

        question = 'What is the call about?'
        transcript = 'This is a test transcript.'
        expected = ('Failed to process the request. \n API error', 500)
        self.assertEqual(ask_anthropic(question, transcript), expected)


if __name__ == '__main__':
    TestCase.main()
