FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5173

# Using dev server for this setup as requested
CMD ["npm", "run", "dev", "--", "--host"]
