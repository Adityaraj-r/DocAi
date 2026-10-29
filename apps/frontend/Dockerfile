FROM node:22-alpine AS build

WORKDIR /app
ARG NEXT_PUBLIC_API_URL=http://localhost:5000/api/v1
ENV NEXT_PUBLIC_API_URL=${NEXT_PUBLIC_API_URL}

COPY package*.json ./
COPY packages/shared/package*.json ./packages/shared/
COPY apps/backend/package*.json ./apps/backend/
COPY apps/frontend/package*.json ./apps/frontend/
RUN npm ci

COPY packages/shared ./packages/shared
COPY apps/backend/package.json ./apps/backend/package.json
COPY apps/frontend ./apps/frontend
RUN npm run build:shared \
    && npm run build:frontend \
    && npm prune --omit=dev

FROM node:22-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV PORT=3000
ENV HOSTNAME=0.0.0.0

COPY --from=build --chown=node:node /app/package*.json ./
COPY --from=build --chown=node:node /app/node_modules ./node_modules
COPY --from=build --chown=node:node /app/packages/shared/package.json ./packages/shared/package.json
COPY --from=build --chown=node:node /app/packages/shared/dist ./packages/shared/dist
COPY --from=build --chown=node:node /app/apps/frontend/package.json ./apps/frontend/package.json
COPY --from=build --chown=node:node /app/apps/frontend/.next ./apps/frontend/.next
COPY --from=build --chown=node:node /app/apps/frontend/public ./apps/frontend/public
COPY --from=build --chown=node:node /app/apps/frontend/next.config.mjs ./apps/frontend/next.config.mjs

WORKDIR /app/apps/frontend
USER node
EXPOSE 3000
CMD ["../../node_modules/.bin/next", "start"]
