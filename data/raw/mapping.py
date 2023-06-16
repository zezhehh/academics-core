# Map columns to data fields in each data file.
from enum import IntEnum


class FieldName(IntEnum):
    INSTITUTION_NAME = 0
    COUNTRY_CODE = 1
    QS_SCORE = 2
    TIMES_SCORE = 3
    COUNTRY = 4
    SUBJECTS = 5


MAPPING = {
    "QS_2023.csv": {
        FieldName.INSTITUTION_NAME: "institution",
        FieldName.COUNTRY_CODE: "country_code",
        FieldName.COUNTRY: "country",
        FieldName.QS_SCORE: "score_scaled",
        FieldName.TIMES_SCORE: "dummy",
        FieldName.SUBJECTS: "dummy",
    },
    "Times_2023.csv": {
        FieldName.INSTITUTION_NAME: "name",
        FieldName.COUNTRY_CODE: "dummy",
        FieldName.COUNTRY: "location",
        FieldName.QS_SCORE: "dummy",
        FieldName.TIMES_SCORE: "scores_overall",
        FieldName.SUBJECTS: "subjects_offered",
    },
}
