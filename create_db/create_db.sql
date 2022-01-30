PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS category;
CREATE TABLE category(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE
    , name VARCHAR(32)
    , parent_category INT
    , FOREIGN KEY (parent_category) REFERENCES category(id)
                     );

DROP TABLE IF EXISTS product;
CREATE TABLE product(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE
    , name VARCHAR(32)
    , category_id INT
    , price REAL(5, 2) DEFAULT 0
    , wight REAL(5, 2)
    , volume REAL(5, 2)
    , FOREIGN KEY (category_id) REFERENCES category(id)
                     );

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
