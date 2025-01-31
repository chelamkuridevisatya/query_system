# Use the official Nginx base image
FROM nginx:latest

# Remove the default Nginx configuration file
RUN rm /etc/nginx/nginx.conf

# Copy your custom Nginx configuration
COPY ./nginx.config /etc/nginx/nginx.config

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
