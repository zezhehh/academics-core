package structs

type Institution struct {
	ID            int     `json:"id"`
	QSScore       float32 `json:"qs_score"`
	TimesScore    float32 `json:"times_score"`
	Name          string  `json:"name"`
	LowerCaseName string  `json:"lower_case_name"`
	CountryCode   string  `json:"country_code"`
	Website       string  `json:"website"`
	Hidden        bool    `json:"hidden"`
}

type Subject struct {
	ID   int    `json:"id"`
	Name string `json:"name"`
}

type SubjectOffered struct {
	ID            int `json:"id"`
	InstitutionID int `json:"institution_id"`
	SubjectID     int `json:"subject_id"`
}
