## POST API 

### Environment set up


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

