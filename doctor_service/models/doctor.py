class Doctor:
    docid = None
    fist_name = None
    last_name = None

    def __init__(self, docid, first_name, last_name):
        if not isinstance(docid, int):
            raise TypeError('docid must be string or unicode')
        self.docid = docid

        if not isinstance(first_name, unicode) and not isinstance(first_name, str):
            raise TypeError('first_name must be a string or unicode')
        self.first_name = first_name.strip()

        if not isinstance(last_name, unicode) and not isinstance(last_name, str):
            raise TypeError('last_name must be a string or unicode')
        self.last_name = last_name.strip()

    def get_id(self):
        return self.docid

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def to_dict(self):
        return {
            'docid': self.docid,
            'first_name': self.first_name,
            'last_name': self.last_name
        }
