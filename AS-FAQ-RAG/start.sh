#!/bin/bash

# 預設不啟用自動更新
ENABLE_AUTO_UPDATE=0
PORT=8000

# 檢查參數
for arg in "$@"
  do
    if [ "$arg" = "--auto-update" ]; then
      ENABLE_AUTO_UPDATE=1
    fi
    if [[ $arg == --port=* ]]; then
      PORT="${arg#--port=}"
    fi
  done

# 若未指定參數，則檢查環境變數
if [ "$ENABLE_AUTO_UPDATE" = "0" ] && [ "$ENABLE_AUTO_UPDATE_ENV" = "1" ]; then
  ENABLE_AUTO_UPDATE=1
fi

if [ "$ENABLE_AUTO_UPDATE" = "1" ]; then
  echo "自動更新已啟用"
  python auto_update.py &
else
  echo "自動更新未啟用"
fi

# 啟動 API 服務在前台運行
## dev
# exec uvicorn api:app --reload --reload-exclude ".venv" --reload-exclude ".git" --host 0.0.0.0 --port $PORT
## prod
exec uvicorn api:app --host 0.0.0.0 --port $PORT
