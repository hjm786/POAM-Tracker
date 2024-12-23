import unittest
from unittest.mock import patch, MagicMock
from github import Github
from integrations.github import create_github_issue

class TestCreateGithubIssue(unittest.TestCase):

    @patch('integrations.github.get_integration_config')
    @patch('integrations.github.Github')
    def test_create_github_issue_success(self, mock_github, mock_get_integration_config):
        # Mock configuration
        mock_get_integration_config.return_value = {
            'access_token': 'fake_token',
            'repository': 'fake_user/fake_repo'
        }

        # Mock GitHub objects
        mock_repo = MagicMock()
        mock_github_instance = MagicMock()
        mock_github_instance.get_repo.return_value = mock_repo
        mock_github.return_value = mock_github_instance

        # Call the function
        title = "Test Issue"
        body = "This is a test issue."
        create_github_issue(title, body)

        # Assertions
        mock_get_integration_config.assert_called_once_with('github')
        mock_github.assert_called_once_with('fake_token')
        mock_github_instance.get_repo.assert_called_once_with('fake_user/fake_repo')
        mock_repo.create_issue.assert_called_once_with(title=title, body=body)

    @patch('integrations.github.get_integration_config')
    def test_create_github_issue_no_config(self, mock_get_integration_config):
        # Mock configuration to return None
        mock_get_integration_config.return_value = None

        # Call the function and assert it raises ValueError
        with self.assertRaises(ValueError) as context:
            create_github_issue("Test Issue", "This is a test issue.")
        
        self.assertEqual(str(context.exception), "GitHub integration is not configured.")

if __name__ == '__main__':
    unittest.main()