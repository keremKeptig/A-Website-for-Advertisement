import sqlite3


def createDatabase(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE User(
            username TEXT PRIMARY KEY,
            fullname TEXT,
            email TEXT,
            password TEXT,
            telno INTEGER
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS Category(
            cid INTEGER PRIMARY KEY,
            cname TEXT
        )

    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS Advertisement(
            aid INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            isactive INTEGER, 
            username TEXT,
            cid INTEGER,
            FOREIGN KEY(username) REFERENCES User(username),
            FOREIGN KEY(cid) REFERENCES Category(cid)
        )
    """)

    conn.commit()
    conn.close()


def insertRecords(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    categories = [(1, "Clothes"), (2, "Technology"), (3, "Cars"), (4, "Food"), (5, "Drink")]
    c.executemany("INSERT INTO Category VALUES(?, ?)", categories)


    conn.commit()
    conn.close()


if __name__ == "__main__":
    conn = sqlite3.connect("shop.db")
    c = conn.cursor()

    createDatabase("shop.db")
    insertRecords("shop.db")