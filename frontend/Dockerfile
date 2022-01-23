FROM node:16-alpine
WORKDIR '/frontend'

COPY package.json .
RUN npm install
COPY . .
#ENV NODE_OPTIONS=--openssl-legacy-provider
RUN npm run build
CMD ["npm", "start"]