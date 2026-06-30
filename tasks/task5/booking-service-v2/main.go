package main

import (
	"fmt"
	"log"
	"net/http"
)

func main() {
	http.HandleFunc("/ping", func(w http.ResponseWriter, r *http.Request) {
		if r.Header.Get("X-Feature-Enabled") == "true" {
			fmt.Fprintf(w, "pong-v2-feature\n")
		} else {
			fmt.Fprintf(w, "pong-v2\n")
		}
	})

	log.Println("Server running on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
