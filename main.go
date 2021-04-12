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

type Ping struct {
	Status int    `json:"status"`
	Result string `json:"result"`
}

func dbHandler(db *sql.DB) func(http.ResponseWriter, *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
		w.Header().Set("Content-Type", "application/json")

		if _, err := db.Exec("CREATE TABLE IF NOT EXISTS ticks (tick timestamp)"); err != nil {
			s := fmt.Sprintf("Error creating database table: %q", err)
			res, _ := json.Marshal(Ping{http.StatusInternalServerError, s})
			w.Write(res)
			return
		}

		if _, err := db.Exec("INSERT INTO ticks VALUES (now())"); err != nil {
			s := fmt.Sprintf("Error inserting: %q", err)
			res, _ := json.Marshal(Ping{http.StatusInternalServerError, s})
			w.Write(res)
			return
		}

		rows, err := db.Query("SELECT tick FROM ticks ORDER BY tick DESC LIMIT 1")
		if err != nil {
			s := fmt.Sprintf("Error reading: %q", err)
			res, _ := json.Marshal(Ping{http.StatusInternalServerError, s})
			w.Write(res)
			return
		}
		defer rows.Close()

		for rows.Next() {
			var tick time.Time
			if err := rows.Scan(&tick); err != nil {
				s := fmt.Sprintf("Error scanning: %q", err)
				res, _ := json.Marshal(Ping{http.StatusInternalServerError, s})
				w.Write(res)
				return
			}
			ping := Ping{http.StatusOK, tick.String()}
			res, _ := json.Marshal(ping)
			w.Write(res)
			return
		}
	}
}

func rootHandler(w http.ResponseWriter, r *http.Request) {
	ping := Ping{http.StatusOK, "ok"}
	res, _ := json.Marshal(ping)

	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.Header().Set("Content-Type", "application/json")
	w.Write(res)
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
