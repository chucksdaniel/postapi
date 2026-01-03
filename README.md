## POST API 

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

[FastAPI](https://fastapi.tiangolo.com/learn/) documentation

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
