FROM node:alpine3.14
WORKDIR '/frontend'

COPY package.json .
RUN npm install
COPY . .
RUN npm run build
CMD ["npm", "start"]