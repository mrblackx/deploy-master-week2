import subprocess
import typing
import smtplib
from email.mime.text import MIMEText
import yaml
import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
LOG_DIR = 'logs'
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logging():
    """
    Set up comprehensive logging with file and console output.
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Generate unique log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(LOG_DIR, f'deployment_{timestamp}.log')
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),  # Log to file
            logging.StreamHandler()                           # Log to console
        ]
    )
    
    return logging.getLogger(__name__)

# Create a global logger
logger = setup_logging()

def load_config(file_path):
    """
    Load deployment configuration from YAML file.
    
    Args:
        file_path (str): Path to the configuration file.
    
    Returns:
        dict: Deployment configuration
    """
    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
            logger.info(f"Configuration loaded successfully from {file_path}")
            return config
    except Exception as e:
        logger.error(f"Failed to load configuration: {e}")
        raise

# Load configuration
try:
    deployment_config = load_config('deployment_config.yaml')
except Exception as e:
    logger.error(f"Deployment configuration could not be loaded: {e}")
    deployment_config = {}

def send_notification(email: str, message: str) -> None:
    """
    Send email notification with comprehensive logging.
    
    Args:
        email (str): Recipient email address.
        message (str): Notification message.
    """
    try:
        logger.info(f"Sending notification to {email}")
        logger.info(f"Notification message: {message}")
        
        # Simulate email sending for demonstration
        print(f"Notification to {email}: {message}")
        
        logger.info("Notification sent successfully")
    except Exception as e:
        logger.error(f"Failed to send notification: {e}")

def perform_rollback(rollback_steps: typing.List[typing.Dict[str, str]]) -> None:
    """
    Perform rollback steps with detailed logging.
    
    Args:
        rollback_steps (List[Dict]): List of rollback steps.
    """
    logger.warning("Initiating rollback process")
    
    for step in rollback_steps:
        try:
            logger.info(f"Executing rollback step: {step['name']}")
            output = execute_command(step['command'])
            logger.info(f"Rollback step '{step['name']}' completed successfully")
        except Exception as error:
            logger.error(f"Rollback step '{step['name']}' failed: {error}")

def execute_command(command: str) -> str:
    """
    Execute a shell command with comprehensive logging.
    
    Args:
        command (str): Command to execute.
    
    Returns:
        str: Command output.
    
    Raises:
        subprocess.CalledProcessError: If the command fails.
    """
    try:
        logger.info(f"Executing command: {command}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        logger.info(f"Command executed successfully: {command}")
        logger.info(f"Command output: {result.stdout}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {command}")
        logger.error(f"Error details: {e.stderr}")
        raise

def deploy(config: typing.Dict[str, typing.Any]) -> None:
    """
    Deploy application with comprehensive logging.
    
    Args:
        config (Dict[str, Any]): Deployment configuration.
    """
    logger.info("Starting deployment process")
    
    deployment_config = config.get('deployment', {})
    steps = deployment_config.get('steps', [])
    rollback_steps = deployment_config.get('rollback', [])
    notification_email = deployment_config.get('notifications', {}).get('email')

    try:
        for step in steps:
            logger.info(f"Starting step: {step['name']}")
            output = execute_command(step['command'])
            logger.info(f"Step '{step['name']}' completed: {output}")

        if notification_email:
            send_notification(notification_email, 'Deployment successful')
        
        logger.info("Deployment completed successfully")

    except subprocess.CalledProcessError as e:
        logger.error("Deployment encountered issues")
        logger.error(f"Failed step details: {e}")
        
        perform_rollback(rollback_steps)
        
        if notification_email:
            send_notification(notification_email, f'Deployment failed: {e}')
        
        raise

# Optional: Main execution block
if __name__ == "__main__":
    try:
        deploy(deployment_config)
    except Exception as e:
        logger.critical(f"Deployment process failed: {e}")
