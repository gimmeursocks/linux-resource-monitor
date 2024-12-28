#!/bin/bash

# Stop and remove running container if it exists
docker stop resource-monitor 2>/dev/null || true
docker rm resource-monitor 2>/dev/null || true

# Install Docker if not already installed
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    sudo apt-get update
    sudo apt-get install -y docker.io
    sudo systemctl start docker
    sudo systemctl enable docker
fi

# Build and run the container
echo "Building Docker image..."
docker build -t resource-monitor .

echo "Starting container..."
docker run -d -p 5000:5000 --name resource-monitor resource-monitor

echo "Waiting for application to start..."
sleep 3

echo "Checking container status..."
docker ps | grep resource-monitor
docker logs resource-monitor

echo "Testing endpoint..."
curl http://localhost:5000/metrics

echo "Deployment complete! Access metrics at: http://localhost:5000/metrics"