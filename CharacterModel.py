class CharacterModel:
    def __init__(self, db, characterID=None):
        self.db = db
        self.c = self.db.conn.cursor()
        self.characterID = characterID
        self.populate()

    def populate(self):
        """Update properties from the DB"""
        query = "SELECT fullName, shortName, description, bio FROM Character WHERE characterID=" + \
            str(self.characterID)
        self.c.execute(query)
        result = self.c.fetchone()
        self.fullName = result[0]
        self.shortName = result[1]
        self.description = result[2]
        self.bio = result[3]

    def commit(self):
        """Store any changes in the DB"""
        query = "UPDATE Character SET fullName=?, shortName=?, description=?, bio=? WHERE characterID=?"
        self.c.execute(query, (self.fullName, self.shortName,
                               self.description, self.bio, self.characterID))
        self.db.conn.commit()

    def remove(self):
        """Remove self from the DB"""
        pass
