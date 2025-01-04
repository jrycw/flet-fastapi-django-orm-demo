import os
from importlib.util import find_spec

from django.conf import settings
from django.core.wsgi import get_wsgi_application
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.staticfiles import StaticFiles

# Export Django settings env variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Get Django WSGI app
django_app = get_wsgi_application()

# Import a model
# And always import your models after you export settings
# and you get Django WSGI app
from django.contrib.auth.models import User  # noqa

# Create FasatAPI instance
app = FastAPI()

app.mount(
    "/static",
    StaticFiles(
        directory=os.path.normpath(
            os.path.join(find_spec("django.contrib.admin").origin,
                         "..", "static")
        )
    ),
    name="static",
)


@app.get("/fastapi/users")  # Define a FastAPI route
def users():
    usernames = [user.username for user in User.objects.all()]
    return {"usernames": usernames}


# Mount Django app
app.mount("/", WSGIMiddleware(django_app))
