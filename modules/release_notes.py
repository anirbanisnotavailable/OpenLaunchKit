import git

def generate_changelog(repo_path: str):
    """
    Reads recent git commits and formats them.
    """
    try:
        repo = git.Repo(repo_path)
        commits = list(repo.iter_commits('master', max_count=5))
        
        log = "### Recent Updates\n\n"
        for commit in commits:
            log += f"- {commit.summary}\n"
            
        log += "\n*Pro-tip: Connect to Ollama to translate these technical commits into user-friendly update notes!*"
        return log
    except git.exc.InvalidGitRepositoryError:
        return "⚠️ Invalid Git repository path."
    except Exception as e:
        return f"⚠️ Error reading repository: {e}"
