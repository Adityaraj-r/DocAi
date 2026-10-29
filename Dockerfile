FROM node:22-alpine AS build

WORKDIR /app

# Build context must be the repository root: this is an npm workspace.
COPY package*.json ./
COPY packages/shared/package*.json ./packages/shared/
COPY apps/backend/package*.json ./apps/backend/
RUN npm ci

COPY packages/shared ./packages/shared
COPY apps/backend ./apps/backend
RUN npm run build:shared \
    && npm run build:backend \
    && npm prune --omit=dev

FROM node:22-alpine AS runner

WORKDIR /app
ENV NODE_ENV=production
ENV PORT=10000

COPY --from=build --chown=node:node /app/package*.json ./
COPY --from=build --chown=node:node /app/node_modules ./node_modules
COPY --from=build --chown=node:node /app/packages/shared/package.json ./packages/shared/package.json
COPY --from=build --chown=node:node /app/packages/shared/dist ./packages/shared/dist
COPY --from=build --chown=node:node /app/apps/backend/package.json ./apps/backend/package.json
COPY --from=build --chown=node:node /app/apps/backend/dist ./apps/backend/dist
RUN mkdir -p /app/apps/backend/uploads && chown node:node /app/apps/backend/uploads

WORKDIR /app/apps/backend
USER node

EXPOSE 10000
CMD ["node", "dist/app.js"]
