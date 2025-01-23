import yaml
from typing import Dict, Any

def parse_config(file_path: str) -> Dict[str, Any]:
    """
    Parses a YAML configuration file and returns the parsed object.
    
    Args:
        file_path (str): Path to the YAML configuration file.
    
    Returns:
        Dict[str, Any]: Parsed configuration object.
    
    Raises:
        ValueError: If file path is invalid or parsing fails.
    """
    if not file_path or not isinstance(file_path, str):
        raise ValueError('Invalid file path. Please provide a valid YAML file path.')

    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except (IOError, yaml.YAMLError) as error:
        raise ValueError(f'Error parsing configuration: {str(error)}')
