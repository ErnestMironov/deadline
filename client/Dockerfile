FROM node:20-alpine AS builder

WORKDIR /app

ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL

COPY package.json yarn.lock ./
RUN yarn config set network-timeout 600000 && \
    yarn install --frozen-lockfile --network-timeout 600000 || \
    (yarn cache clean && yarn install --frozen-lockfile --network-timeout 600000)

COPY . .
RUN yarn build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]
