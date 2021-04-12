package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	_ "github.com/lib/pq"
)

type Record struct {
	Id        int    `json:"id,omitempty"`
	Referrer  string `json:"referrer,omitempty"`
	Url       string `json:"url,omitempty"`
	CreatedAt string `json:"created_at,omitempty"`
}

type Ping struct {
	Status int    `json:"status"`
	Rec    Record `json:"record,omitempty"`
	Err    string `json:"error"`
}

func dbHandler(db *sql.DB) func(http.ResponseWriter, *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
		w.Header().Set("Content-Type", "application/json")

		if _, err := db.Exec(`
			CREATE TABLE
				IF NOT EXISTS links (
					id serial PRIMARY KEY
					, referrer text
					, url text
					, created_at timestamp default CURRENT_TIMESTAMP
				)
		`); err != nil {
			s := fmt.Sprintf("Error creating database table: %q", err)
			res, _ := json.Marshal(Ping{http.StatusInternalServerError, Record{}, s})
			w.Write(res)
			return
		}

		v := r.URL.Query()
		if v == nil {
			res, _ := json.Marshal(Ping{http.StatusBadRequest, Record{}, ""})
			w.Write(res)
			return
		}

		url := r.URL.Query().Get("url")
		referrer := r.Referer()
		if url == "" {
			res, _ := json.Marshal(Ping{http.StatusBadRequest, Record{}, ""})
			w.Write(res)
		}

		if _, err := db.Exec(`
			INSERT INTO links
			(referrer, url) VALUES (
				$1
				, $2
			)
		`, referrer, url); err != nil {
			s := fmt.Sprintf("Error inserting: %q", err)
			res, _ := json.Marshal(Ping{http.StatusInternalServerError, Record{}, s})
			w.Write(res)
			return
		}

		rows, err := db.Query("SELECT id, referrer, url, created_at FROM links ORDER BY created_at DESC LIMIT 1")
		if err != nil {
			s := fmt.Sprintf("Error reading: %q", err)
			res, _ := json.Marshal(Ping{http.StatusInternalServerError, Record{}, s})
			w.Write(res)
			return
		}
		defer rows.Close()

		for rows.Next() {
			var id int
			var t time.Time
			var url string
			var ref string
			if err := rows.Scan(&id, &ref, &url, &t); err != nil {
				s := fmt.Sprintf("Error scanning: %q", err)
				res, _ := json.Marshal(Ping{http.StatusInternalServerError, Record{}, s})
				w.Write(res)
				return
			}
			ping := Ping{http.StatusOK, Record{id, url, ref, t.String()}, ""}
			res, _ := json.Marshal(ping)
			w.Write(res)
			return
		}
	}
}

func main() {
	var httpServer http.Server
	port := os.Getenv("PORT")

	db, err := sql.Open("postgres", os.Getenv("DATABASE_URL"))
	if err != nil {
		log.Fatalf("Error opening database: %q", err)
	}

	http.HandleFunc("/", dbHandler(db))
	httpServer.Addr = ":" + port

	log.Fatalln(httpServer.ListenAndServe())
}
