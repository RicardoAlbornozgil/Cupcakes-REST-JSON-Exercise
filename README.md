# Cupcakes Flask App

This Flask application is designed to manage a collection of cupcakes. It provides endpoints for listing, creating, updating, and deleting cupcakes, along with a homepage to view and interact with the cupcakes.

## Features

- **List Cupcakes:** View all cupcakes stored in the database.
- **Add Cupcake:** Create a new cupcake and store it in the database.
- **View Cupcake Details:** Retrieve details of a specific cupcake by its ID.
- **Update Cupcake:** Modify the details of an existing cupcake.
- **Delete Cupcake:** Remove a cupcake from the database.

## Technologies Used

- **Flask:** A micro web framework for Python used to develop the backend logic.
- **SQLAlchemy:** An SQL toolkit and Object-Relational Mapping (ORM) library for Python used for database operations.
- **WTForms:** A flexible form rendering and validation library for Python used for form management.
- **HTML/CSS:** Frontend markup and styling for the homepage and form elements.
- **PostgreSQL:** A powerful, open-source relational database system used for storing cupcake data.
- **Flask-CORS:** A Flask extension for handling Cross-Origin Resource Sharing (CORS), allowing frontend applications to access the API endpoints.
- **Axios:** A promise-based HTTP client for the browser and Node.js, used for making AJAX requests from the frontend to the backend.

## Setup

1. Clone this repository to your local machine.
2. Install the required dependencies listed in the `requirements.txt` file using the following command:
``` bash
pip install -r requirements.txt
```
3. Set up a PostgreSQL database and update the `SQLALCHEMY_DATABASE_URI` configuration in `app.py` with your database connection string.
4. Run the Flask application using `python app.py`.
5. (Optional) Populate the database with sample data using the `seed.py` script provided in the repository.
6. (Optional) Run the test suite to ensure the correctness of the application using the `tests.py` script.

## Models

The application utilizes SQLAlchemy ORM to define the following model:

### Cupcake

- **Table Name:** cupcakes
- **Columns:**
- `id`: Integer, Primary Key, Autoincrement
- `flavor`: Text, Not Null
- `size`: Text, Not Null
- `rating`: Float, Not Null
- `image`: Text, Not Null, Default: DEFAULT_IMAGE

## Frontend

The frontend of the application is powered by HTML, CSS, and JavaScript. The `index.html` template provides the layout for the homepage, allowing users to view all cupcakes and add new ones. The styling is defined in the `style.css` file, and the interactivity is handled by the `cupcakes.js` script.

## Usage

- Access the homepage by navigating to the root URL of the application.
- Use the provided API endpoints (`/api/cupcakes`) to interact with cupcakes programmatically.
- Follow the provided API documentation in the source code comments for details on each endpoint's functionality.

## Further Study

- Implement tests to ensure robustness and correctness of the application.
- Enhance the frontend with object-oriented JavaScript and utilize class methods for better code organization.
- Refactor HTML templates to use WTForms for improved form handling and validation.
- Expand search functionality to allow filtering cupcakes by various criteria.
- Add support for updating cupcakes directly from the frontend.
- Extend the application by introducing a new table for managing cupcake ingredients.

## Contributors

- [Ricardo Albornoz](https://github.com/RicardoAlbornozgi)
