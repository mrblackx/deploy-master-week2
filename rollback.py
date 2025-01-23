import subprocess
from typing import Dict, Any

def execute_command(command: str) -> str:
    """
    Execute a shell command.
    
    Args:
        command (str): Command to execute.
    
    Returns:
        str: Command output.
    
    Raises:
        subprocess.CalledProcessError: If command execution fails.
    """
    result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
    return result.stdout

def rollback(config: Dict[str, Any]) -> None:
    """
    Rollback deployment based on configuration.
    
    Args:
        config (Dict[str, Any]): Rollback configuration.
    """
    rollback_steps = config.get('deployment', {}).get('rollback', [])

    for step in rollback_steps:
        try:
            execute_command(step['command'])
            print(f"Rollback step '{step['name']}' completed successfully.")
        except subprocess.CalledProcessError as error:
            print(f"Rollback step '{step['name']}' failed: {error}")
