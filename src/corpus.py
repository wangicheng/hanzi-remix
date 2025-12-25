import re
import os

def extract_from_cedict(input_file):
    """從 CC-CEDICT 提取雙字詞"""
    words = set()
    pattern = re.compile(r'^([^\s]{2})\s+([^\s]{2})\s+\[[^\s]+\s+[^\s]+\]')
    
    if not os.path.exists(input_file):
        print(f"[警告] 找不到 {input_file}")
        return words

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#') or not line.strip(): continue
            match = pattern.match(line)
            if match:
                words.add(match.group(1)) # 繁體
                words.add(match.group(2)) # 簡體
    return words

def extract_from_jieba(input_file, min_freq=100):
    """從 Jieba 字典提取高頻雙字詞"""
    words = set()
    if not os.path.exists(input_file):
        print(f"[警告] 找不到 {input_file}")
        return words

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(' ')
            if len(parts) < 2: continue
            
            word = parts[0]
            freq = int(parts[1]) if len(parts) > 1 else 0
            
            if len(word) == 2 and freq >= min_freq:
                words.add(word)
    return words

def save_word_list(words, output_file):
    """儲存詞表"""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    sorted_words = sorted(list(words))
    with open(output_file, 'w', encoding='utf-8') as f:
        for w in sorted_words:
            f.write(f"{w}\n")
    print(f"已儲存 {len(words)} 個詞彙至 {output_file}")