from models import Institution, Subject
import psycopg2
import os

print(os.getenv("DB_PWD"), os.getenv("DB_USER"))


class DB:
    def __init__(self):
        self.conn = psycopg2.connect(
            database="academics",
            host="localhost",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PWD"),
        )
        self.cursor = self.conn.cursor()
        self.drop_all()
        self.create_tables()

    def __del__(self):
        self.conn.close()

    def drop_all(self):
        self.cursor.execute("DROP TABLE IF EXISTS institutions")
        self.cursor.execute("DROP TABLE IF EXISTS subjects")
        self.cursor.execute("DROP TABLE IF EXISTS subject_offered")
        self.conn.commit()

    def create_tables(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS subjects (
                id SERIAL PRIMARY KEY, 
                name TEXT UNIQUE
            )"""
        )
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS institutions (
                id SERIAL PRIMARY KEY, 
                qs_score REAL, 
                times_score REAL, 
                name TEXT UNIQUE,
                lower_case_name TEXT UNIQUE,
                country_code TEXT,
                website TEXT
            )"""
        )
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS subject_offered (
                id SERIAL PRIMARY KEY, 
                institution_id INTEGER, 
                subject_id INTEGER,
                UNIQUE(institution_id, subject_id)
            )"""
        )
        self.conn.commit()

    def __find_subject(self, name: str) -> Subject:
        self.cursor.execute(
            """SELECT * FROM subjects WHERE name = %s""",
            (name,),
        )
        subject = self.cursor.fetchone()
        return Subject(id=subject[0], name=subject[1])

    def create_subjects(self, subjects: list[str]) -> list[Subject]:
        self.cursor.executemany(
            """INSERT INTO subjects (name) VALUES (%s) ON CONFLICT (name) DO NOTHING""",
            [(subject,) for subject in subjects],
        )
        self.conn.commit()
        return [self.__find_subject(subject) for subject in subjects]

    def __update_institution(self, institution: Institution) -> Institution:
        if institution.qs_score != 0:
            self.cursor.execute(
                """UPDATE institutions SET qs_score = %s
                WHERE id = %s""",
                (institution.qs_score, institution.id),
            )
        if institution.times_score != 0:
            self.cursor.execute(
                """UPDATE institutions SET times_score = %s
                WHERE id = %s""",
                (institution.times_score, institution.id),
            )
        self.conn.commit()
        self.cursor.execute(
            """SELECT * FROM institutions WHERE id = %s""",
            (institution.id,),
        )
        institution = self.cursor.fetchone()
        institution = Institution(
            id=institution[0],
            qs_score=institution[1],
            times_score=institution[2],
            name=institution[3],
            lower_case_name=institution[4],
            country_code=institution[5],
            website=institution[6],
        )
        return institution

    def create_or_update_institution(self, institution: Institution):
        self.cursor.execute(
            """SELECT * FROM institutions WHERE lower_case_name = %s""",
            (institution.lower_case_name,),
        )

        institution_found = self.cursor.fetchone()
        if institution_found:
            institution.id = institution_found[0]
            return self.__update_institution(institution)
        self.cursor.execute(
            """INSERT INTO institutions 
            (qs_score, times_score, name, lower_case_name, country_code, website)
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (
                institution.qs_score,
                institution.times_score,
                institution.name,
                institution.lower_case_name,
                institution.country_code,
                institution.website,
            ),
        )
        self.conn.commit()
        institution.id = self.cursor.lastrowid
        return institution

    def create_subject_offered(self, institution: Institution, subjects: list[Subject]):
        self.cursor.executemany(
            """INSERT INTO subject_offered (institution_id, subject_id) 
            VALUES (%s, %s) ON CONFLICT (institution_id, subject_id) DO NOTHING""",
            [(institution.id, subject.id) for subject in subjects],
        )
        self.conn.commit()
