FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm install

# Copy source and build for production
COPY . .
RUN npm run build

# Simple static file server for the built Vite app
RUN npm install -g serve

ENV PORT=4173

CMD ["sh", "-c", "serve -s dist -l 0.0.0.0:${PORT}"]
