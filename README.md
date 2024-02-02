# WBES Project

Ecommerce web application project using Django (python) and Gulp (nodejs), started January 2024.

# Setup

## Prerequisites

The following are installed in order to clone or replicate the project. You can pull this repository in your local files once you already have the listed prerequisites.

General
- **Browser**: to access the webapp.
- **VS Code**: used for development.
- **Git**: used for code repository.

Front-end
- **Nodejs**: `npm` is needed.
- **Gulp**: use the command `npm install -g gulp` to install.

Back-end
- **Python**: for the actual web framework, Django.
- **Pip**: install latest pip by using `py -m pip install --upgrade pip `.
- **Virtual Environment**: install with `pip install virtualenvwrapper`.

## Dependencies

To install the **nodejs** dependencies, simply do the following.

1. Open the project in VS Code (root folder `wbes-app-2024`), then open the terminal.
2. In the terminal, enter the command `npm install`.
3. Check if you have the folder `/node_modules`.

To install the **python** dependencies needed, simply do the following.

1. Open the project in VS Code (root folder `wbes-app-2024`), then open the terminal.
2. Make a virtual environment in the root folder by simply using the command `python -m venv PyEnv`. It is important that the name is *PyEnv* so that github will ignore this folder moving forward.
3. `Ctrl + Shift + P` to open the command palette, and type "*Select Interpreter*". Choose `Python: Select Interpreter`.
4. Click "+ Enter interpreter path...", click "Find...", and navigate inside the PyEnv folder and select `/PyEnv/Scripts/python.exe`.
5. Open another terminal in VS Code to activate the Python Environment; `(PyEnv)` should be at the beginning of each line. 
6. Go to `/py_requirements.txt`, copy the pip installation code inside the file, paste it in the terminal, and hit enter.
7. Try running the server (`py manage.py runserver`)

## Database

- The current database uses `sqlite3`.
- It is included in the git repository with the file name `db.sqlite3`.

In case you want to reset the database

- Rename the current one to have a backup.
- In the terminal, enter the command `py manage.py migrate`. This will create a new `db.sqlite3`.
- Then create a superuser with the command `py manage.py createsuperuser` to be able to login.

## Setup Footnote

In case you want to see the full documentation, e.g. the general webapp setup, how to setup the authenticated login, etc., kindly access the folder `/dason/documentation`, and you will see `setup.html`, `socialloginsetup.html`, etc.

# Code Workflow

This section describes how to work on the current state of the code considering that the whole front-end is from a preset design supposedly called "Dason" developed by "Themesbrand". The items below will help you guide in connecting the back-end to the front-end.

The process has three parts: 
1. Links in *templates* 
2. URL in `urls.py`
3. Process in `views.py` 

## ***Consider the link or url of the action.***

For example, accessing a page requires you to change the url in the `/templates/partials/left-sidebar.html`, or maybe the `/templates/partials/header.html`.

html
```
<li>
    <a href="{% url 'apps:calendar' %}">
        <i data-feather="calendar"></i>
        <span data-key="t-calendar">Calendar</span>
    </a>
</li>
```
urls.py
```
...
path("calendar/", view=apps_calendar_calendar_view, name="calendar"),
...
```

So in one more example, it could look like below, wherein the url can have extra slashes.

html
```
<li>
    <a href="{% url 'apps:offices/add/external' %}">
        <span> Add External Office </span>
    </a>
</li>
```
urls.py
```
...
path("offices/add/external", view=apps_add_external_office_view, name="add.external.office"),
...
```

## ***Another instance to consider is when using Ajax calls.***

For instance, when fetching the rooms in `/templates/apps/apps-calendar.html`.
```
$.ajax({
    url: `get_rooms`,
    data: {building_id: this.value},
    success: function (response) {
        
        $('#select-conference-room option').remove();
        disableSubmitRoom(false);

        if (response.rooms) {
            for (const room of JSON.parse(response.rooms)) {
                $('#select-conference-room').append(
                    $("<option>").text(room.name).attr('value', room.id)
                );
            }
        }
    },
});
```
The urls.py would be the following. This is because we are already in `domain.com/calendar` when we enter the Calendar page, so just call `/get_rooms` in Ajax.
```
...
path("calendar/get_rooms/", view=apps_calendar_get_rooms, name="calendar.get.rooms"),
...
```

## ***Process in views.py with a structure in mind***

The current structure uses *class-based views*. For example, supposed we need a view function for the Office, then it could maybe look like the following, in one code block.
```
class EcommerceOfficeView(LoginRequiredMixin, TemplateView): 
    # the parameter "TemplateView" is to inherit the class-based template as view
    # the parameter "LoginRequiredMixin" is to inherit the class property - can only be accessed if logged in

    # this get function processes all GET requests
    def get(request):
        context = {}
        # ... process here ...
        return render(request, self.template_name, context)

    # similarly, this function processes all POSTS requests
    def post(request):
        context = {}
        # ... process here ...
        return render(request, self.template_name, context)

# for example, the template has a path of "/templates/apps/apps-offices.html"
# supply the template name, this is called by self.template_name inside the class
# call "apps_office_view" in the urls.py as the function for the url
apps_office_view = EcommerceOfficeView.as_view("apps/apps-offices.html")
```

## Footnotes

Since the front-end is a preset code, a diligent reverse engineering is really needed to determine where changes are needed to be made. It could be in the JavaScript files, or it could be in an HTML file, and so on.
