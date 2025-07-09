import os
import pandas as pd
import logging
import subprocess

# 設定資料來源目錄與輸出檔案名稱
DATA_DIR = os.path.abspath('./FAQ_data')
OUTPUT_FILE = os.path.abspath('./combined_context_en.csv')

# 設定 logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 下載github repo
def download_github_repo():
    # 從 github 下載原始資料
    repo_url = os.getenv("REPO_URL")

    if not os.path.exists(DATA_DIR):
        # 如果資料夾不存在，則建立資料夾
        os.makedirs(DATA_DIR)
        logging.info(f"Created directory: {DATA_DIR}")
        
    if not os.listdir(DATA_DIR):
        # 如果資料夾為空，則 clone repo
        logging.info(f"Folder {DATA_DIR} is empty, cloning repository")
        subprocess.run(['git', 'clone', repo_url, DATA_DIR], check=True)
    elif not os.path.exists(os.path.join(DATA_DIR, '.git')):
        # 檢查是否為 git repo，如果不是，則重新 clone
        logging.info(f"Folder {DATA_DIR} is not a git repository, re-cloning")
        import shutil
        shutil.rmtree(DATA_DIR)
        os.makedirs(DATA_DIR)
        subprocess.run(['git', 'clone', repo_url, DATA_DIR], check=True)
    else:
        # 嘗試更新 repo
        logging.info(f"Folder {DATA_DIR} already exists, attempting to update repo")
        original_dir = os.getcwd()
        os.chdir(DATA_DIR)
        
        # 確保 remote 已設定
        try:
            # 檢查 remote 是否存在
            remote_check = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
            if 'origin' not in remote_check.stdout:
                logging.info("Setting up git remote")
                subprocess.run(['git', 'remote', 'add', 'origin', repo_url], check=True)
            
            # 獲取所有分支
            subprocess.run(['git', 'fetch', '--all'], check=True)
            
            # 重設到最新狀態
            subprocess.run(['git', 'reset', '--hard', 'origin/main'], check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Git operation failed: {str(e)}, re-cloning repository")
            # 如果失敗，嘗試重新 clone
            os.chdir(original_dir)
            import shutil
            shutil.rmtree(DATA_DIR)
            os.makedirs(DATA_DIR)
            subprocess.run(['git', 'clone', repo_url, DATA_DIR], check=True)
        
            # 切回原始目錄
            os.chdir(original_dir)

# 檢查 Git 儲存庫是否需要更新
def check_git_updates():
    """
    檢查 Git 儲存庫是否需要更新
    
    Returns:
        bool: 如果需要更新則返回 True，否則返回 False
    """
    try:
        # 檢查資料夾是否存在
        if not os.path.exists(DATA_DIR):
            logging.info(f"Repository directory {DATA_DIR} does not exist, will clone")
            return True
            
        # 檢查是否為 git 儲存庫
        if not os.path.exists(os.path.join(DATA_DIR, '.git')):
            logging.info(f"Directory {DATA_DIR} is not a git repository, will re-clone")
            return True
            
        # 切換到儲存庫目錄
        original_dir = os.getcwd()
        os.chdir(DATA_DIR)
        
        try:
            # 確保 remote 已設定
            remote_check = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
            if 'origin' not in remote_check.stdout:
                logging.info("Remote not set, update needed")
                os.chdir(original_dir)
                return True
                
            # 取得最新變更
            logging.info("Fetching latest changes from remote repository...")
            subprocess.run(['git', 'fetch', '--all'], check=True)
            
            # 獲取本地 HEAD 的 commit hash
            local_hash = subprocess.run(
                ['git', 'rev-parse', 'HEAD'], 
                capture_output=True, 
                text=True, 
                check=True
            ).stdout.strip()
            
            # 獲取遠端 origin/main 的 commit hash
            remote_hash = subprocess.run(
                ['git', 'ls-remote', 'origin', 'main'], 
                capture_output=True, 
                text=True, 
                check=True
            ).stdout.strip().split()[0]
            
            # 切換回原始目錄
            os.chdir(original_dir)
            
            # 比較 hash 值
            if local_hash != remote_hash:
                logging.info(f"Repository has updates: local {local_hash[:7]} vs remote {remote_hash[:7]}")
                return True
            else:
                logging.info("No updates found in repository")
                return False
                
        except subprocess.CalledProcessError as e:
            logging.error(f"Git command execution failed: {str(e)}")
            os.chdir(original_dir)
            return True
            
    except Exception as e:
        logging.error(f"Error checking git updates: {str(e)}")
        # 如果出錯，為安全起見，假設需要更新
        return True

# 處理單一 CSV 檔案
def process_csv_file(file_path):
    df = pd.read_csv(file_path)
    return df

# 合併所有 CSV 檔案並輸出結果
def combine_csv_files():
    # 設定源文件目錄
    SOURCE_DIR = os.path.join(DATA_DIR, 'data/source')
    
    combined_df = pd.DataFrame()
    for file_name in os.listdir(SOURCE_DIR):
        if file_name.endswith('.csv'):
            file_path = os.path.join(SOURCE_DIR, file_name)
            logging.info("Processing file: %s", file_path)
            df = process_csv_file(file_path)
            combined_df = pd.concat([combined_df, df], ignore_index=True)
    # 調整欄位順序
    columns_order = ['contact', 'context', 'category', 'url', 'title']
    combined_df = combined_df[columns_order]
    combined_df.to_csv(OUTPUT_FILE, index=False)
    logging.info("Combined CSV file saved to %s", OUTPUT_FILE)

if __name__ == "__main__":
    # 檢查 Git 儲存庫是否有更新
    if check_git_updates():
        # 下載資料
        download_github_repo()
    # 合併 CSV 檔案
    combine_csv_files()
