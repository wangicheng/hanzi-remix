import os
from src.corpus import extract_from_cedict, extract_from_jieba, save_word_list

# 設定路徑
DATA_DIR = 'data'
OUTPUT_DIR = 'output'

CEDICT_FILE = os.path.join(DATA_DIR, 'cedict_ts.u8')
JIEBA_FILE = os.path.join(DATA_DIR, 'dict.txt.big')
MERGED_OUTPUT = os.path.join(OUTPUT_DIR, 'merged_words.txt')

def main():
    print("開始執行資料前處理...")
    
    # 1. 提取 CEDICT
    print("正在處理 CEDICT...")
    cedict_words = extract_from_cedict(CEDICT_FILE)
    print(f"CEDICT 提取數量: {len(cedict_words)}")
    
    # 2. 提取 Jieba
    print("正在處理 Jieba 字典...")
    jieba_words = extract_from_jieba(JIEBA_FILE, min_freq=50) # 可調整頻率閾值
    print(f"Jieba 提取數量: {len(jieba_words)}")
    
    # 3. 合併 (聯集)
    all_words = cedict_words.union(jieba_words)
    print(f"合併後總數量: {len(all_words)}")
    
    # 4. 輸出
    save_word_list(all_words, MERGED_OUTPUT)
    print("前處理完成！")

if __name__ == "__main__":
    main()