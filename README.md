# Ansible Tower Admin GUI

This project provides a web-based administrative graphical user interface (GUI) for managing Ansible Tower instances. It allows users to view and manage Tower instances, credentials, execution environments, audit logs, and user accounts.

## Technologies Used

### Backend
*   **Django**: Web framework for rapid development.
*   **Django Rest Framework (DRF)**: For building robust RESTful APIs.
*   **PostgreSQL**: (Assumed, based on Django's ORM capabilities and typical deployments) Database for storing application data.
*   **Fernet Fields**: For encrypting sensitive data like passwords in the database.

### Frontend
*   **AngularJS**: JavaScript framework for building the single-page application (SPA).
*   **ngRoute**: For client-side routing.
*   **ngResource**: For interacting with RESTful APIs.
*   **Chart.js**: (Assumed, based on "Job Chart" and "Statistics" in app.js) For rendering charts and graphs.
*   **HTML5 & CSS3**: For structuring and styling the user interface.

## Project Structure

*   `backend/`: Contains the Django backend application.
    *   `tower/`: The core Django app with models, views, serializers, and URLs.
    *   `tower_admin/`: Django project settings.
*   `frontend/`: Contains the AngularJS frontend application.
    *   `app/`: Main AngularJS application files, including `app.js`, controllers, services, and filters.
    *   `index.html`: The main HTML file for the single-page application.
    *   `style.css`: Global styles for the application.

## Core Functionalities

*   **Dashboard**: Provides an overview of Tower instances, credentials, environments, and recent audit logs. Includes job statistics charts.
*   **Tower Instance Management**: CRUD operations for Ansible Tower instances, including details like URL, username, region, and environment. Passwords are encrypted.
*   **Credential Management**: CRUD operations for credentials associated with Tower instances.
*   **Execution Environment Management**: CRUD operations for execution environments.
*   **User Management**: Admin-only functionality to manage application users, including their roles (admin, member, viewer).
*   **Audit Logging**: Tracks and logs all create, update, and delete actions performed on Tower instances, credentials, and execution environments.
*   **Configuration**: Allows administrators to configure global settings, such as the primary Ansible Tower connection details.
*   **Ansible Tower Proxy**: Proxies requests to the actual Ansible Tower API for fetching specific data (e.g., credentials).

## Key Backend Concepts

The backend is built with Django and Django Rest Framework (DRF), providing a robust API for the frontend.

### Django Models (`backend/tower/models.py`)
These define the database schema and relationships between different data entities.
*   `TowerConfig`: Stores the primary Ansible Tower connection details.
*   `Auditlog`: Records all significant changes (create, update, delete) to other models, including who made the change, what was changed, and when.
*   `TowerInstance`: Represents a managed Ansible Tower instance with its connection details and status. Notably, passwords are encrypted using `fernet_fields`.
*   `Credential`: Stores credentials (e.g., API keys, SSH keys) that can be used with specific `TowerInstance`s. It has a `ForeignKey` relationship to `TowerInstance`.
*   `ExecutionEnvironment`: Defines various execution environments available within Ansible Tower, also linked to a `TowerInstance`.
*   `CustomUser`: Extends Django's default `User` model to include a `role` field for access control (admin, member, viewer).

### Django Rest Framework (DRF) Serializers (`backend/tower/serializers.py`)
Serializers convert complex data types (like Django model instances) into native Python datatypes that can be easily rendered into JSON, XML, or other content types. They also provide deserialization, allowing parsed data to be converted back into complex types.
*   Each model generally has a corresponding serializer (e.g., `TowerInstanceSerializer` for `TowerInstance`).
*   Sensitive fields like `password` are often marked as `write_only` for security, meaning they are accepted on input but not returned in API responses.

### Django Rest Framework (DRF) Views (`backend/tower/views.py`)
Views handle incoming HTTP requests and return HTTP responses. DRF's `ViewSet`s provide a convenient way to implement API endpoints for common operations (CRUD).
*   `ModelViewSet`: Provides a full set of CRUD operations (List, Create, Retrieve, Update, Destroy) for a model. Examples include `UserViewSet`, `TowerInstanceViewSet`, etc.
*   **Custom Logic**: `perform_create`, `perform_update`, and `perform_destroy` methods are overridden in some ViewSets to implement custom logic, such as audit logging. The `log_action` utility (from `utils.py`) is used for this purpose.
*   `TowerCredentialProxy`: A custom ViewSet that acts as a proxy to fetch credentials directly from a configured Ansible Tower instance, using the stored `TowerConfig` credentials.
*   `user_info`: A simple API endpoint (`@api_view`) to return details about the currently authenticated user.

### URL Routing (`backend/tower/urls.py` and `backend/tower_admin/urls.py`)
*   `DefaultRouter`: Automatically generates URL patterns for `ViewSet`s, simplifying API endpoint creation.
*   The `backend/tower/urls.py` defines the API endpoints for the `tower` application, which are then included in the main project's `backend/tower_admin/urls.py`.

## Key Frontend Concepts

The frontend is an AngularJS single-page application (SPA) that consumes the Django backend API.

### Main Application Module (`frontend/app/app.js`)
*   Defines the main AngularJS module `towerAdminApp` and its dependencies (`ngRoute`, `ngResource`).
*   **Routing (`$routeProvider`)**: Configures client-side routes, mapping URL paths to specific HTML templates and controllers. This allows for navigation within the SPA without full page reloads.
*   **Global Run Block**: The `.run()` block executes after all modules have been loaded. It's used here to fetch the current user's information via `AuthService` and make it globally available on `$rootScope`.

### Controllers (`frontend/app/controllers/`)
Controllers (`DashboardController`, `InstanceController`, `UserMgmtController`, etc.) are JavaScript functions that are responsible for the application logic and data binding for a specific view.
*   They interact with services (e.g., `apiService`, `UserService`) to fetch and manipulate data.
*   They expose data and functions to the HTML templates via the `$scope` object.

### Services/Factories (`frontend/app/services/`)
Services (or factories in AngularJS) are singletons that can be injected into controllers or other services. They are used to encapsulate reusable business logic, especially for interacting with backend APIs.
*   `apiService.js`: Intended for general API calls (currently has a placeholder).
*   `authUserService.js`:
    *   `AuthService`: Manages user authentication state and provides methods to retrieve user information from the backend.
    *   `UserService`: Provides methods (`list`, `create`, `update`, `delete`) for interacting with the `/api/users/` endpoint to manage user accounts.

### Filters (`frontend/app/filters/`)
Filters (`uniqueFilter.js`) are used to format data for display in HTML templates. They can be applied in expressions using the `|` symbol (e.g., `{{ data | uniqueFilter }}`).

### Views (Inline HTML in `app.js` and `index.html`)
*   `index.html`: The main entry point of the frontend application. It loads AngularJS, its dependencies, and the application's JavaScript files.
*   Inline HTML templates within `app.js` define the structure and content for each route's view. These templates use AngularJS directives (e.g., `ng-repeat`, `ng-model`, `ng-click`, `ng-if`) for data binding and dynamic content.

### Styling (`frontend/style.css`)
Provides the global CSS for the application's visual presentation.

## Setup Instructions

### Prerequisites
*   Python 3.x
*   Node.js & npm (or yarn)
*   A database (e.g., PostgreSQL) compatible with Django.

### Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```
2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt # (Assuming a requirements.txt file exists or will be created)
    ```
3.  **Configure database settings:**
    Edit `tower_admin/settings.py` to configure your database connection.

4.  **Run database migrations:**
    ```bash
    python manage.py makemigrations tower
    python manage.py migrate
    ```
5.  **Create a superuser (admin account):**
    ```bash
    python manage.py createsuperuser
    ```
6.  **Run the Django development server:**
    ```bash
    python manage.py runserver
    ```
    The backend API will be available at `http://127.0.0.1:8000/`.

### Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```
2.  **Install Node.js dependencies:**
    ```bash
    npm install
    ```
3.  **Start the frontend development server:**
    (This project uses AngularJS and seems to be served directly from `index.html` via a web server or Django's static files. For development, you might need a simple static file server or rely on Django's `runserver`.)

    If running separately, ensure your frontend is served from a web server (e.g., Apache, Nginx, or a simple `http-server` npm package) and can access the backend API at `http://127.0.0.1:8000/`.

## API Endpoints (Backend)

*   `/api/user-info/`: GET - Current authenticated user details.
*   `/api/users/`: CRUD operations for user management.
*   `/api/tower-credentials/`: GET - Proxied Ansible Tower credentials.
*   `/api/tower/`: CRUD operations for Tower instances.
*   `/api/instances/`: CRUD operations for Tower instances (alias of `/api/tower/`).
*   `/api/credentials/`: CRUD operations for credentials.
*   `/api/environments/`: CRUD operations for execution environments.
*   `/api/audit-logs/`: GET - Audit log entries.

## Frontend Routes (AngularJS)

*   `/dashboard`: Main dashboard view.
*   `/instances`: Manage Ansible Tower instances.
*   `/credentials`: Manage credentials.
*   `/environments`: Manage execution environments.
*   `/statistics`: View application statistics.
*   `/audit-logs`: View audit trail.
*   `/users`: Manage application users.
*   `/config`: Configure global application settings.

## Development Workflow for a Colleague

Here's a guide to help you get started and contribute to this project.

### 1. Getting Started
Follow the "Setup Instructions" section above to get both the backend and frontend running on your local machine. Ensure both are running simultaneously for the application to function correctly.

### 2. Running the Application
*   **Backend**: `cd backend && python manage.py runserver`
*   **Frontend**: As the frontend is served directly, you'll open `frontend/index.html` in your browser, or serve it using a simple static file server (e.g., `npx http-server` from the `frontend` directory after `npm install http-server -g`). Ensure your browser can reach `http://127.0.0.1:8000` for API calls.

### 3. Debugging Tips
*   **Backend (Django)**:
    *   **Django Debug Toolbar**: While not explicitly installed, consider adding it for detailed request/response information, database queries, and more.
    *   **`print()` statements**: Simple `print()` statements in your Django views or models will output to the terminal where `runserver` is running.
    *   **Django Shell**: `python manage.py shell` provides an interactive Python shell with your Django environment loaded, useful for testing models and functions.
*   **Frontend (AngularJS)**:
    *   **Browser Developer Tools**: Use your browser's developer console (F12 or right-click -> Inspect) to:
        *   Inspect network requests to see API calls and responses.
        *   View console logs for JavaScript errors or `console.log()` outputs.
        *   Debug JavaScript code with breakpoints.
    *   **AngularJS Batarang (Chrome Extension)**: A browser extension that provides enhanced debugging capabilities for AngularJS applications.

### 4. Common Development Tasks

#### Adding a New Feature
1.  **Backend**:
    *   Define/update models in `backend/tower/models.py`. Run migrations.
    *   Create/update serializers in `backend/tower/serializers.py`.
    *   Implement API logic in `backend/tower/views.py` (e.g., a new `ViewSet` or custom API view).
    *   Register new API endpoints in `backend/tower/urls.py`.
2.  **Frontend**:
    *   Add a new route to `frontend/app/app.js` (or modify an existing one).
    *   Create a new controller in `frontend/app/controllers/` (e.g., `newFeatureController.js`) or modify an existing one.
    *   Develop the HTML template for the new view (either inline in `app.js` or in a separate file if it gets complex).
    *   Create new services/factories in `frontend/app/services/` if specific API interactions are needed.
    *   Update `frontend/index.html` or `frontend/style.css` if global changes are required.

#### Modifying Existing Functionality
*   Trace the functionality from the frontend route (`app.js`) to its controller, then to the services, and finally to the backend API endpoint (view, serializer, model).
*   Make changes in the relevant files following the same logic as adding a new feature.

### 5. Troubleshooting Common Issues

*   **"Error contacting Tower" / 502 Bad Gateway (Backend)**:
    *   Check `TowerConfig` settings in the database. Ensure the `base_url`, `username`, and `password` are correct and the Ansible Tower instance is accessible from where the Django backend is running.
    *   Verify network connectivity between the Django backend and Ansible Tower.
*   **404 Not Found (API Endpoints)**:
    *   Double-check URL patterns in `backend/tower/urls.py` and `backend/tower_admin/urls.py`.
    *   Ensure the `runserver` is running.
*   **Frontend Not Loading / Blank Page**:
    *   Open browser developer tools (F12) and check the Console for JavaScript errors.
    *   Verify that `index.html` is correctly loading `app.js` and all other AngularJS files.
    *   Check network requests to ensure all frontend assets are loading correctly.
*   **Authentication Issues**:
    *   Ensure you've created a superuser with `python manage.py createsuperuser`.
    *   Verify the `AuthService` is correctly hitting the `/api/user-info/` endpoint.
    *   Check user roles and permissions if you're experiencing access denied issues.

## Further Exploration

*   **Django Documentation**: [https://docs.djangoproject.com/en/stable/](https://docs.djangoproject.com/en/stable/)
*   **Django Rest Framework Documentation**: [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)
*   **AngularJS Documentation**: [https://docs.angularjs.org/api](https://docs.angularjs.org/api)
*   **Fernet Fields**: Understand how sensitive data encryption works.
*   **Chart.js**: If you need to modify charts, refer to the Chart.js documentation.

## Contributing

(Add contributing guidelines here)

## License

(Add license information here)
