BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "tasks" (
	"id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"title"	varchar(100),
	"description"	TEXT,
	"created_at"	datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
	"status"	varchar(50) NOT NULL DEFAULT 'Pending'
);
COMMIT;
