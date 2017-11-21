class SceneModel:
    def __init__(self, db, sceneID=None):
        self.db = db
        self.c = self.db.conn.cursor()
        self.sceneID = sceneID
        self.populate()

    def populate(self):
        """Update properties from the DB"""
        query = "SELECT title, description FROM Scene WHERE sceneID=" + \
            str(self.sceneID)
        self.c.execute(query)
        result = self.c.fetchone()
        self.title = result[0]
        self.description = result[1]

        # Get characters in scene
        query = "SELECT characterID, fullName FROM Character"
        self.c.execute(query)
        IDs = self.c.fetchall()
        self.notInSceneCharacters = {}
        for ID in IDs:
            self.notInSceneCharacters[ID[0]] = ID[1]
        query = "SELECT CharacterInScene.characterID, Character.fullName " + \
            "FROM CharacterInScene JOIN Character ON Character.characterID=CharacterInScene.characterID " + \
                "WHERE CharacterInScene.sceneID=" + str(self.sceneID)
        self.c.execute(query)
        IDs = self.c.fetchall()
        self.inSceneCharacters = {}
        for ID in IDs:
            self.inSceneCharacters[ID[0]] = ID[1]
        for ID in self.inSceneCharacters.keys():
            del self.notInSceneCharacters[ID]

    def commit(self):
        """Store any changes in the DB"""
        query = "UPDATE Scene SET title=?, description=? WHERE sceneID=?"
        self.c.execute(query, (self.title, self.description, self.sceneID))
        self.db.conn.commit()

    def remove(self):
        """Remove self from the DB"""
        pass
