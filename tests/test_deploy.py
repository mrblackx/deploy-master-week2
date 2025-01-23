import pytest
from unittest.mock import patch
import subprocess
from deploy import execute_command, send_notification, deploy

def test_execute_command_success():
    """Test successful command execution."""
    result = execute_command('echo test')
    assert 'test' in result

def test_execute_command_failure():
    """Test command execution with a failing command."""
    with pytest.raises(subprocess.CalledProcessError):
        execute_command('invalid_command_that_does_not_exist')

def test_send_notification():
    """Test notification sending."""
    with patch('builtins.print') as mock_print:
        send_notification('test@example.com', 'Test Message')
        mock_print.assert_called_once_with('Notification to test@example.com: Test Message')

def test_deploy_successful_scenario():
    """Test deployment with successful steps."""
    mock_config = {
        'deployment': {
            'steps': [
                {'name': 'Install Dependencies', 'command': 'pip install'},
                {'name': 'Run Tests', 'command': 'pytest'}
            ],
            'rollback': [
                {'name': 'Cleanup', 'command': 'rm -rf temp_files'}
            ],
            'notifications': {'email': 'devops@example.com'}
        }
    }

    with patch('deploy.execute_command', return_value="Success"), \
         patch('deploy.send_notification') as mock_notify:
        deploy(mock_config)
        mock_notify.assert_called_with('devops@example.com', 'Deployment successful')

def test_deploy_with_partial_failures():
    """Test deployment with some steps failing."""
    mock_config = {
        'deployment': {
            'steps': [
                {'name': 'Successful Step', 'command': 'echo success'},
                {'name': 'Failing Step', 'command': 'invalid_command'}
            ],
            'rollback': [
                {'name': 'Rollback', 'command': 'echo rollback'}
            ],
            'notifications': {'email': 'alert@example.com'}
        }
    }

    with patch('deploy.execute_command', side_effect=[
        "Success",  # First step succeeds
        subprocess.CalledProcessError(1, 'invalid_command', stderr='Command not found')  # Second step fails
    ]), \
         patch('deploy.perform_rollback') as mock_rollback, \
         patch('deploy.send_notification') as mock_notify:
        
        with pytest.raises(subprocess.CalledProcessError):
            deploy(mock_config)

        mock_rollback.assert_called_once()
        
        # More flexible assertion
        assert mock_notify.call_args[0][0] == 'alert@example.com'
        
        # Check that the notification message contains key components
        notification_message = mock_notify.call_args[0][1]
        assert 'Deployment failed' in notification_message
        assert 'invalid_command' in notification_message
        assert 'returned non-zero exit status' in notification_message
