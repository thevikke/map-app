# Django REST API project

- This API authenticates users and allows users to save marker locations to a Postgre database.
- The infrastructure is handled with docker-compose.
- **NOTE**: This is a `.md` document, use md-editor.

## Running

- **Note:** you need to set up the **.env** file to run this project (check .env_example).

- Run the following commands:

- Build and start all containers:
    `docker-compose up --build`

- Default users:

    ```python
      {'username': 'admin', 'email': 'admin@example.com', 'password': 'adminpassword'},
      {'username': 'user1', 'email': 'user1@example.com', 'password': 'user1password'},
      {'username': 'user2', 'email': 'user2@example.com', 'password': 'user2password'},
    ```

- Login to `http://localhost:3000`

## Other Commands

- Migration:
  - Once the containers are up and running, you need to apply the database migrations.
    `docker-compose run web python manage.py migrate`
  - Create migrations.
    `docker-compose exec web python manage.py makemigrations`
- Tests:
    `docker-compose run web python manage.py test`
- Stop containers:
    `docker-compose down`
- Remove containers and volumes:
    `docker-compose down -v`
- View logs:
    `docker-compose logs -f`
- Access Django shell:
    `docker-compose exec web python manage.py shell`
  - Adding test user in the shell:

    ```python
    from django.contrib.auth.models import User

    # Create a new user
    user = User.objects.create_user(username='testuser', password='testpassword')
    user.email = 'testuser@example.com'
    user.save()
    exit()
    ```

## Access Admin Page

- Need to create a superuser first.
  - Navigate to `http://localhost:8000/admin/`
