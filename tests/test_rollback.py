import pytest
from unittest.mock import patch
from rollback import rollback, execute_command

def test_rollback_command():
    """Test rollback command execution."""
    mock_config = {
        'deployment': {
            'rollback': [
                {'name': 'Rollback Test', 'command': 'echo rollback'}
            ]
        }
    }
    
    # This should not raise any exceptions
    rollback(mock_config)

def test_execute_rollback_command():
    """Test individual rollback command execution."""
    result = execute_command('echo rollback test')
    assert 'rollback test' in result

    # Input Config
{
    'deployment': {
        'rollback': [
            {'name': 'Undo Changes', 'command': 'git reset --hard'}
        ]
    }
}

# Expected Outcomes:
# - Rollback command executes
# - Step name printed
# - No critical failures
# - Graceful error handling if command fails