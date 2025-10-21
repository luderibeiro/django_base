#!/usr/bin/env python3
"""
Pre-generation hook for Cookiecutter Django Base template.

This hook validates the user inputs and performs any necessary setup
before the project is generated.
"""

import re
import sys
from pathlib import Path


def validate_project_slug(slug):
    """Validate that the project slug follows Python naming conventions."""
    if not re.match(r'^[a-z][a-z0-9_]*$', slug):
        print("❌ Error: Project slug must start with a letter and contain only lowercase letters, numbers, and underscores.")
        sys.exit(1)
    return slug


def validate_email(email):
    """Validate email format."""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        print("❌ Error: Please provide a valid email address.")
        sys.exit(1)
    return email


def validate_python_version(version):
    """Validate Python version."""
    try:
        major, minor = map(int, version.split('.'))
        if major < 3 or (major == 3 and minor < 8):
            print("❌ Error: Python version must be 3.8 or higher.")
            sys.exit(1)
    except ValueError:
        print("❌ Error: Invalid Python version format. Use format like '3.12'.")
        sys.exit(1)
    return version


def validate_django_version(version):
    """Validate Django version."""
    try:
        major, minor = map(int, version.split('.'))
        if major < 4 or (major == 4 and minor < 0):
            print("❌ Error: Django version must be 4.0 or higher.")
            sys.exit(1)
    except ValueError:
        print("❌ Error: Invalid Django version format. Use format like '5.2'.")
        sys.exit(1)
    return version


def main():
    """Main validation function."""
    print("🔍 Validating project configuration...")
    
    # Get the project context
    project_slug = "{{ cookiecutter.project_slug }}"
    author_email = "{{ cookiecutter.author_email }}"
    python_version = "{{ cookiecutter.python_version }}"
    django_version = "{{ cookiecutter.django_version }}"
    
    # Validate inputs
    validate_project_slug(project_slug)
    validate_email(author_email)
    validate_python_version(python_version)
    validate_django_version(django_version)
    
    # Additional validations
    if "{{ cookiecutter.use_redis }}" == "y" and "{{ cookiecutter.cache_backend }}" != "redis":
        print("⚠️  Warning: You selected Redis but not as cache backend. This might cause issues.")
    
    if "{{ cookiecutter.use_postgresql }}" == "y" and "{{ cookiecutter.database_engine }}" != "postgresql":
        print("⚠️  Warning: You selected PostgreSQL but not as database engine. This might cause issues.")
    
    print("✅ Project configuration is valid!")
    print(f"📦 Project: {project_slug}")
    print(f"🐍 Python: {python_version}")
    print(f"🌐 Django: {django_version}")
    print(f"📧 Author: {{ cookiecutter.author_name }} <{author_email}>")


if __name__ == "__main__":
    main()
