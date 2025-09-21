# Stage 1: Build the Angular application
FROM node:20-alpine as builder
WORKDIR /app

# Copy only package files to leverage Docker cache for npm install
COPY package.json package-lock.json ./

# Use npm cache mount for faster installs (requires BuildKit enabled)
RUN --mount=type=cache,target=/root/.npm npm install

# Copy the rest of the source code
COPY . .

# Build the Angular app
RUN npm run build


# Stage 2: Serve the application with Nginx on port 8080
FROM nginx:stable-alpine

# Copy Angular build output to Nginx html folder
COPY --from=builder /app/dist/agent_framework_web/browser /usr/share/nginx/html

# Use custom nginx config listening on port 8080
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Run Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
