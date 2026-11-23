-- Create the project tables. This file contains no accounts or other records.
CREATE TABLE IF NOT EXISTS rifles (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    cartridge TEXT NOT NULL DEFAULT 'unknown',
    action_type TEXT NOT NULL DEFAULT 'unknown',
    barrel_length_in TEXT NOT NULL DEFAULT 'unknown',
    adoption_year TEXT NOT NULL DEFAULT 'unknown',
    weight_lb TEXT NOT NULL DEFAULT 'unknown',
    standard_capacity TEXT NOT NULL DEFAULT 'unknown',
    adoption_branch TEXT NOT NULL DEFAULT 'unknown'
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER NOT NULL PRIMARY KEY,
    fname TEXT NOT NULL,
    lname TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    pass TEXT NOT NULL
);
