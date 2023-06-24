package structs

type InstitutionDocument struct {
	ID            int      `json:"id"`
	QSScore       float32  `json:"qs_score"`
	TimesScore    float32  `json:"times_score"`
	Name          string   `json:"name"`
	LowerCaseName string   `json:"lowercase_name"`
	Country       string   `json:"country"`
	CountryCode   string   `json:"country_code"`
	Subjects      []string `json:"subjects"`
}
