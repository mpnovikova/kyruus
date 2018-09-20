from datetime import datetime
from dateutil.parser import *

from doctor_service.models.appointment import Appointment
from doctor_service.models.doctor import Doctor
from doctor_service.models.location import Location
from doctor_service.services.sqlite_service import SQLiteService


class DoctorAppointmentDataService:
    def __init__(self, db_service):
        if not isinstance(db_service, SQLiteService):
            raise TypeError('db_service must be an instance of SQLiteService')
        self.db_service = db_service

        self.db_table = 'schedule'
        self.db_fields = ['app_date', 'docid', 'locid', 'slotid']

    def index(self, docid):
        if not isinstance(docid, unicode) and not isinstance(docid, str):
            raise TypeError('docid must be string or unicode')

        return self._get_appointments_for_doctor(int(docid.strip()))

    def read(self):
        pass

    def create(self, docid, locid, app_datetime):
        if not isinstance(docid, unicode) and not isinstance(docid, str):
            raise TypeError('docid must be string or unicode')

        if not isinstance(locid, unicode) and not isinstance(locid, str):
            raise TypeError('locid must be string or unicode')

        if not isinstance(app_datetime, unicode) and not isinstance(app_datetime, str):
            raise TypeError('app_datetime must be string or unicode')

        try:
            app_datetime_tz = parser(app_datetime)
        except Exception as e:
            raise RuntimeError(e.message)

        utc_offset_timedelta = datetime.utcnow() - app_datetime_tz
        app_datetime_utc = app_datetime_tz + utc_offset_timedelta

        values = [
            app_datetime_utc.strftime("%Y-%m-%d"),
            docid.strip(),
            locid.strip(),
            self._get_slotid(app_datetime_utc)
        ]
        try:
            app_id = self.db_service.insert(self.db_table, self.db_fields, values)
        except Exception as e:
            raise RuntimeError(e.message)

        return app_id

    def update(self, _id, *args):
        pass

    def delete(self, _id):
        pass

    def _get_appointments_for_doctor(self, docid):
        result = []

        table = '''schedule
            INNER JOIN doctors ON doctors.docid = schedule.docid
            INNER JOIN locations ON locations.locid = schedule.locid
            INNER JOIN slots ON slots.slotid = schedule.slotid
        '''

        fields = [
            'schedule.app_date',
            'slots.slot_start',
            'doctors.first_name',
            'doctors.last_name',
            'locations.locid',
            'locations.address'
        ]

        predicate = "schedule.docid=%d" % docid

        data = self.db_service.select_by_predicate(table, fields, predicate)

        for row in data:
            print row
            [app_date, slot_start, first_name, last_name, locid, address] = row
            doctor = Doctor(docid, first_name, last_name)
            print doctor
            location = Location(locid, address)
            print location
            app_datetime = Appointment.get_apt_datetime(app_date, slot_start)
            print app_datetime

            result.append(Appointment(app_datetime, doctor, location))

        return result

    def _get_slotid(self, datetime_utc):
        slot = datetime_utc.strftime("%H%M")
        try:
            result = self.db_service.read('slots', ['slotid'], "slot_start=%s" % slot)
        except:
            raise ValueError('Unknown slot')
        return result[0]

