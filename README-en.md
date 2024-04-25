# Django Project Template

Quer ler este README em português? [Clique aqui](README.md)

This repository serves as a template for starting projects in Python (version 3.12) with the Django framework (version 5.0).

## About the Project

This Django project is Dockerized and follows the principles of Clean Architecture. It provides a solid structure for developing a variety of applications, from APIs to web applications.

## How to Use

Follow these steps to run the project:

1.  **Clone the Repository:**

        git clone git@github.com:luderibeiro/django_base.git

2.  **Set Up the Environment:**

-   Create a `.env` file in the project root and add necessary configurations such as API keys, database settings, etc.

3.  **Run Docker Compose:**

        docker-compose up --build

`Note: The `--build` flag should be executed only the first time the project is installed or when there are changes in the build files.`

4. **Access the Application:**
   The application will be available at `http://localhost:8000`.

## Contribution

Feel free to contribute improvements or new features. Just follow these steps:

1. Fork the repository.
2. Create a branch for your contribution: `git checkout -b feature/new-feature`.
3. Make your changes and commit: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature/new-feature`.
5. Open a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
