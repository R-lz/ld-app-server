# 构建阶段
FROM node:18-alpine AS builder

WORKDIR /app

# 添加构建参数
ARG NODE_ENV=production
ENV NODE_ENV=${NODE_ENV}

# 清理 npm 缓存
RUN npm cache clean --force

# 安装依赖（包括开发依赖）
COPY package*.json ./
RUN npm install --include=dev

# 复制源代码和配置文件
COPY . .

RUN test -f tailwind.config.js || echo "module.exports = {content: ['./src/**/*.{vue,js}'],theme: {extend: {}},plugins: [],}" > tailwind.config.js
RUN test -f postcss.config.js || echo "module.exports = {plugins: {tailwindcss: {},autoprefixer: {},},}" > postcss.config.js

# 强制重新构建
RUN rm -rf dist || true
RUN npm run build

# 生产阶段
FROM nginx:alpine

# 复制构建文件
COPY --from=builder /app/dist /usr/share/nginx/html

# 复制 nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 添加健康检查
HEALTHCHECK --interval=30s --timeout=3s \
    CMD wget --quiet --tries=1 --spider http://localhost:80/ || exit 1

EXPOSE 80 