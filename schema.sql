CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER NOT NULL,
	"username"	TEXT NOT NULL UNIQUE,
	"email"	TEXT NOT NULL UNIQUE,
	"password_hash"	TEXT NOT NULL,
	"role"	TEXT NOT NULL,
	"created_at"	TEXT NOT NULL,
	"updated_at"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "session" (
	"id"	INTEGER,
	"user_id"	INT NOT NULL,
	"session_token"	TEXT NOT NULL,
	"expires_at"	TEXT NOT NULL,
	FOREIGN KEY("user_id") REFERENCES "users"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "order" (
	"id"	INTEGER NOT NULL UNIQUE,
	"user_id"	INTEGER NOT NULL,
	"status"	TEXT NOT NULL,
	"special_requests"	TEXT,
	"created_at"	TEXT NOT NULL,
	"updated_at"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("user_id") REFERENCES "users"("id")
);
CREATE TABLE IF NOT EXISTS "dish" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT NOT NULL,
	"description"	TEXT,
	"price"	REAL NOT NULL,
	"quantity"	INTEGER NOT NULL,
	"created_at"	TEXT,
	"updated_at"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "order_dish" (
	"id"	INTEGER NOT NULL UNIQUE,
	"order_id"	INTEGER NOT NULL,
	"dish_id"	INTEGER NOT NULL,
	"quantity"	INTEGER NOT NULL,
	"price"	REAL NOT NULL,
	FOREIGN KEY("order_id") REFERENCES "dish"("id"),
	FOREIGN KEY("dish_id") REFERENCES "dish"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
