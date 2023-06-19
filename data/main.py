import typer
import csv
from raw import COUNTRY_NAMES2CODES, FieldName, MAPPING
from rich.progress import track
from rich import print
from db import DB
from models import Institution

app = typer.Typer(add_completion=False)


@app.command()
def extract():
    """
    Extract data from /raw folder.
    """
    db = DB()
    files = MAPPING.keys()
    for fn in files:
        if ".csv" not in fn:
            print("Only support csv files")
            continue
        mapping = MAPPING[fn]

        with open(f"./raw/{fn}", "r") as f:
            reader = csv.DictReader(f)
            for row in track(reader, description=f"Reading {fn}..."):
                subjects = row.get(mapping[FieldName.SUBJECTS], [])
                if subjects != []:
                    subjects = [s.strip() for s in subjects.split(",")]
                    subjects = db.create_subjects(subjects)
                country_code = row.get(mapping[FieldName.COUNTRY_CODE], None)
                if country_code is None:
                    country_code = COUNTRY_NAMES2CODES[row[mapping[FieldName.COUNTRY]]]
                qs_score = row.get(mapping[FieldName.QS_SCORE], 0)
                if qs_score == "-":
                    qs_score = 0
                times_score = row.get(mapping[FieldName.TIMES_SCORE], 0)
                if type(times_score) == str and "–" in times_score:
                    scores = times_score.split("–")
                    times_score = (float(scores[0]) + float(scores[1])) / 2
                elif type(times_score) == str and times_score == "":
                    times_score = 0
                institution_name = row[mapping[FieldName.INSTITUTION_NAME]].strip()
                lower_case_name = institution_name.lower()
                institution = Institution(
                    name=institution_name,
                    lower_case_name=lower_case_name,
                    country_code=country_code.strip(),
                    qs_score=qs_score,
                    times_score=times_score,
                    website="",
                )
                institution = db.create_or_update_institution(institution)

                db.create_subject_offered(institution, subjects)


if __name__ == "__main__":
    app()
