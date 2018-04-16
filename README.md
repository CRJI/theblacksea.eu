# How to install and run:

## Make the python virtualenv
```
pipenv install --skip-lock
pipenv shell
```

## Install PostgreSQL, create user and db
```
createdb tbs
```

## Install git-lfs and use it to clone the media&db repo, then copy it
```
cp -a tbs-backups/media ./
```

## Run it
```
./manage.py runserver
```
