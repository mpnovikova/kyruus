# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

from flask import Blueprint, jsonify, request

from doctor_service.exceptions.api_error import ApiError

from doctor_service.services.service_container import ServiceContainer


doctor_api = Blueprint('doctor_api', __name__, url_prefix='')
service_container = ServiceContainer()


@doctor_api.route('/doctors', methods=['GET'])
def index():
    if not request.method == 'GET':
        raise ApiError('Invalid request', status_code=400)

    response = []

    result = service_container.doctor_data_service().index()
    for doc in result:
        response.append(doc.to_dict())

    return jsonify({'response': response}), 200


@doctor_api.route('/doctors', methods=['POST'])
def create():
    if not request.method == 'POST':
        raise ApiError('Invalid request', status_code=400)

    try:
        response = service_container.doctor_data_service().create(
            first_name=request.json.get('first_name'),
            last_name=request.json.get('last_name'))
    except (TypeError, RuntimeError) as e:
        raise ApiError(e.message, status_code=400)

    return jsonify({'response': response}), 201


@doctor_api.route('/doctors/<docid>', methods=['GET'])
def read(docid):
    if not request.method == 'GET':
        raise ApiError('Invalid request', status_code=400)
    try:
        doctor = service_container.doctor_data_service().read(docid=docid)
    except (TypeError, RuntimeError) as e:
        raise ApiError(e.message, status_code=400)

    if doctor is None:
        raise ApiError('Doctor not found', status_code=404)

    return jsonify({'response': doctor.to_dict()}), 200


@doctor_api.route('/doctors/<docid>', methods=['PUT'])
def update(docid):
    if not request.method == 'PUT':
        raise ApiError('Invalid request', status_code=400)

    try:
        doctor = service_container.doctor_data_service().update(
            docid=docid,
            first_name=request.json.get('first_name'),
            last_name=request.json.get('last_name'))
    except (TypeError, RuntimeError) as e:
        raise ApiError(e.message, status_code=400)

    return jsonify({'response': doctor.to_dict()}), 200


@doctor_api.route('/doctors/<docid>', methods=['DELETE'])
def delete(docid):
    if not request.method == 'DELETE':
        raise ApiError('Invalid request', status_code=400)

    try:
        service_container.doctor_data_service().delete(docid=docid)
        return jsonify({}), 204
    except (TypeError, RuntimeError) as e:
        raise ApiError(e.message, status_code=400)


@doctor_api.errorhandler(ApiError)
def handle_api_error(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

