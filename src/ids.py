import os
import sys

class IDSDatabase:
    # IDS 運算符 (Unicode)
    OP_LR = '\u2ff0'  # ⿰ (左右)
    OP_LMR = '\u2ff2' # ⿲ (左中右)

    def __init__(self, ids_path, debug_out_path=None):
        print("正在載入 IDS 資料庫，請稍候...")
        self.char_to_sequences = {} # 字典: 字 -> [可能的部件列表, ...]
        self.sequence_to_char = {}  # 字典: tuple(部件) -> 字 (用於驗證組合後是否為合法字)
        self._load_ids(ids_path)
        print(f"資料庫載入完成。已知漢字數: {len(self.char_to_sequences)}")
        
        if debug_out_path:
            self.dump_sequence_to_char(debug_out_path)
            print(f"已輸出序列映射到: {debug_out_path}")

    def _load_ids(self, path):
        try:
            print(f"正在讀取 {path} ...")
            count = 0
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'): continue
                    
                    parts = line.split('\t')
                    if len(parts) < 3: continue
                    
                    char = parts[1]
                    seen_ids_in_line = set()

                    for raw_ids in parts[2:]:
                        ids_str = raw_ids.split('[')[0].strip()
                        
                        if not ids_str: continue
                        if ids_str in seen_ids_in_line: continue
                        seen_ids_in_line.add(ids_str)

                        comps = []
                        if ids_str.startswith(self.OP_LR):   # ⿰
                            comps = self._parse_simple_ids(ids_str[1:])
                        elif ids_str.startswith(self.OP_LMR): # ⿲
                            comps = self._parse_simple_ids(ids_str[1:])
                        
                        if comps:
                            self._add_entry(char, comps)
                    
                    self._add_entry(char, [char])
                    count += 1
            print(f"資料庫載入完成。處理了 {count} 個漢字條目。")

        except FileNotFoundError:
            print(f"錯誤: 找不到 {path}。請確認檔案路徑。")
            sys.exit(1)

    def _parse_simple_ids(self, content_str):
        return list(content_str)

    def _add_entry(self, char, comps):
        if len(comps) > 1:
            self.sequence_to_char[tuple(comps)] = char
        
        if char not in self.char_to_sequences:
            self.char_to_sequences[char] = []
        
        if comps not in self.char_to_sequences[char]:
            self.char_to_sequences[char].append(comps)

    def dump_sequence_to_char(self, out_path):
        try:
            os.makedirs(os.path.dirname(out_path), exist_ok=True)
        except Exception:
            pass
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(f"# 共 {len(self.sequence_to_char)} 條序列映射\n")
            for comps, ch in sorted(self.sequence_to_char.items(),
                                    key=lambda kv: (kv[1], ''.join(kv[0]))):
                f.write(f"{'+'.join(comps)} -> {ch}\n")

    def get_all_linear_sequences(self, char, depth=0):
        if depth > 2: return [[char]]
        if char not in self.char_to_sequences: return [[char]]
        
        results = []
        basic_decomps = self.char_to_sequences[char]
        
        for decomp in basic_decomps:
            if len(decomp) > 1:
                results.append(decomp)
            else:
                if decomp[0] == char:
                    results.append(decomp)
                    continue

            fully_expanded = []
            for part in decomp:
                part_seqs = self.get_all_linear_sequences(part, depth + 1)
                longest_seq = max(part_seqs, key=len)
                fully_expanded.extend(longest_seq)
            
            if len(fully_expanded) > len(decomp):
                results.append(fully_expanded)

        return results if results else [[char]]

    def _resolve_seq_to_char(self, seq_tuple):
        if len(seq_tuple) == 1:
            return seq_tuple[0]
        return self.sequence_to_char.get(seq_tuple)

    def find_match(self, char_a, char_b):
        seqs_a = self.get_all_linear_sequences(char_a)
        seqs_b = self.get_all_linear_sequences(char_b)
        found_combinations = []

        for sa in seqs_a:
            if len(sa) < 2: continue
            for sb in seqs_b:
                if len(sb) < 2: continue

                for i in range(1, len(sa)):
                    x_seq = tuple(sa[:i])
                    a_tail = sa[i:]
                    x_char = self._resolve_seq_to_char(x_seq)
                    if not x_char: continue

                    for j in range(1, len(sb)):
                        b_head = sb[:j]
                        z_seq = tuple(sb[j:])
                        z_char = self._resolve_seq_to_char(z_seq)
                        if not z_char: continue

                        y_seq = tuple(a_tail + b_head)
                        y_char = self._resolve_seq_to_char(y_seq)
                        
                        if y_char:
                            found_combinations.append(f"{x_char}{y_char}{z_char}")

        return list(set(found_combinations))