from datetime import datetime

from doctor_service.models.doctor import Doctor
from doctor_service.services.sqlite_service import SQLiteService


class DoctorDataService:

    def __init__(self, db_service):
        if not isinstance(db_service, SQLiteService):
            raise TypeError('db_service must be an instance of SQLiteService')
        self.db_service = db_service

        self.db_table = 'doctors'

    def read(self, docid):
        if not isinstance(docid, int):
            raise TypeError('docid must be int')

        return self._get_doctor_by_id(docid)

    def index(self):
        result = []
        fields = ['docid', 'first_name', 'last_name']

        try:
            data = self.db_service.select_by_predicate(self.db_table, fields, "deleted_at IS NULL")
        except Exception as e:
            raise RuntimeError(e.message)

        for row in data:
            [docid, first_name, last_name] = row
            result.append(Doctor(docid, first_name, last_name))

        return result

    def create(self, first_name, last_name):
        if not isinstance(first_name, unicode) and not isinstance(first_name, str):
            raise TypeError('first_name must be string or unicode')

        if not isinstance(last_name, unicode) and not isinstance(last_name, str):
            raise TypeError('last_name must be string or unicode')

        try:
            field_values = {
                'first_name': "'" + first_name.strip() + "'",
                'last_name': "'" + last_name.strip() + "'",
                'created_at': int(datetime.utcnow().strftime("%s"))
            }
            docid = self.db_service.insert(self.db_table, field_values)
        except Exception as e:
            raise RuntimeError(e.message)

        return docid

    def update(self, docid, first_name=None, last_name=None):
        if not isinstance(docid, int):
            raise TypeError('docid must be int')

        if not self._get_doctor_by_id(docid):
            raise RuntimeError('Cannot modify non-existing record')

        updates = [
            "updated_at=%d" % int(datetime.utcnow().strftime("%s"))
        ]

        if first_name is not None:
            if not isinstance(first_name, unicode) and not isinstance(first_name, str):
                raise TypeError('first_name must be string or unicode')
            updates.append("first_name='%s'" % first_name.strip())

        if last_name is not None:
            if not isinstance(last_name, unicode) and not isinstance(last_name, str):
                raise TypeError('last_name must be string or unicode')
            updates.append("last_name='%s'" % last_name.strip())
        print updates
        try:
            self.db_service.update(self.db_table, updates, "docid=%d" % docid)
        except Exception as e:
            raise RuntimeError(e.message)

        return self._get_doctor_by_id(docid)

    def delete(self, docid):
        if not isinstance(docid, int):
            raise TypeError('docid must be int')

        updates = ["deleted_at=%d" % int(datetime.utcnow().strftime("%s"))]

        try:
            self.db_service.update(self.db_table, updates, "docid=%d" % docid)
        except Exception as e:
            raise RuntimeError(e.message)

        return

    def _get_doctor_by_id(self, docid):
        fields = ['docid', 'first_name', 'last_name']
        try:
            [docid, first_name, last_name] = \
                self.db_service.select_by_predicate(self.db_table, fields, "docid=%d AND deleted_at IS NULL" % docid)[0]
        except Exception as e:
            if e.message == 'list index out of range':
                return None  # Not an error
            raise RuntimeError(e.message)

        return Doctor(docid, first_name, last_name)


