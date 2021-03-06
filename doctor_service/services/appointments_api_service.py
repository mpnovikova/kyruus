# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

from flask import Blueprint, jsonify, request

from doctor_service.exceptions.api_error import ApiError
from doctor_service.services.service_container import ServiceContainer

appointments_api = Blueprint('appointment_api', __name__, url_prefix='')
service_container = ServiceContainer()
appointments_service = service_container.appointments_data_service()


@appointments_api.route('/doctors/<docid>/appointments', methods=['GET'])
def index(docid):
    if not request.method == 'GET':
        raise ApiError('Invalid request', status_code=400)

    response = []
    try:
        result = appointments_service.index(int(docid.strip()))
    except TypeError as e:
        raise ApiError(e.message, status_code=400)

    for apt in result:
        response.append(apt.to_dict())

    return jsonify({'response': response}), 200


@appointments_api.route('/doctors/<docid>/appointments', methods=['POST'])
def create(docid):
    if not request.method == 'POST':
        raise ApiError('Invalid request', status_code=400)

    try:
        appointment = appointments_service.create(
            docid=int(docid.strip()),
            locid=request.json.get('locid'),
            app_datetime=request.json.get('app_datetime')
        )
    except (TypeError, RuntimeError) as e:
        raise ApiError(e. message, status_code=400)

    return jsonify({'response': appointment.to_dict()}), 201


@appointments_api.route('/doctors/<docid>/appointments', methods=['DELETE'])
def cancel(docid):
    if not request.method == 'DELETE':
        raise ApiError('Invalid request', status_code=400)

    try:
        appointments_service.delete(
            docid=int(docid.strip()),
            locid=request.json.get('locid'),
            app_datetime=request.json.get('app_datetime')
        )
    except (TypeError, RuntimeError) as e:
        raise ApiError(e. message, status_code=400)

    return jsonify({}), 204


@appointments_api.errorhandler(ApiError)
def handle_api_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
