import os
import sqlite3

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Factory

from doctor_service.services.doctor_appointment_data_service import DoctorAppointmentDataService
from doctor_service.services.doctor_data_service import DoctorDataService
from doctor_service.services.sqlite_service import SQLiteService


class ServiceContainer(DeclarativeContainer):
    basedir = os.path.abspath(os.path.dirname(__file__))

    db_client = Factory(sqlite3.connect, basedir + '/../data/database.sqlite')

    db_service = Factory(SQLiteService, db_client=db_client)

    doctor_data_service = Factory(DoctorDataService, db_service=db_service)

    appointments_data_service = Factory(DoctorAppointmentDataService, db_service=db_service)
