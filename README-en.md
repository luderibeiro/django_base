# 🚀 Django Base - Clean Architecture Template

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.0+-green.svg)](https://djangoproject.com)
[![Version](https://img.shields.io/badge/Version-2.1.0-orange.svg)](https://github.com/luderibeiro/django_base/releases)
[![Tests](https://img.shields.io/badge/Tests-93%25%20coverage-brightgreen.svg)](https://github.com/luderibeiro/django_base/actions)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-MkDocs-blue.svg)](https://luderibeiro.github.io/django_base/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](Dockerfile)

**🌟 Professional template for Django projects with Clean Architecture**

[📖 Documentation](https://luderibeiro.github.io/django_base/) • [🚀 Quick Start](#-quick-start) • [🏗️ Architecture](#️-architecture) • [🤝 Contributing](#-contributing)

</div>

---

## 🎯 About the Project

This Django template provides a **solid and professional foundation** for developing web applications and APIs, following **Clean Architecture** principles. Perfect for:

-   🔥 **Startups** that need fast and scalable development
-   🏢 **Companies** seeking code standardization and quality
-   👨‍💻 **Developers** who want to learn good architecture practices
-   🎓 **Students** interested in well-structured projects

### ✨ Key Features

-   🏗️ **Clean Architecture** - Clear separation of responsibilities
-   📊 **93% Test Coverage** - Complete suite of unit and integration tests
-   📖 **OpenAPI/Swagger** - Automatic API documentation
-   🔧 **Pre-commit Hooks** - Automated code quality
-   🐍 **MyPy** - Static type checking
-   🐳 **Docker Ready** - Complete containerization for development and production
-   🚀 **GitHub Actions CI/CD** - Complete continuous integration pipeline
-   📚 **Rich Documentation** - MkDocs with MkDocstrings for automatic documentation
-   🔧 **Powerful Makefile** - 20+ development automation commands
-   🎨 **Admin Interface** - Django Jazzmin for elegant administration
-   🔐 **OAuth2 Authentication** - Robust authentication system
-   📊 **REST API** - Configured Django REST Framework

## 🚀 Quick Start

### Prerequisites

-   Python 3.12+
-   Docker & Docker Compose (optional)
-   Git

### ⚡ Setup in 3 commands

```bash
# 1. Clone the template
git clone https://github.com/luderibeiro/django_base.git my_project
cd my_project

# 2. Configure the environment
make setup

# 3. Start the server
make run
```

🎉 **Done!** Access <http://127.0.0.1:8000>

### 🐳 With Docker

```bash
# Development
make docker-run

# Production
make docker-prod
```

## 🏗️ Architecture

```bash
project/
├── core/                    # Main application
│   ├── domain/             # Business rules
│   ├── repositories/       # Data access
│   ├── api/               # REST endpoints
│   └── admin/             # Administrative interface
├── project/               # Django settings
└── tests/                 # Automated tests
```

### 🎯 Architecture Layers

-   **🎯 Domain**: Entities and business rules
-   **🔄 Repository**: Data access abstraction
-   **🌐 API**: Endpoints and serializers
-   **⚙️ Infrastructure**: Settings and integrations

## 📋 Available Commands

```bash
make help              # List all commands
make setup             # Complete initial setup
make test              # Run all tests
make test-coverage     # Tests with coverage
make lint              # Code analysis
make format            # Automatic formatting
make docs-serve        # Serve local documentation
make clean             # Clean temporary files
```

## 🛠️ Technologies

-   **Backend**: Django 5.2+, Django REST Framework
-   **Database**: PostgreSQL (production), SQLite (development)
-   **Authentication**: Django OAuth Toolkit
-   **Testing**: pytest, pytest-django
-   **Documentation**: MkDocs
-   **Containerization**: Docker, Docker Compose
-   **Code Quality**: Black, Flake8, pip-audit

## 📖 Complete Documentation

For detailed guides, examples and API references, access our [**complete documentation**](https://luderibeiro.github.io/django_base/).

### 📚 Available Guides

-   [🚀 Project Setup](https://luderibeiro.github.io/django_base/setup/project-setup/)
-   [🏗️ Detailed Architecture](https://luderibeiro.github.io/django_base/architecture/)
-   [🧪 Automated Testing](https://luderibeiro.github.io/django_base/development/automated-testing/)
-   [🚀 Production Deploy](https://luderibeiro.github.io/django_base/setup/production-setup/)

## 🤝 Contributing

Contributions are very welcome! This project was created to be a **community template**.

### 💡 How to Contribute

1. 🍴 Fork the project
2. 🌟 Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. ✅ Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push to the branch (`git push origin feature/AmazingFeature`)
5. 🔄 Open a Pull Request

### 🎯 Ideas for Contribution

-   📱 Specific templates (e-commerce, blog, API, etc.)
-   🔧 Automation improvements
-   📚 Documentation translation
-   🧪 New test cases
-   🎨 UI/UX improvements

## 📄 License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.

## 🌟 Support the Project

If this template was useful to you:

-   ⭐ Give a star to the repository
-   🍴 Fork for your customizations
-   📢 Share with other developers
-   🐛 Report bugs or suggest improvements

---

<div align="center">

**Developed with ❤️ for the Django community**

[📖 Documentation](https://luderibeiro.github.io/django_base/) • [🐛 Issues](https://github.com/luderibeiro/django_base/issues) • [💬 Discussions](https://github.com/luderibeiro/django_base/discussions)

</div>
