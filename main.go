package main

import (
	"encoding/json"
	"log"
	"net/http"
	"os"
)

type Ping struct {
	Status int    `json:"status"`
	Result string `json:"result"`
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
	http.HandleFunc("/", rootHandler)
	httpServer.Addr = ":" + port

	log.Fatalln(httpServer.ListenAndServe())
}
