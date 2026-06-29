FROM node:20-alpine
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json* ./frontend/
WORKDIR /app/frontend
RUN npm install || true
COPY frontend /app/frontend
EXPOSE 3000
CMD ["npm", "run", "dev"]
