from sqlite3 import Connection


class SQLiteService:
    db_name = None

    def __init__(self, db_client):
        if not isinstance(db_client, Connection):
            raise TypeError('db_client must be sqlite3.Connection')
        self.db_client = db_client

    def select_all(self, table, fields):
        cursor = self.db_client.cursor()

        query = "SELECT %s FROM %s" % (",".join(fields), table)

        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def select_by_predicate(self, table, fields, predicate):
        cursor = self.db_client.cursor()

        query = "SELECT %s FROM %s WHERE %s" % (",".join(fields), table, predicate)
        print query
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def insert(self, table, field_values):
        cursor = self.db_client.cursor()

        fields = []
        values = []

        for field, value in field_values.items():
            fields.append(field)
            values.append(str(value))

        query = "INSERT INTO %s(%s) VALUES(%s)" % (table, ",".join(fields), ",".join(values))

        cursor.execute(query)
        result = cursor.lastrowid
        self.db_client.commit()
        return result

    def update(self, table, rowid, updates):
        cursor = self.db_client.cursor()

        query = "UPDATE %s SET %s WHERE rowid=%d" % (table, ",".join(updates), rowid)

        cursor.execute(query)
        self.db_client.commit()
