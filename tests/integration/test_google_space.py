import unittest
from unittest.mock import patch, MagicMock
from google_space import send_google_space_message

class TestGoogleSpaceIntegration(unittest.TestCase):

    @patch('google_space.get_integration_config')
    @patch('google_space.requests.post')
    def test_send_google_space_message_success(self, mock_post, mock_get_config):
        # Mock the configuration
        mock_get_config.return_value = {'webhook_url': 'https://example.com/webhook'}
        
        # Mock the response from requests.post
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"success": True}
        mock_post.return_value = mock_response

        # Call the function
        response = send_google_space_message("Test message")

        # Assertions
        mock_get_config.assert_called_once_with('google_space')
        mock_post.assert_called_once_with(
            'https://example.com/webhook',
            json={"text": "Test message"},
            headers={'Content-Type': 'application/json'}
        )
        self.assertEqual(response, {"success": True})

    @patch('google_space.get_integration_config')
    @patch('google_space.requests.post')
    def test_send_google_space_message_failure(self, mock_post, mock_get_config):
        # Mock the configuration
        mock_get_config.return_value = {'webhook_url': 'https://example.com/webhook'}
        
        # Mock the response from requests.post
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response

        # Call the function and assert exception
        with self.assertRaises(Exception) as context:
            send_google_space_message("Test message")
        
        self.assertIn("Failed to send message: Bad Request", str(context.exception))

    @patch('google_space.get_integration_config')
    def test_send_google_space_message_no_config(self, mock_get_config):
        # Mock the configuration to return None
        mock_get_config.return_value = None

        # Call the function and assert exception
        with self.assertRaises(ValueError) as context:
            send_google_space_message("Test message")
        
        self.assertIn("Google Space integration is not configured.", str(context.exception))

if __name__ == '__main__':
    unittest.main()