# Quick Start Guide

## 5 Bước Để Bắt Đầu

### 1️⃣ Cài Đặt (2 phút)

```bash
# Tạo virtual environment
python -m venv venv
venv\Scripts\activate

# Cài packages
pip install -r requirements.txt

# Set API key
$env:ANTHROPIC_API_KEY = "sk-ant-your-key-here"
```

### 2️⃣ Kiểm Tra Config (1 phút)

Mở `config.py` và đảm bảo:
- ✅ `API_KEY` được set (hoặc dùng environment variable)
- ✅ `NUM_RECORDS = 100` (hay bao nhiêu bạn muốn)
- ✅ `MODEL_NAME = "claude-3-5-sonnet-20241022"` (điều chỉnh nếu cần)

### 3️⃣ Sinh Dữ Liệu (10-20 phút)

```bash
python generate_data.py --num-records 50
```

**Output bạn sẽ thấy:**
```
============================================================
Starting Fine-tuning Data Generation
============================================================
Target records: 50
Output file: data.json
...
[1/50] Sinh: DEBUG_FOCUS (Bank, Mới bắt đầu)...
Generating problem: DEBUG_FOCUS / Bank / Mới bắt đầu
Generating teaching response for DEBUG_FOCUS
✅ Lưu records #1
...
```

### 4️⃣ Kiểm Tra Output (2 phút)

```python
# Xem file data.json được tạo
import json

with open("data.json", "r", encoding="utf-8") as f:
    records = json.load(f)
    
print(f"Total records: {len(records)}")
print(f"First record keys: {records[0].keys()}")
print(f"Messages: {records[0]['messages'][0]}")
```

### 5️⃣ Tối Ưu & Expand (Tuỳ)

```bash
# Sinh thêm 50 records nữa (sẽ append vào file cũ)
python generate_data.py --num-records 50

# Hoặc sinh từ đầu với output file mới
python generate_data.py --num-records 100 --output data_v2.json
```

---

## 📋 Common Commands

### Sinh 100 Records (Default)
```bash
python generate_data.py
```

### Sinh X Records
```bash
python generate_data.py --num-records 200
```

### Sinh Đến File Khác
```bash
python generate_data.py --output my_dataset.json --num-records 100
```

### Debug Mode (Xem chi tiết)
```bash
python generate_data.py --debug
```

### Không Backup
```bash
python generate_data.py --no-backup
```

### Kết Hợp Nhiều Tuỳ Chọn
```bash
python generate_data.py \
    --num-records 200 \
    --output train_data.json \
    --batch-size 5 \
    --debug
```

---

## 🎛️ Tuỳ Chỉnh Focus Areas

### Mặc Định (Balanced)
```python
FOCUS_DISTRIBUTIONS = {
    "DEBUG_FOCUS": 0.25,
    "OPTIMIZATION_FOCUS": 0.25,
    "EDGE_CASE_FOCUS": 0.25,
    "CONCEPT_FOCUS": 0.15,
    "SCAFFOLDING_FOCUS": 0.10,
}
```

### Tập Trung Debug
```python
FOCUS_DISTRIBUTIONS = {
    "DEBUG_FOCUS": 0.50,           # 50%
    "OPTIMIZATION_FOCUS": 0.20,   # 20%
    "EDGE_CASE_FOCUS": 0.15,      # 15%
    "CONCEPT_FOCUS": 0.10,         # 10%
    "SCAFFOLDING_FOCUS": 0.05,     # 5%
}
```

### Tập Trung Algorithm Learning
```python
FOCUS_DISTRIBUTIONS = {
    "SCAFFOLDING_FOCUS": 0.40,    # 40% - Dàn ý thuật toán
    "CONCEPT_FOCUS": 0.30,         # 30% - Khái niệm
    "DEBUG_FOCUS": 0.20,           # 20% - Debug
    "EDGE_CASE_FOCUS": 0.10,       # 10% - Edge case
    "OPTIMIZATION_FOCUS": 0.00,    # 0% - Không có
}
```

---

## 🔍 Xem Kết Quả

### Xem JSON Structure

```bash
# Windows PowerShell
Get-Content data.json -TotalCount 20

# Linux/macOS
head -20 data.json
```

### Format Đúng Không?

```python
import json

with open("data.json", "r", encoding="utf-8") as f:
    records = json.load(f)

record = records[0]
print("Structure check:")
print(f"- Has 'messages'? {('messages' in record)}")
print(f"- Message count? {len(record['messages'])}")
print(f"- Roles? {[m['role'] for m in record['messages']]}")
print(f"\nFirst message (system):")
print(record['messages'][0]['content'][:100])
print(f"\nSecond message (user) preview:")
print(record['messages'][1]['content'][:200])
print(f"\nThird message (assistant) preview:")
print(record['messages'][2]['content'][:200])
```

### Đếm Records Theo Focus Area

```python
import json
from collections import Counter

with open("data.json", "r", encoding="utf-8") as f:
    records = json.load(f)

# Phải parse từ system message
focus_counts = Counter()
for record in records:
    system_msg = record['messages'][0]['content']
    for focus in ["DEBUG", "OPTIM", "EDGE", "CONCEPT", "SCAFFOLDING"]:
        if focus in system_msg:
            focus_counts[focus] += 1

print("Focus distribution:")
for focus, count in focus_counts.most_common():
    print(f"  {focus}: {count} ({100*count/len(records):.1f}%)")
```

---

## ⚠️ Troubleshooting

### Problem: "ANTHROPIC_API_KEY not provided"

**Solution:**
```bash
# Set environment variable
$env:ANTHROPIC_API_KEY = "sk-ant-xxx"

# Or create .env file with:
# ANTHROPIC_API_KEY=sk-ant-xxx
```

### Problem: "Rate limit, retry in 2s..."

**Normal** - Script tự động retry, không cần làm gì

### Problem: "Failed to parse problem response"

**Solution:** 
- Check API key hợp lệ
- Kiểm tra model name (claude-3-5-sonnet-20241022)
- Try lại với `--debug` flag

### Problem: Network timeout

**Solution:**
```python
# Tăng timeout trong config.py
API_TIMEOUT = 180  # từ 120 thành 180
```

---

## 📊 Expected Results

Khi chạy thành công, bạn sẽ nhìn thấy:

```
✅ [1/50] DEBUG_FOCUS completed (824 tokens)
✅ [2/50] OPTIMIZATION_FOCUS completed (1205 tokens)
✅ [3/50] EDGE_CASE_FOCUS completed (945 tokens)
...
Generation Complete!
Total records in file: 50
Token usage: 70,250 tokens (~$0.21)
```

File `data.json` sẽ chứa 50 conversations, sẵn sàng fine-tune!

---

## 🎓 Next Steps

1. **Validate Quality**: Xem vài records bằng tay, đảm bảo quality tốt
2. **Expand Dataset**: Sinh 1,000+ records cho production
3. **Fine-tune Model**: Upload `data.json` lên OpenAI/Hugging Face
4. **Evaluate**: Test performance trên validation set
5. **Iterate**: Feedback → Adjust prompts → Re-generate

---

## 📞 Support

Issues?
- Check `generation.log` file
- Run with `--debug` flag
- Verify API key and network
- Check Claude API status page
