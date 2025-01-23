from git import Repo

def get_latest_changes(repo_path: str = '.'):
    """
    Pull latest changes from the repository.
    
    Args:
        repo_path (str, optional): Path to the repository. Defaults to current directory.
    """
    try:
        repo = Repo(repo_path)
        origin = repo.remotes.origin
        origin.pull()
        print("Pulled latest changes successfully.")
    except Exception as e:
        print(f"Error pulling latest changes: {e}")
