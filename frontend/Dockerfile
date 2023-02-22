FROM node:16-alpine
WORKDIR '/frontend'

COPY package.json .
RUN npm install
COPY . .
ARG REACT_APP_API_URL
RUN echo $REACT_APP_API_URL
ENV REACT_APP_API_URL=$REACT_APP_API_URL
#ENV NODE_OPTIONS=--openssl-legacy-provider
RUN npm run build
CMD ["npm", "start"]