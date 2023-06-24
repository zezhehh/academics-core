package structs

type Institution struct {
	ID            int
	QSScore       float32
	TimesScore    float32
	Name          string
	LowerCaseName string
	CountryCode   string
	Website       string
	Hidden        bool
}

type Subject struct {
	ID   int
	Name string
}

type SubjectOffered struct {
	ID            int
	InstitutionID int
	SubjectID     int
}
