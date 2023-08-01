# Use the Nginx image from the Docker Hub
FROM nginx:latest

# Remove the default Nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Copy the configuration file from the local directory (i.e., .) to the image
COPY nginx.conf /etc/nginx/conf.d
