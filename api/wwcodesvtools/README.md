# WWCode-SV Chapter Tools API

## Setup instructions using Docker:
1. Install [Docker Community Edition](https://docs.docker.com/install/) if it
is not already installed.
1. Once Docker is installed, run the following commands:
    ```
    $ cd api/wwcodesvtools/
    $ docker-compose up
    ```
1. The web application will be available at http://localhost:8000

### Compose
Generally it is more convenient to run the containers in the background using daemon mode. To start the containers in daemon mode, use the following command:
```
$ docker-compose up -d
```
To check if the containers are running, use:
```
$ docker-compose ps
```
To rebuild all the containers, use the following command:
```
$ docker-compose up -d --build
```
To restart the web service, run:
```
$ docker-compose restart web
```
To run any command in the app container, use:
```
$ docker-compose exec web <command>
```

To be able to interactively run or debug inside the container environment, run:
```
$ docker-compose exec <service> bash
```

For example:
```
$ docker-compose exec web bash
```

### Logs
To tail logs, run:
```
$ docker-compose logs -f web
```

### Migrations
When you bring up docker containers for the first time or rebuild them,
migrations are automatically run. If your containers are already running and
you want to add a few migrations and run migrations in the db, you can use the
following commands.

To make a new migration, run:
```
$ docker-compose exec web python manage.py makemigrations --name <name of migration>
```
To run migrations, run:
```
$ docker-compose exec web python manage.py migrate --noinput
```

### Shut down
To stop the containers but not remove them, run:
```
$ docker-compose stop
```

To stop and remove containers, run:
```
$ docker-compose down
```

To stop and remove all containers, as well as volumes as networks, run:
```
$ docker-compose down -v
```
This command is helpful if you want to start with a clean slate. However, it
will completely remove any data you have already stored in the database.

## Deploying onto Heroku
* Check that the containers are working on the localhost.
* Login to heroku
```
heroku login
```

* Login for heroku container registry
```
heroku container:login
```

* Build and push container to heroku registry
```
heroku container:push web -a wwcode-chtools-api -r <git remote of app>

heroku container:push web -a wwcode-chtools-api -r wwcode-chtools-api
```

* Release container on heroku
```
heroku container:release web -a wwcode-chtools-api -r <git remote of app>

heroku container:release web -a wwcode-chtools-api -r wwcode-chtools-api
```

* Check releases
```
heroku releases -a wwcode-chtools-api
```

* Check logs
```
heroku logs --tail -a wwcode-chtools-api
```

* To set a config for secret_key or anything else
```
heroku config:set SECRET_KEY=SOME_SECRET_VALUE -a wwcode-chtools-api
```