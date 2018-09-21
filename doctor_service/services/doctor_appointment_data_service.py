from datetime import datetime

from doctor_service.models.appointment import Appointment
from doctor_service.models.doctor import Doctor
from doctor_service.models.location import Location
from doctor_service.services.sqlite_service import SQLiteService


class DoctorAppointmentDataService:
    def __init__(self, db_service):
        if not isinstance(db_service, SQLiteService):
            raise TypeError('db_service must be an instance of SQLiteService')
        self.db_service = db_service

        self.db_table = '''schedule
            INNER JOIN doctors ON doctors.docid = schedule.docid
            INNER JOIN locations ON locations.locid = schedule.locid
            INNER JOIN slots ON slots.slotid = schedule.slotid
        '''

        self.db_fields = [
            'doctors.docid',
            'schedule.app_date',
            'slots.slot_start',
            'doctors.first_name',
            'doctors.last_name',
            'locations.locid',
            'locations.address'
        ]

    def index(self, docid):
        if not isinstance(docid, int):
            raise TypeError('docid must be int')

        return self._get_appointments_for_doctor(docid)

    def create(self, docid, locid, app_datetime):
        if not isinstance(docid, int):
            raise TypeError('docid must be int')

        if not isinstance(locid, int):
            raise TypeError('locid int')

        if not isinstance(app_datetime, int):
            raise TypeError('app_datetime must be int')

        try:
            app_datetime_utc = datetime.utcfromtimestamp(app_datetime)
        except Exception as e:
            raise RuntimeError(e.message)

        app_date_utc = int(datetime(app_datetime_utc.year, app_datetime_utc.month, app_datetime_utc.day).strftime("%s"))
        app_slot = app_datetime_utc.strftime("%H%M")

        existing_appointment = self._get_appointments_for_doctor_location_datetime(
            docid, locid, app_date_utc, app_slot)

        if existing_appointment:
            raise RuntimeError('Appointment for this doctor, location and time already exists')

        field_values = {
            'app_date': app_date_utc,
            'docid': docid,
            'locid': locid,
            'slotid': "(SELECT slotid FROM slots WHERE slot_start='%s' )" % app_slot,
            'created_at': int(datetime.utcnow().strftime("%s"))
        }

        try:
            self.db_service.insert('schedule', field_values)
        except Exception as e:
            raise RuntimeError(e.message)

        return self._get_appointments_for_doctor_location_datetime(docid, locid, app_date_utc, app_slot)

    def delete(self, docid, locid, app_datetime):
        if not isinstance(docid, int):
            raise TypeError('docid must be int')

        if not isinstance(locid, int):
            raise TypeError('locid int')

        if not isinstance(app_datetime, int):
            raise TypeError('app_datetime must be int')

        try:
            app_datetime_utc = datetime.utcfromtimestamp(app_datetime)
        except Exception as e:
            raise RuntimeError(e.message)

        app_date_utc = int(datetime(app_datetime_utc.year, app_datetime_utc.month, app_datetime_utc.day).strftime("%s"))
        app_slot = app_datetime_utc.strftime("%H%M")

        existing_appointment = self._get_appointments_for_doctor_location_datetime(
            docid, locid, app_date_utc, app_slot)

        if not existing_appointment:
            raise RuntimeError('Cannot cancel appointment that doesn\'t exist')

        table = "schedule"

        updates = [
            "deleted_at=%d" % int(datetime.utcnow().strftime("%s"))
        ]
        predicate = \
            "docid=%d AND locid=%d AND app_date=%d AND slotid IN (SELECT slotid FROM slots WHERE slot_start='%s')" % \
            (docid, locid, app_date_utc, app_slot)

        self.db_service.update(table, updates, predicate)

    def _get_appointments_for_doctor(self, docid):
        predicate = "schedule.docid=%d AND schedule.deleted_at IS NULL" % docid

        data = self.db_service.select_by_predicate(self.db_table, self.db_fields, predicate)

        return [Appointment.from_datarow(row) for row in data]

    def _get_appointments_for_doctor_location_datetime(self, docid, locid, app_date, app_slot):
        predicate = "doctors.docid=%d AND locations.locid=%d AND schedule.app_date=%d AND slots.slot_start='%s' AND schedule.deleted_at IS NULL" % \
                    (docid, locid, app_date, app_slot)

        try:
            data = self.db_service.select_by_predicate(self.db_table, self.db_fields, predicate)
        except Exception as e:
                raise RuntimeError(e.message)

        return Appointment.from_datarow(data[0]) if len(data) else None

