# Django REST API project

- This API authenticates users and allows users to save marker locations to a Postgre database.
- The infrastructure is handled with docker-compose.

## Running

- **Note:** you need to set up the **.env** file to run this project (check .env_example).

- Run the following commands:

- Build and start all containers:
    `docker-compose up --build`
- Migration:
  - Once the containers are up and running, you need to apply the database migrations.
    `docker-compose run web python manage.py migrate`
- Tests:
    `docker-compose run web python manage.py test`
- Stop containers:
    `docker-compose down`

## Other Commands

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

- Test authentication with test user:
    `curl -X POST -d "username=testuser&password=testpassword" http://localhost:8000/api-token-auth/`
- Use the token to access a protected endpoint:
    `curl -H "Authorization: Token <your-token>" http://localhost:8000/api/hello/`
