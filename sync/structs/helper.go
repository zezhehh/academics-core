package structs

func ConvertToDocument(institution *Institution, subjects []*Subject) InstitutionDocument {
	var subjectNames []string
	for _, subject := range subjects {
		subjectNames = append(subjectNames, subject.Name)
	}
	return InstitutionDocument{
		ID:            institution.ID,
		QSScore:       institution.QSScore,
		TimesScore:    institution.TimesScore,
		Name:          institution.Name,
		LowerCaseName: institution.LowerCaseName,
		Country:       Contries[institution.CountryCode],
		CountryCode:   institution.CountryCode,
		Subjects:      subjectNames,
	}
}
