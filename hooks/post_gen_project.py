#!/usr/bin/env python3
"""
Post-generation hook for Cookiecutter Django Base template.

This hook performs setup tasks after the project is generated,
such as removing template-specific files and initializing the project.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def remove_template_files():
    """Remove files that are specific to the template, not the generated project."""
    template_files = [
        "teste.txt",
        "commit.sh",
        "cookiecutter.json",
        "hooks/",
        "EVOLUTION_GUIDE.md",
        "project_improvements.md",
        "project_standards.md",
        "RELEASE_NOTES_v2.1.0.md",
    ]
    
    for file_path in template_files:
        if os.path.exists(file_path):
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print(f"🗑️  Removed directory: {file_path}")
            else:
                os.remove(file_path)
                print(f"🗑️  Removed file: {file_path}")


def generate_secret_key():
    """Generate a secure SECRET_KEY for Django."""
    import secrets
    import string
    
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*(-_=+)"
    secret_key = ''.join(secrets.choice(alphabet) for _ in range(50))
    return secret_key


def update_env_file():
    """Update the .env file with generated values."""
    env_file = Path(".env")
    if env_file.exists():
        # Read current content
        content = env_file.read_text()
        
        # Replace placeholder values
        secret_key = generate_secret_key()
        content = content.replace("change-me-in-production-please-use-a-secure-key", secret_key)
        content = content.replace("your-oauth2-client-id", f"{{ cookiecutter.project_slug }}-client-id")
        
        # Write back
        env_file.write_text(content)
        print("🔐 Updated .env file with secure values")


def initialize_git_repo():
    """Initialize git repository if requested."""
    if "{{ cookiecutter.use_github_actions }}" == "y":
        try:
            subprocess.run(["git", "init"], check=True, capture_output=True)
            subprocess.run(["git", "add", "."], check=True, capture_output=True)
            subprocess.run([
                "git", "commit", "-m", 
                "🎉 Initial commit: {{ cookiecutter.project_name }} setup"
            ], check=True, capture_output=True)
            print("📦 Initialized git repository")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Warning: Could not initialize git repository: {e}")


def install_pre_commit_hooks():
    """Install pre-commit hooks if requested."""
    if "{{ cookiecutter.use_pre_commit }}" == "y":
        try:
            subprocess.run([
                "python", "-m", "pip", "install", "pre-commit"
            ], check=True, capture_output=True)
            subprocess.run([
                "pre-commit", "install"
            ], check=True, capture_output=True)
            print("🔧 Installed pre-commit hooks")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Warning: Could not install pre-commit hooks: {e}")


def create_oauth_application():
    """Create OAuth2 application if OAuth is enabled."""
    if "{{ cookiecutter.include_oauth }}" == "y":
        try:
            # This would be done via Django management command
            print("🔐 OAuth2 application will be created on first run")
        except Exception as e:
            print(f"⚠️  Warning: Could not create OAuth2 application: {e}")


def update_readme():
    """Update README with project-specific information."""
    readme_file = Path("README.md")
    if readme_file.exists():
        content = readme_file.read_text()
        
        # Replace template placeholders
        content = content.replace("Django Base", "{{ cookiecutter.project_name }}")
        content = content.replace("django_base", "{{ cookiecutter.project_slug }}")
        content = content.replace("luderibeiro", "{{ cookiecutter.github_username }}")
        
        readme_file.write_text(content)
        print("📖 Updated README.md with project information")


def run_initial_migrations():
    """Run initial Django migrations if possible."""
    try:
        # This would be done via Django management command
        print("🗄️  Initial migrations will be run on first setup")
    except Exception as e:
        print(f"⚠️  Warning: Could not run initial migrations: {e}")


def main():
    """Main post-generation function."""
    print("🚀 Setting up {{ cookiecutter.project_name }}...")
    
    # Change to the generated project directory
    project_dir = Path("{{ cookiecutter.project_slug }}")
    if project_dir.exists():
        os.chdir(project_dir)
        print(f"📁 Changed to project directory: {project_dir}")
    
    # Perform setup tasks
    remove_template_files()
    update_env_file()
    update_readme()
    initialize_git_repo()
    install_pre_commit_hooks()
    create_oauth_application()
    run_initial_migrations()
    
    print("\n✅ Project setup completed!")
    print("\n📋 Next steps:")
    print("1. cd {{ cookiecutter.project_slug }}")
    print("2. python -m venv venv")
    print("3. source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
    print("4. pip install -r project/requirements.txt")
    print("5. make setup")
    print("6. make run")
    print("\n🎉 Happy coding!")


if __name__ == "__main__":
    main()
