import json
import re

def is_valid_response(response):
    """
    判断 response 是否精确匹配 <think>...</think><answer>...</answer> 的结构
    """
    if not isinstance(response, str):
        return False
    # 匹配完整的 think + answer 结构，允许中间有换行
    pattern = r'^<think>[\s\S]*?</think>\s*<answer>[\s\S]*?</answer>\s*$'
    return re.match(pattern, response.strip()) is not None

def filter_jsonl_by_response(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            try:
                record = json.loads(line)
                response = record.get("response", "")
                if is_valid_response(response):
                    outfile.write(json.dumps(record, ensure_ascii=False) + '\n')
            except json.JSONDecodeError:
                continue  # 跳过无效 JSON 行

if __name__ == '__main__':
    input_path = '/mnt/data/dhd/dataset/sft_train.jsonl'   # 替换为你的输入文件路径
    output_path = '/mnt/data/dhd/dataset/sft_train_c.jsonl'  # 输出文件路径
    print('claer begin')
    filter_jsonl_by_response(input_path, output_path)
    print('claer end')
