# Frontend Dockerfile (frontend/Dockerfile)

FROM node:18-alpine as frontend-build

WORKDIR /app

# Install dependencies
COPY ./angular_query_system/package.json ./angular_query_system/package-lock.json ./
RUN npm install

# Copy the rest of the frontend code
COPY ./angular_query_system /app/

# Build the Angular app for production
RUN npm run build --prod

# Use Nginx to serve the built app
FROM nginx:latest
<<<<<<< HEAD
COPY --from=build /app/dist/angular_query_system /usr/share/nginx/html
# COPY ../nginx/ngnix.config /etc/nginx/conf.d/default.conf

=======
>>>>>>> 9f0c5f7 (updated)

# Copy the build output to the Nginx directory
COPY --from=frontend-build /app/dist/angular_query_system /usr/share/nginx/html

# Expose the port for Nginx
EXPOSE 80
