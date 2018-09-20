# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

from flask import Flask


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(config)

    register_blueprints(app)

    return app


def register_blueprints(app):
    # Import and register blueprints here.
    from doctor_service.example import api as exampleapi
    from services.doctor_api_service import doctor_api
    from services.appointments_api_service import appointments_api

    app.register_blueprint(exampleapi.example_api)
    app.register_blueprint(doctor_api)
    app.register_blueprint(appointments_api)
