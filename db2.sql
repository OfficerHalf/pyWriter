DROP TABLE IF EXISTS Section;
DROP TABLE IF EXISTS SectionTree;
DROP TABLE IF EXISTS Scene;
DROP TABLE IF EXISTS CharacterInScene;
DROP TABLE IF EXISTS Character;
DROP TABLE IF EXISTS Revision;
DROP TRIGGER IF EXISTS SectionUpdateOrderOnDelete;
DROP TRIGGER IF EXISTS SectionUpdateOrderOnInsert;
DROP TRIGGER IF EXISTS SectionUpdateOrderOnUpdateDown;
DROP TRIGGER IF EXISTS SectionUpdateOrderOnUpdateUp;

CREATE TABLE Section (
    sectionID INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    sOrder INTEGER NOT NULL,
    parentID INTEGER NOT NULL,
    FOREIGN KEY (parentID) REFERENCES Section (sectionID)
);

CREATE TRIGGER SectionUpdateOrderOnInsert BEFORE INSERT ON Section
BEGIN
    UPDATE Section SET sOrder = sOrder + 1 WHERE sOrder >= NEW.sOrder;
END;

INSERT INTO Section VALUES (1, "Part I", 1, 1);
INSERT INTO Section VALUES (2, "Part II", 2, 2);
INSERT INTO Section VALUES (3, "Chapter 1", 3, 1);
INSERT INTO Section VALUES (4, "Chapter 2", 4, 1);
INSERT INTO Section VALUES (5, "Chapter 1.5", 3, 1);