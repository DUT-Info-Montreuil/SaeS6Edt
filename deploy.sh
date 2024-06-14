#!/bin/bash

# Iterate through all directories in the current directory
for dir in */; do
    dir=${dir%*/}  # Remove the trailing slash from the directory name
    cd "$dir" || continue  # Move to the next directory if the change fails

    # Check if the deploy.sh file exists
    if [ -f "deploy.sh" ]; then
        echo "Executing deploy.sh in directory: $dir"
        if [[ "$OS" == "Windows_NT" ]]; then
            ./deploy.sh  # Execute deploy.sh sous Windows
        else
            bash deploy.sh  # Execute deploy.sh sous Linux
        fi
    else
        echo "No deploy.sh file in directory: $dir"
    fi

    cd ..  # Return to the parent directory
done

# Deploy the database and phpMyAdmin
# docker-compose up -d --build db phpmyadmin

# docker-compose down courroux-sapp courroux-sme


# Check if the 'db' container is running
# if [ "$(docker ps -q -f name=courroux_db)" ]; then
#     echo "The 'db' container is already running."
# else
#     echo "Starting the 'db' container..."
#     docker-compose up -d --build db
# fi
# docker-compose up -d --build db


# ./wait-for-it.sh -t 0 -q localhost:8083
# # Wait for 5 seconds (adjust the sleep duration as needed)
# sleep 5

docker-compose up -d --build

# Deploy the back-end
sleep 10
docker-compose up -d --build courroux-sme

