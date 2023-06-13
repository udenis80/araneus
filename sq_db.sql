CREATE TABLE IF NOT EXISTS mainmenu (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
image BLOB DEFAULT NULL,
image_id INTEGER,
text text NOT NULL,
url text NOT NULL,
time integer NOT NULL
);