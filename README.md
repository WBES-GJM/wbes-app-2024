# WBES Project

Ecommerce project, started January 2024

# Setup

## Prerequisites

The following are installed in order to clone or replicate the project. You can pull this repository in your local files once you already have the listed prerequisites.

General
- **Browser**: to access the webapp.
- **VS Code**: used for development.
- **Git**: used for code repository.

Front-end
- **Nodejs**:`npm` is needed.
- **Gulp**: use the command `npm install -g gulp` to install.

Back-end
- **Python**: for the actual web framework, Django.
- **Pip**: install latest pip by using `py -m pip install --upgrade pip `.
- **Virtual Environment**: install with `pip install virtualenvwrapper`.

## Python Dependencies

To install the python dependencies needed, follow the steps below.

1. Open the project in VS Code (root folder `wbes-app-2024`), then open the terminal.
2. Make a virtual environment in the root folder by simply using the command `python -m venv PyEnv`. It is important that the name is *PyEnv* so that github will ignore this folder moving forward.
3. `Ctrl + Shift + P` to open the command palette, and type `Select Interpreter`. Choose `Python: Select Interpreter`.
4. Click `+ Enter interpreter path...`, click `Find...`, and navigate inside the PyEnv folder and select (`/PyEnv/Scripts/python.exe`).
5. Open another terminal to activate the Python Environment, and you should be able to see `(PyEnv)` at the beginning of each line. 
6. Go to `/py_requirements.txt`, copy the pip installation code inside the file, paste it in the terminal, and hit enter.
7. Try running the server (`py manage.py runserver`)

## Database

- The current database uses `sqlite3`.
- It is included in the git repository with the file name `db.sqlite3`.

In case you want to reset the database
- Rename the current one to have a backup.
- In the terminal, enter the command `py manage.py migrate`.
- Then create a superuser with the command `py manage.py createsuperuser` to be able to login.

# Footnotes

In case you want to see the full documentation, e.g. the general webapp setup, how to setup the authenticated login, etc., kindly access the folder `/dason/documentation`, and you will see `setup.html`, `socialloginsetup.html`, etc.


