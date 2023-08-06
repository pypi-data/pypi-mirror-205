DROP TABLE IF EXISTS exa;

CREATE TABLE "exa" (
	"id"	INTEGER NOT NULL,
	"created"	TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"title"	TEXT NOT NULL,
	"col_1" TEXT,
	"col_2" TEXT,
	"col_3" TEXT,
	"col_4" TEXT,
	"col_5" TEXT,
	"col_6" TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
)
;
