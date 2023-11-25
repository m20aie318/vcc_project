#!/bin/bash

for ((i=1; i<=1000; i++)); do
  # Generate random title, dynamic content, and context
  title="Note Title $i"
  content=$(LC_ALL=C tr -dc 'a-zA-Z0-9' </dev/urandom | head -c 100)
  context="Context for Note $i. This could be additional information or details related to the note."

  # Send POST request using curl
  curl -X POST -H "Content-Type: application/json" -d '{
    "title": "'"$title"'",
    "content": "'"$content"'"
  }' http://localhost:5001/notes

  # Add a delay between requests (adjust as needed)
  sleep 0.1
done