DROP TABLE IF EXISTS Section;
DROP VIEW IF EXISTS SectionView;
DROP TABLE IF EXISTS Scene;
DROP VIEW IF EXISTS SceneView;
DROP TABLE IF EXISTS CharacterInScene;
DROP TABLE IF EXISTS Character;
DROP TABLE IF EXISTS Revision;
DROP TRIGGER IF EXISTS InsertSection;
DROP TRIGGER IF EXISTS DeleteSection;
DROP TRIGGER IF EXISTS UpdateSectionUp;
DROP TRIGGER IF EXISTS UpdateSectionDown;
DROP TRIGGER IF EXISTS InsertScene;
DROP TRIGGER IF EXISTS DeleteScene;
DROP TRIGGER IF EXISTS UpdateSceneUp;
DROP TRIGGER IF EXISTS UpdateSceneDown;

CREATE TABLE Section (
    sectionID INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    sectionOrder INTEGER NOT NULL,
    parentID INTEGER NOT NULL,
    FOREIGN KEY (parentID) REFERENCES Section (sectionID)
);

CREATE VIEW SectionView AS SELECT * FROM Section;

CREATE TRIGGER InsertSection INSTEAD OF INSERT ON SectionView
BEGIN
    UPDATE Section SET sectionOrder = sectionOrder + 1 WHERE sectionOrder >= NEW.sectionOrder;
    INSERT INTO Section (name, description, sectionOrder, parentID) VALUES (NEW.name, NEW.description, new.sectionOrder, new.parentID);
END;

CREATE TRIGGER DeleteSection INSTEAD OF DELETE ON SectionView
BEGIN
    UPDATE Section SET sectionOrder = sectionOrder - 1 WHERE sectionOrder > OLD.sectionOrder;
    DELETE FROM Section WHERE sectionID = OLD.sectionID;
END;

CREATE TRIGGER UpdateSectionUp INSTEAD OF UPDATE ON SectionView
WHEN OLD.sectionOrder < NEW.sectionOrder
BEGIN
    UPDATE Section SET sectionOrder = sectionOrder - 1 WHERE sectionOrder > OLD.sectionOrder AND sectionOrder <= NEW.sectionOrder;
    UPDATE Section SET name = NEW.name, description = NEW.description, sectionOrder = NEW.sectionOrder, parentID = NEW.parentID WHERE sectionID = NEW.sectionID;
END;

CREATE TRIGGER UpdateSectionDown INSTEAD OF UPDATE ON SectionView
WHEN OLD.sectionOrder > NEW.sectionOrder
BEGIN
    UPDATE Section SET sectionOrder = sectionOrder + 1 WHERE sectionOrder < OLD.sectionOrder AND sectionOrder >= NEW.sectionOrder;
    UPDATE Section SET name = NEW.name, description = NEW.description, sectionOrder = NEW.sectionOrder, parentID = NEW.parentID WHERE sectionID = NEW.sectionID;
END;

CREATE TABLE Scene (
    sceneID INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    revisionID INTEGER NOT NULL,
    sectionID INTEGER NOT NULL,
    sceneOrder INTEGER NOT NULL,
    FOREIGN KEY(revisionID) REFERENCES Revision(revisionID),
    FOREIGN KEY(sectionID) REFERENCES Section(sectionID)
);

CREATE VIEW SceneView AS SELECT * FROM Scene;

CREATE TRIGGER InsertScene INSTEAD OF INSERT ON SceneView
BEGIN
    UPDATE Scene SET sceneOrder = sceneOrder + 1 WHERE sceneOrder >= NEW.sceneOrder AND sectionID = NEW.sectionID;
    INSERT INTO Scene VALUES (NEW.sceneID, NEW.title, NEW.description, NEW.revisionID, NEW.sectionID, NEW.sceneOrder);
END;

CREATE TRIGGER DeleteScene INSTEAD OF DELETE ON SceneView
BEGIN
    UPDATE Scene SET sceneOrder = sceneOrder - 1 WHERE sceneOrder > OLD.sceneOrder AND sectionID = OLD.sectionID;
    DELETE FROM Scene WHERE sceneID = OLD.sceneID;
END;

CREATE TRIGGER UpdateSceneUp INSTEAD OF UPDATE ON SceneView
WHEN OLD.sceneOrder < NEW.sceneOrder
BEGIN
    UPDATE Scene SET sceneOrder = sceneOrder - 1 WHERE sceneOrder > OLD.sceneOrder AND sceneOrder <= NEW.sceneOrder AND sectionID = OLD.sectionID;
    UPDATE Scene SET title = NEW.title, description = NEW.description, revisionID = NEW.revisionID, sectionID = NEW.sectionID, sceneOrder = NEW.sceneOrder WHERE sceneID = NEW.sceneID;
END;

CREATE TRIGGER UpdateSceneDown INSTEAD OF UPDATE ON SceneView
WHEN OLD.sceneOrder > NEW.sceneOrder
BEGIN
    UPDATE Scene SET sceneOrder = sceneOrder + 1 WHERE sceneOrder < OLD.sceneOrder AND sceneOrder >= NEW.sceneOrder AND sectionID = OLD.sectionID;
    UPDATE Scene SET title = NEW.title, description = NEW.description, revisionID = NEW.revisionID, sectionID = NEW.sectionID, sceneOrder = NEW.sceneOrder WHERE sceneID = NEW.sceneID;
END;

CREATE TABLE Character (
    characterID INTEGER PRIMARY KEY,
    fullName TEXT NOT NULL,
    shortName TEXT NOT NULL,
    description TEXT NOT NULL,
    bio TEXT NOT NULL
);

CREATE TABLE CharacterInScene (
    characterID INTEGER,
    sceneID INTEGER,
    PRIMARY KEY(characterID, sceneID),
    FOREIGN KEY(characterID) REFERENCES Character(characterID),
    FOREIGN KEY(sceneID) REFERENCES Scene(sceneID)
);

CREATE TABLE Revision (
    revisionID INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);