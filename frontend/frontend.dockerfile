# Use an official Node.js LTS (Long Term Support) image as the base
FROM node:lts-alpine as build
WORKDIR /app
# Cache and Install dependencies
COPY ./app/package.json ./app/package-lock.json ./
RUN npm ci
# Copy app files
COPY ./app .
# Build the app
RUN npm run build

# Bundle static assets with nginx
FROM nginx:1.23.0-alpine
# Copy built assets from builder
COPY --from=build /app/build /usr/share/nginx/html
# Add your nginx.conf
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
# Expose port
EXPOSE 80
# Start nginx
CMD ["nginx", "-g", "daemon off;"]