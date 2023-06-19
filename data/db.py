import sqlite3
from models import Institution, Subject


class DB:
    def __init__(self):
        self.conn = sqlite3.connect("academics.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def __del__(self):
        self.conn.close()

    def create_tables(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY, 
                name TEXT UNIQUE
            )"""
        )
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS institutions (
                id INTEGER PRIMARY KEY, 
                qs_score REAL, 
                times_score REAL, 
                name TEXT UNIQUE, 
                country_code TEXT,
                website TEXT
            )"""
        )
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS subject_offered (
                id INTEGER PRIMARY KEY, 
                institution_id INTEGER, 
                subject_id INTEGER,
                UNIQUE(institution_id, subject_id)
            )"""
        )
        self.conn.commit()

    def __find_subject(self, name: str) -> Subject:
        self.cursor.execute(
            """SELECT * FROM subjects WHERE name = ?""",
            (name,),
        )
        subject = self.cursor.fetchone()
        return Subject(id=subject[0], name=subject[1])

    def create_subjects(self, subjects: list[str]) -> list[Subject]:
        self.cursor.executemany(
            """INSERT OR IGNORE INTO subjects (name) VALUES (?)""",
            [(subject,) for subject in subjects],
        )
        self.conn.commit()
        return [self.__find_subject(subject) for subject in subjects]

    def __update_institution(self, institution: Institution) -> Institution:
        if institution.qs_score != 0:
            self.cursor.execute(
                """UPDATE institutions SET qs_score = ?
                WHERE id = ?""",
                (institution.qs_score, institution.id),
            )
        if institution.times_score != 0:
            self.cursor.execute(
                """UPDATE institutions SET times_score = ?
                WHERE id = ?""",
                (institution.times_score, institution.id),
            )
        self.conn.commit()
        self.cursor.execute(
            """SELECT * FROM institutions WHERE id = ?""",
            (institution.id,),
        )
        institution = self.cursor.fetchone()
        institution = Institution(
            id=institution[0],
            qs_score=institution[1],
            times_score=institution[2],
            name=institution[3],
            country_code=institution[4],
            website=institution[5],
        )
        return institution

    def create_or_update_institution(self, institution: Institution):
        self.cursor.execute(
            """SELECT * FROM institutions WHERE name = ?""",
            (institution.name,),
        )

        institution_found = self.cursor.fetchone()
        if institution_found:
            institution.id = institution_found[0]
            return self.__update_institution(institution)
        self.cursor.execute(
            """INSERT INTO institutions 
            (qs_score, times_score, name, country_code, website)
            VALUES (?, ?, ?, ?, ?)""",
            (
                institution.qs_score,
                institution.times_score,
                institution.name,
                institution.country_code,
                institution.website,
            ),
        )
        self.conn.commit()
        institution.id = self.cursor.lastrowid
        return institution

    def create_subject_offered(self, institution: Institution, subjects: list[Subject]):
        self.cursor.executemany(
            """INSERT OR IGNORE INTO subject_offered (institution_id, subject_id) 
            VALUES (?, ?)""",
            [(institution.id, subject.id) for subject in subjects],
        )
        self.conn.commit()
