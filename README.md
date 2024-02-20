# notes_taking_app
---
1. set up a Database and create a .env file from .env.example
2. create a virtual environment.
3. Create migrations `./manage.py makemigrations notes_app`.
4. Run migrations `python manage.py migrate notes_app`
5. Now you can run the file `python manage.py runserver`
6. open postman and hit the api's.

## API Documentation.
---
1. **signup**: `/api/signup` POST method in request body name,email,password are mandatory
2. **login**:`/api/login` POST method in request body email,password are mandatory
3. **create note**: `/api/notes/create` POST method title,content mandatory
4. **read note**: `/api/notes/{id}` GET method here id is notes id
5. **share notes**: `/api/notes/share` POST method in request body note_id,user_emails(array) are mandatory
6. **edit note**:`/api/notes/{id}` POST method title or content are mandatory.
7. **version history**:`/api/notes/version-history/{id}` GET method id is note's id.

contact: rahulvemula03@gmail.com, 7093328593