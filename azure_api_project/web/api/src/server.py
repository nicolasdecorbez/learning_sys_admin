"""
Start the API to retrive data and call functions
to create audio and configuration files.
"""

from dataclasses import dataclass
from sanic import Sanic
from sanic.response import json
from src import file_creator


# Call the Sanic Framework to create the API.
app = Sanic("Step1 API")


@dataclass
class DataFromRequest:
    """Create a list of parameters from previous request."""

    max_allowed: str
    message: str


def store_data(max_allowed, message):
    """Format and store data received."""

    data = DataFromRequest(
        max_allowed,
        message
    )
    return data


def launch_api():
    """Launch the sanic API."""

    app.run(host='0.0.0.0', port=8000, access_log=False)


@app.post("/data")
async def retrive_data(request):
    """Retrive data from request and send it."""

    max_allowed = request.form.get("max_allowed")
    message = request.form.get("message")
    request_data = store_data(max_allowed, message)
    file_creator.generate_files(request_data)
    return json({"received": True}, status=200)
