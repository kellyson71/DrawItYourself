# DrawItYourself
 
## Running the project

### Install dependencies

```
pip install -r requirements.txt
```

### Define environment variables (if any)
Whatever environment variables that are used in the system must be defined in a `.env` file.
Those variables must be included in the `.env-EXAMPLE` so other developer may know what is necessary.

### Load migrations

```py manage.py migrate```

### Run server

```py manage.py runserver```

## About development
Whatever feature is being developed, I suggest that a seperate branch from `main` must be made. Besides that,
I'd say that, instead of merging directly to the `main` branch, it is made a pull request and requested a review,
in order to have a good quality of code and avoid conflicts.