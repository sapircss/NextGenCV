FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Expose port 3000
EXPOSE 3000

# Set environment to development for hot reload
ENV NODE_ENV=development

# Start the React development server
CMD ["npm", "start"]