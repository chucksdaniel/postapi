## POST API 

Source Code of FastAPI Examples
FastAPI examples often act as living documentation.
🔗 https://github.com/tiangolo/fastapi/tree/master/docs_src/security

### Environment set up

-  **Create a new venv in the project folder** Run the following command to create an environment
```bash
python3 -m venv venv
```

Activate the environment for the project
```bash
source venv/bin/activate
```

- **Install the dependencies for the project** The requirement files is a file generated that containers all the requires packages/dependencies for the project.

```bash
pip install -r requirements.txt
```

Common issues - could not be resolved
Package could not be resolved - This kind of error is associated with the python interpreter the system is using for the execution.
Ensure that the python interpreter selected is the one in the same project directory where the environment was created

- **Force your editor to use the venv interpreter**
Open Command Palette

Ctrl + Shift + P

Select:

Python: Select Interpreter


Choose:
```bash
./venv/bin/python
```

Reload VS Code:
```bash
Ctrl + Shift + P → Reload Window
```

Verify in VS Code terminal:
```bash
python -c "import sqlalchemy; print(sqlalchemy.__version__)"
```

[FastAPI](https://fastapi.tiangolo.com/learn/) documentation [JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/?h=passli#hash-and-verify-the-passwords)

[SQLALCHEMY](https://www.sqlalchemy.org/) documentation

We are using the sqlalchemy ORM for this Project, and note that Sqlalchemy doesn't know how to talk to database it requires an underline driver to be able to, for this project, we are using Postgres Database and the drivers under the hood is `psycopg`. 

To install 

`pip install SQLAlchemy==1.4.23` is the required SQLAlchemy for this course

#### Some of the challenges of sqlalchemy
- When a new column with default value is added to a table It doesn't take effect untill you drop the table and recreate it

### The Server 
This contains really database manipulation with more clear up data

#### Links to the documentation [clickme](https://www.psycopg.org/docs/)
For [Psycopg3](https://www.psycopg.org/psycopg3/docs/basic/usage.html) installation

### Authentication 
What is Authentication?






#### JWT Base Authentication
In this project, we are going to implement `jwt` based authentication

The package we will be using for this is `python-jose` Python-jose is commonly used with FastAPI for JWT handling, even though it’s not explicitly listed everywhere in the official FastAPI docs

- FastAPI Is Library-agnostic
  - FastAPI deliberately avoids tying authentication to a specific JWT library.
  - JWT is not part of FastAPI
  - JWT handling is an implementation detail
  - Multiple valid libraries exist (python-jose, PyJWT, Authlib)

- Avoiding Vendor Lock-in If FastAPI officially endorsed one JWT library:
  - It would limit flexibility
  - It would increase maintenance burden
  - It would break apps if that library changed
  - Instead, FastAPI documents:
    - OAuth2 flows
    - Dependency injection
    - Security schemes
    …and leaves token creation/verification to you.

- Where to Find Proper Documentation ✅
  1. Official python-jose Documentation
   This is the primary source.
    🔗 GitHub README - https://github.com/mpdavis/python-jose
    Key sections to read:
    - JWT encoding/decoding
    - Supported algorithms (HS256, RS256)
    - Error handling (JWTError, ExpiredSignatureError)


If you want to generate a password

```bash
openssl rand -hex 32
```


(class) OAuth2PasswordRequestForm
This is a dependency class to collect the username and password as form data for an OAuth2 password flow.
The OAuth2 specification dictates that for a password flow the data should be collected using form data (instead of JSON) and that it should have the specific fields username and password.
All the initialization parameters are extracted from the request. [Read more](https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/#scope) 

If you using this method, You no longer send credential through the body, but through the form data. My question is with schema we have the flexibility of ensuring the email is a validate email using `Emailstr` here how is this achieved.


### Database Migration Tool

The ORM has a limitation, one of the limitation is that once a table has been created doesn't allow for the table upgrade or deleting. so you will have to manually update or drop the table

The solution is [documentation](https://alembic.sqlalchemy.org/en/latest/)

