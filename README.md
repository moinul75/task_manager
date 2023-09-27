# Task Manager with REST API

## Description

Create a task management web application with a REST API using Django. The application allows multiple users to create, view, update, and delete tasks. This project follows best development practices, including using virtual environments, environment variables, and Git for version control.

## Project Setup

1. **Django Project Setup**
    - Create a new Django project named "task_manager" (or your preferred name).
    - Set up a virtual environment for the project.
    - Install the required dependencies, including Django, djangorestframework, psycopg2, etc.
    - Configure the PostgreSQL database.

2. **Django App Setup**
    - Create a new Django app named "tasks."

3. **Features/Functionalities**
    - User Authentication (Registration, Login).
    - Password reset option (Optional).
    - Home page displaying the tasks list after successful login.
    - Task properties:
        - Title, description, due date.
        - Multiple photos add/delete options.
        - Priority (Low, medium, high).
        - Option to mark as complete.
        - Creation date and time.
        - Last Update date and time (Optional).
    - Task list page with search and filter options.
    - Task details page.
    - Task update page with all fields.
    - Task deletion with confirmation.
    - Additional fields/models as needed.

4. **Database Relations**
    - Define appropriate relations between models using ForeignKey, ManyToManyField, etc.
    - Represent any other entities required for the project (e.g., User).

5. **Admin Panel**
    - Add all models in Admin.
    - Implement CRUD functionalities for all models in Admin.
    - Show only necessary fields in the list for each model.
    - Sort tasks by Priority by default.

6. **Django Templates**
    - Create a base template shared among all other templates.
    - Create templates for task list, task creation, task details, task update, and task deletion.
    - Use Django template tags and filters as needed.
    - Ensure responsive and visually appealing templates.

7. **Django Views and URLs**
    - Create Class-Based Views for task-related functionalities.
    - Define URL patterns for each view.
    - Map URLs to respective views.

8. **Functionality Implementation**
    - Retrieve tasks from the database and display them.
    - Implement forms for task creation and update.
    - Handle form validation and errors.
    - Implement logic for creating, updating, and deleting tasks using Django ORM.

9. **REST API**
    - Create API views for listing tasks, retrieving a single task, creating, updating, and deleting tasks.
    - Use appropriate serializers for data conversion.
    - Handle HTTP methods (GET, POST, PUT/PATCH, DELETE).
    - Validate input data and handle errors.
    - Api Documents are given below:
  

## Usage

### Environment Variables

Create a `.env` file with the following environment variables:

- `SECRET_KEY` - Django secret key.
- `DEBUG` - Set to `True` for development, `False` for production.
- `DB_NAME` - PostgreSQL database name.
- `DB_USER` - PostgreSQL database user.
- `DB_PASSWORD` - PostgreSQL database password.
- `DB_HOST` - PostgreSQL database host.
- `DB_PORT` - PostgreSQL database port.
- Add any other sensitive information here.

### Running the Project
1. Clone this git repository 
   ```bash
   git clone https://github.com/moinul75/task_manager

2. Activate your virtual environment.


3. Install project dependencies:

   ```bash
   pip install -r requirements.txt 

4. Go to Project Folder 
   ```bash
   cd task_manager

5. Run django start server command 
   ```bash 
   python manage.py runserver 


