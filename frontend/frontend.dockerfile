# Use an official Node.js LTS (Long Term Support) image as the base
FROM node:lts-alpine

# Set the working directory inside the container
WORKDIR /app/

# Copy package.json and package-lock.json to the working directory
COPY ./app/package*.json ./

# Install dependencies
RUN npm install

# Copy the entire React app to the working directory
COPY ./app .

#Your app binds to port 3000 so you’ll use the EXPOSE instruction to have it mapped by the docker daemon:
EXPOSE 3000
CMD ["npm", "start"]