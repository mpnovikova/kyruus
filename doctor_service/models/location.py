class Location:
    locid = None
    address = None

    def __init__(self, locid, address):
        # Simplified model for now. If need could be extended into more parsable location: addrline1, addreline2, city,
        # state,
        if not isinstance(locid, int):
            raise TypeError('docid must be int')
        self.locid = locid

        if not isinstance(address, unicode) and not isinstance(address, str):
            raise TypeError('address must be string or unicode')
        self.address = address

    def get_id(self):
        return self.locid

    def get_address(self):
        return self.address

    def to_dict(self):
        return {
            'locid': self.locid,
            'address': self.address
        }
