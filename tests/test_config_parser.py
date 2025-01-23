import pytest
import os
import yaml
from config_parser import parse_config

def test_parse_complete_config(tmp_path):
    """Comprehensive test for parsing a full deployment configuration."""
    test_config = {
        'deployment': {
            'environment': 'staging',
            'steps': [
                {'name': 'Install Dependencies', 'command': 'pip install -r requirements.txt'},
                {'name': 'Run Migrations', 'command': 'python manage.py migrate'}
            ],
            'rollback': [
                {'name': 'Rollback Migrations', 'command': 'python manage.py migrate --revert'}
            ],
            'notifications': {
                'email': 'devops@company.com'
            }
        }
    }
    
    # Create a temporary yaml file
    config_file = tmp_path / "deployment_config.yaml"
    with open(config_file, 'w') as f:
        yaml.safe_dump(test_config, f)
    
    # Parse the config
    parsed_config = parse_config(str(config_file))
    
    # Detailed Assertions
    assert parsed_config == test_config
    assert 'deployment' in parsed_config
    assert parsed_config['deployment']['environment'] == 'staging'
    assert len(parsed_config['deployment']['steps']) == 2
    assert parsed_config['deployment']['steps'][0]['name'] == 'Install Dependencies'
    assert 'notifications' in parsed_config['deployment']

def test_parse_minimal_config(tmp_path):
    """Test parsing a minimal valid configuration."""
    test_config = {
        'deployment': {
            'steps': [{'name': 'Minimal Step', 'command': 'echo test'}]
        }
    }
    
    config_file = tmp_path / "minimal_config.yaml"
    with open(config_file, 'w') as f:
        yaml.safe_dump(test_config, f)
    
    parsed_config = parse_config(str(config_file))
    
    assert parsed_config == test_config
    assert len(parsed_config['deployment']['steps']) == 1

def test_invalid_config_scenarios():
    """Test various invalid configuration scenarios."""
    # Test None input
    with pytest.raises(ValueError, match='Invalid file path'):
        parse_config(None)
    
    # Test non-existent file
    with pytest.raises(ValueError, match='Error parsing configuration'):
        parse_config('/nonexistent/path/config.yaml')
    
    # Test empty file path
    with pytest.raises(ValueError, match='Invalid file path'):
        parse_config('')

def test_malformed_yaml(tmp_path):
    """Test parsing a malformed YAML file."""
    malformed_yaml = """
    deployment:
      steps:
        - name: Test Step
          command: echo test
      # Intentional syntax error
      invalid_key: [
    """
    
    config_file = tmp_path / "malformed_config.yaml"
    with open(config_file, 'w') as f:
        f.write(malformed_yaml)
    
    with pytest.raises(ValueError, match='Error parsing configuration'):
        parse_config(str(config_file))