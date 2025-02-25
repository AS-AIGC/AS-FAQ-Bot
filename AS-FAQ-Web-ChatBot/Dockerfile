# 使用官方 Node.js 映像檔作為基礎映像檔
FROM node:20-alpine

# 設定工作目錄
WORKDIR /app

# 複製 package.json 和 package-lock.json
COPY package*.json ./

# 安裝專案依賴
RUN npm install

# 複製專案檔案到工作目錄
COPY . .

# 編譯 Tailwind CSS
RUN npx tailwindcss -i ./src/css/tailwind-input.css -o ./src/css/tailwind-output.css --minify -c tailwind.config.js

# 暴露應用程式埠號
EXPOSE 3000

# 啟動應用程式
ENTRYPOINT ["node", "server.js"]