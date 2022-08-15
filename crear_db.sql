-- import to SQLite by running: sqlite3.exe db.sqlite3 -init sqlite.sql

-- PRAGMA journal_mode = MEMORY;
-- PRAGMA synchronous = OFF;
-- PRAGMA foreign_keys = OFF;
-- PRAGMA ignore_check_constraINTEGERs = OFF;
-- PRAGMA auto_vacuum = NONE;
-- PRAGMA secure_delete = OFF;
BEGIN TRANSACTION;

-- Drop all tables
DROP TABLE IF EXISTS Captures;
DROP TABLE IF EXISTS Languages;
DROP TABLE IF EXISTS Countries;
DROP TABLE IF EXISTS Official_Languages;
DROP TABLE IF EXISTS Regions;
DROP TABLE IF EXISTS Regions_Countries;
DROP TABLE IF EXISTS Speakers;
DROP TABLE IF EXISTS Speakers_Countries;

-- Create all tables
CREATE TABLE Languages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE Countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE Captures(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER NOT NULL,
    country_population INTEGER NOT NULL,
    country_id INTEGER NOT NULL,
    language_id INTEGER NOT NULL,
    local_speakers INTEGER NOT NULL,
    FOREIGN KEY(country_id) REFERENCES Countries(id),
    FOREIGN KEY(language_id) REFERENCES Languages(id)
);

CREATE TABLE Official_Languages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    language_id INTEGER NOT NULL,
    country_id INTEGER NOT NULL,
    FOREIGN KEY(language_id) REFERENCES Languages(id),
    FOREIGN KEY(country_id) REFERENCES Countries(id)
);

CREATE TABLE Regions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE Regions_Countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region_id INTEGER NOT NULL,
    country_id INTEGER NOT NULL,
    FOREIGN KEY(region_id) REFERENCES Regions(id),
    FOREIGN KEY(country_id) REFERENCES Countries(id)
);

CREATE TABLE Speakers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    native_speakers INTEGER NOT NULL,
    total_speakers INTEGER NOT NULL,
    year INTEGER NOT NULL
);

CREATE TABLE Speakers_Countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    speaker_id INTEGER NOT NULL,
    country_id INTEGER NOT NULL,
    FOREIGN KEY(speaker_id) REFERENCES Speakers(id),
    FOREIGN KEY(country_id) REFERENCES Countries(id)
);

COMMIT;
PRAGMA ignore_check_constraINTEGERs = ON;
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;