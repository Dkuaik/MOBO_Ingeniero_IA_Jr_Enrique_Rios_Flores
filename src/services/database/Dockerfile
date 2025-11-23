# Use official MongoDB image as base
FROM mongo:7.0

# Set environment variables for MongoDB initialization
ENV MONGO_INITDB_ROOT_USERNAME=admin
ENV MONGO_INITDB_ROOT_PASSWORD=password123
ENV MONGO_INITDB_DATABASE=ai_api_db

# Expose MongoDB port
EXPOSE 27017

# Default command to run MongoDB
CMD ["mongod"]