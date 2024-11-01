# Dockerfile

# Use the official Redis base image
FROM redis:latest

# Copy the custom redis.conf to the container
COPY redis.conf /usr/local/etc/redis/redis.conf

# Expose Redis port
EXPOSE 6379

# Define the default command to run Redis with the custom configuration
CMD ["redis-server", "/usr/local/etc/redis/redis.conf"]