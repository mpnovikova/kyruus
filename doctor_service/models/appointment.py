from datetime import datetime

from doctor_service.models.doctor import Doctor
from doctor_service.models.location import Location


class Appointment:
    def __init__(self, apt_datetime, doctor, location):
        if not isinstance(apt_datetime, datetime):
            raise TypeError('apt_datetime must be an instance of datetime')
        self.apt_datetime = apt_datetime

        if not isinstance(doctor, Doctor):
            raise TypeError('doctor must be an instance of Doctor')
        self.doctor = doctor

        if not isinstance(location, Location):
            raise TypeError('location must be an instance of Location')
        self.location = location

    def get_datetime(self):
        return self.apt_datetime

    def get_doctor(self):
        return self.doctor

    def get_location(self):
        return self.location

    def to_dict(self):
        return {
            'datetime': self.apt_datetime.isoformat(),
            'doctor': self.doctor.to_dict(),
            'location': self.location.to_dict()
        }

    @staticmethod
    def get_apt_datetime(timestamp, slot):
        apt_date = datetime.fromtimestamp(timestamp)
        hour = slot[:2]
        minute = slot[2:]
        # For simplicity lets assume we store all appointment in UTC
        return datetime(int(apt_date.year), int(apt_date.month), int(apt_date.day), int(hour), int(minute), tzinfo=None)

    @staticmethod
    def from_datarow(datarow):
        [docid, app_date, slot_start, first_name, last_name, locid, address] = datarow

        doctor = Doctor(docid, first_name, last_name)
        location = Location(locid, address)
        app_datetime = Appointment.get_apt_datetime(int(app_date), slot_start)

        return Appointment(app_datetime, doctor, location)