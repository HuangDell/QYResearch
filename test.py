
import re

def extract_cagr(text):
    pattern = r'CAGR of ([-+]?\d*\.?\d+)%'
    match = re.search(pattern, text)
    if match:
        return float(match.group(1))
    else:
        return None

# 测试函数
test_string = "g a CAGR of +4.3% during "
result = extract_cagr(test_string)
print(f"Extracted CAGR: {result}%")
