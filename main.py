import os
from src.ids import IDSDatabase

# 設定檔案路徑
IDS_FILE = os.path.join('data', 'ids.txt')
INPUT_FILE = os.path.join('output', 'merged_words.txt')
OUTPUT_FILE = os.path.join('output', 'found_results.txt')

def main():
    if not os.path.exists(IDS_FILE):
        print(f"錯誤: 找不到 {IDS_FILE}")
        return

    if not os.path.exists(INPUT_FILE):
        print(f"錯誤: 找不到 {INPUT_FILE}。請先執行 'python preprocess.py'")
        return

    # 初始化資料庫
    db = IDSDatabase(IDS_FILE)
    
    print(f"開始分析詞彙表: {INPUT_FILE}")
    
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        words = [line.strip() for line in f if line.strip()]

    total = len(words)
    count_found = 0
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f_out:
        for idx, word in enumerate(words):
            if len(word) != 2: continue
            
            matches = db.find_match(word[0], word[1])
            if matches:
                result_str = f"{word} -> {', '.join(matches)}"
                f_out.write(result_str + "\n")
                count_found += 1
            
            if idx % 5000 == 0:
                print(f"進度: {idx}/{total} (已找到 {count_found} 組)")

    print(f"完成。共找到 {count_found} 組結果，已儲存至 {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
