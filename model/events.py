# This model can be any type of model you like

class Events:

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'owner': self.owner,
            'datetime': self.datetime,
        }

    def insert_record(self, name,
                      description,
                      owner,
                      datetime):
        return True
