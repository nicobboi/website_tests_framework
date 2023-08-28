# BACKEND framework

## General workflow

All backend files are in `backend/`.

By default, the dependencies are managed with [Poetry](https://python-poetry.org/), go there and install it.

From `./app/` you can install all the dependencies with:

```console
$ poetry install
```

Then you can start a shell session with the new environment with:

```console
$ poetry shell
```

Next, open your editor at `./app/` (instead of the project root: `./`), so that you see an `./app/` directory with your code inside. That way, your editor will be able to find all the imports, etc. Make sure your editor uses the environment you just created with Poetry.

Modify or add SQLAlchemy models in `./app/app/models/`, Pydantic schemas in `./app/app/schemas/`, API endpoints in `./app/app/api/`, CRUD (Create, Read, Update, Delete) utils in `./app/app/crud/`.

If you want to use mockup tools instead of the real ones, uncomment the *MOCKUP_TESTS* variable in `.env`.


## Celery

Celery app configurations are in `./app/app/core/celery_app.py`.

All Celery files are in `./app/app/worker`: 
 * Add and modify tasks to the Celery worker in `tasks.py`;
 * Celery scheduler is handled by `scheduler.py`; 
 * Redis database handler (used to retrieve task informations) is `redis_db.py`.

If you need to install any additional package to the worker, add it to the file `backend/app/celeryworker.dockerfile`.


## Migrations

As during local development your app directory is mounted as a volume inside the container, you can also run the migrations with `alembic` commands inside the container and the migration code will be in your app directory (instead of being only inside the container). So you can add it to your git repository.

Make sure you create a "revision" of your models and that you "upgrade" your database with that revision every time you change them. As this is what will update the tables in your database. Otherwise, your application will have errors.

* Start an interactive session in the backend container:

```console
$ docker compose exec backend bash
```

* If you created a new model in `./app/app/models/`, make sure to import it in `./app/app/db/base.py`, that Python module (`base.py`) that imports all the models will be used by Alembic.

* After changing a model (for example, adding a column), inside the container, create a revision, e.g.:

```console
$ alembic revision --autogenerate -m "Add column last_name to User model"
```

* Commit to the git repository the files generated in the alembic directory.

* After creating the revision, run the migration in the database (this is what will actually change the database):

```console
$ alembic upgrade head
```

If you don't want to use migrations at all, uncomment the line in the file at `./app/app/db/init_db.py` with:

```python
Base.metadata.create_all(bind=engine)
```

and comment the line in the file `prestart.sh` that contains:

```console
$ alembic upgrade head
```


## [Tools implementation guide](TOOLS.md)
