import urllib

class Location(object):
    
    def __init__(self, address=None, lat=None, lng=None):
        self.address = address
        self.urlencoded_address = urllib.quote_plus(address) if address else None
        self.lat = lat
        self.lng = lng
    
    def __str__(self):
        if self.lat and self.lng:
            return '%s,%s' % (self.lat, self.lng)
        else:
            return self.urlencoded_address
    
    __repr__ = __str__

    def __hash__(self):
        return hash((self.address, self.lat, self.lng,))
    
    def __eq__(self, other):
        return self.address == other.address or (self.lat == other.lat and self.lng == other.lng)
