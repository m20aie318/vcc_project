#!/bin/bash

# Build Docker images for frontend, notes, and MongoDB services

# Function to build an image
build_image() {
  service_name=$1
  service_path=$2

  echo "Building image for $service_name..."
  docker build -t $service_name -f $service_path/Dockerfile $service_path
}

# Build images for each service
build_image "frontend-service:snapshot1" "./frontend-service"
build_image "notes-service:snapshot1" "./notes-service"
build_image "ml-ops:snapshot1" "./ml-ops"