from unittest import TestCase
from unittest.mock import patch, MagicMock

from main.app import app


class Test(TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('main.utils.session', {'user_name': 'John Doe', 'email': 'john.doe@example.com'})
    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Shilpa - SWE Take Home Test', response.data)

    @patch('main.utils.session', {'user_name': 'John Doe', 'email': 'john.doe@example.com'})
    def test_detailed_log_page(self):
        response = self.app.get('/detailed_log/123')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Detailed Entry of Call', response.data)

    @patch('main.utils.anthropic_client.messages.create')
    @patch('main.utils.session', {'user_name': 'John Doe', 'email': 'john.doe@example.com'})
    def test_post_query(self, mock_create):
        mock_response = MagicMock()
        mock_response.content = [
            MagicMock(text='Mocked response', type='text')
        ]
        mock_create.return_value = mock_response
        response = self.app.post('/detailed_log/123', data=dict(question='What is the call about?'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Answer', response.data)
        self.assertIn(b'Mocked response', response.data)


if __name__ == '__main__':
    TestCase.main()