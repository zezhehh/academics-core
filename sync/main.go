package main

import (
	"context"
	"encoding/json"
	"log"
	"os"

	"database/sql"
	"sync"

	"golang.org/x/sync/semaphore"

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
	}
	meiliHOST := os.Getenv("MEILI_HOST")
	meiliSearchKey := os.Getenv("MEILI_MASTER_KEY")
	client := meilisearch.NewClient(meilisearch.ClientConfig{
		Host:   meiliHOST,
		APIKey: meiliSearchKey,
	})

	_, err = client.Index("institutions").DeleteAllDocuments()
	if err != nil {
		log.Fatal("Failed to delete all documents")
	}

	connStr := os.Getenv("POSTGRES_URL")
	db, err := sql.Open("postgres", connStr)
	if err != nil {
		log.Fatal("Failed to connect postgres")
	}
	ctx := context.Background()
	var institutions []*structs.Institution
	err = sqlscan.Select(ctx, db, &institutions, "SELECT * FROM institutions")
	if err != nil {
		log.Fatalf("Failed to select institutions: %v", err)
	}

	var (
		wg        sync.WaitGroup
		sem       = semaphore.NewWeighted(10)
		documents []structs.InstitutionDocument
	)

	ch := make(chan structs.InstitutionDocument, 10)
	go func() {
		for document := range ch {
			documents = append(documents, document)
			log.Println("Added", document.Name)
		}
	}()

	query := `
	SELECT s.name as name, s.id as id
	FROM institutions AS i
	JOIN subject_offered AS so ON i.id = so.institution_id
	JOIN subjects AS s ON so.subject_id = s.id
	WHERE i.id = $1
	`
	for _, institution := range institutions {
		if err := sem.Acquire(ctx, 1); err != nil {
			log.Printf("Failed to acquire semaphore: %v", err)
			break
		}
		wg.Add(1)

		go func(i structs.Institution) {
			defer sem.Release(1)
			defer wg.Done()
			log.Println("Adding", i.Name)
			var subjects []*structs.Subject

			err = sqlscan.Select(ctx, db, &subjects, query, i.ID)
			if err != nil {
				log.Fatalf("Failed to select subjects: %v", err)
			}
			document := structs.ConvertToDocument(i, subjects)
			ch <- document
		}(*institution)

	}

	wg.Wait()
	close(ch)

	jsonBytes, err := json.Marshal(documents)
	if err != nil {
		log.Fatalf("Failed to marshal documents: %v", err)
	}

	f, err := os.Create("institutions.json")
	defer f.Close()
	if err != nil {
		log.Fatalf("Failed to create file: %v", err)
	}
	f.Write(jsonBytes)

	_, err = client.Index("institutions").AddDocuments(documents)
	if err != nil {
		log.Fatalf("Failed to add documents to meilisearch: %v", err)
	}
	log.Println("Successfully added documents to meilisearch")
}
