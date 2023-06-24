package main

import (
	"context"
	"log"
	"os"

	"database/sql"

	"github.com/georgysavva/scany/v2/sqlscan"
	"github.com/joho/godotenv"

	"github.com/meilisearch/meilisearch-go"
	"github.com/zezhehh/academics-core/meilisearch-postgres-sync/structs"

	_ "github.com/lib/pq"
)

func main() {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
		os.Exit(1)
	}
	meiliHOST := os.Getenv("MEILI_HOST")
	meiliSearchKey := os.Getenv("MEILI_SEARCH_KEY")
	client := meilisearch.NewClient(meilisearch.ClientConfig{
		Host:   meiliHOST,
		APIKey: meiliSearchKey,
	})

	client.Index("institutions").DeleteAllDocuments()

	connStr := os.Getenv("POSTGRES_URL")
	db, err := sql.Open("postgres", connStr)
	if err != nil {
		log.Fatal("Failed to connect postgres")
		os.Exit(1)
	}
	ctx := context.Background()
	var institutions []*structs.Institution
	err = sqlscan.Select(ctx, db, &institutions, "SELECT * FROM institutions")
	if err != nil {
		log.Fatal("Failed to select institutions")
		os.Exit(1)
	}

	var documents []structs.InstitutionDocument

	query := `
		SELECT s.name as name, s.id as id
		FROM institutions AS i
		JOIN subject_offered AS so ON i.id = so.institution_id
		JOIN subjects AS s ON so.subject_id = s.id
		WHERE i.id = $1
		`
	for _, institution := range institutions {
		log.Println("Adding", institution.Name)
		var subjects []*structs.Subject

		err = sqlscan.Select(ctx, db, &subjects, query, institution.ID)
		if err != nil {
			log.Fatal("Failed to select subjects")
			os.Exit(1)
		}

		document := structs.ConvertToDocument(institution, subjects)
		documents = append(documents, document)
	}

	_, err = client.Index("institutions").AddDocuments(documents)
	if err != nil {
		log.Fatal("Failed to add documents to meilisearch")
		os.Exit(1)
	}
	log.Println("Successfully added documents to meilisearch")
}
