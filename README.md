# Fine-tuning Data Generation System

Hệ thống tự động sinh dữ liệu fine-tuning cho mô hình ngôn ngữ 8B bằng LLM (Claude).

## 📋 Tổng Quan

Dự án này sinh dữ liệu huấn luyện cho một mô hình 8B để dạy lập trình C theo phong cách Socratic. Mỗi bản ghi gồm 3 thành phần:
- **System**: Mô tả persona của giáo viên
- **User**: Sinh viên đặt bài toán (bối cảnh + code có lỗi)
- **Assistant**: Giáo viên phản hồi theo hướng Socratic

## 🎯 5 Focus Areas

Dữ liệu được phân loại theo 5 khu vực học tập:

### 1. **DEBUG FOCUS** (25%)
- **Vấn đề**: Lỗi cú pháp, logic, runtime errors
- **Ví dụ**: Off-by-one errors, Segmentation faults, Type mismatch
- **Phương pháp dạy**: Hướng dẫn sinh viên tìm và sửa lỗi

### 2. **OPTIMIZATION FOCUS** (25%)
- **Vấn đề**: Hiệu suất thuật toán (Time/Memory)
- **Ví dụ**: O(N²) → O(N log N) conversion
- **Phương pháp dạy**: Giải thích Big O, đề xuất giải pháp

### 3. **EDGE CASE FOCUS** (25%)
- **Vấn đề**: Các trường hợp biên
- **Ví dụ**: Mảng rỗng, null pointers, division by zero
- **Phương pháp dạy**: Defensive programming

### 4. **CONCEPT FOCUS** (15%)
- **Vấn đề**: Khái niệm nâng cao
- **Ví dụ**: Pass by value/reference, Pointers, Memory management
- **Phương pháp dạy**: Giải thích bằng ẩn dụ

### 5. **SCAFFOLDING FOCUS** (10%)
- **Vấn đề**: Viết thuật toán từ đầu
- **Ví dụ**: Reverse linked list, BFS, Tree traversal
- **Phương pháp dạy**: Dàn ý từng bước

## 🛠️ Cài Đặt

### Yêu Cầu
- Python 3.9+
- Anthropic API key (Claude)

### Các Bước

1. **Clone repo hoặc tạo thư mục mới**
```bash
mkdir gen_data_finetune
cd gen_data_finetune
```

2. **Tạo virtual environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. **Cài các package**
```bash
pip install -r requirements.txt
```

4. **Setup environment variable**
Tạo file `.env` trong root thư mục:
```
ANTHROPIC_API_KEY=sk-ant-xxxxxxx
```

Hoặc set trực tiếp trong terminal:
```bash
# Windows (PowerShell)
$env:ANTHROPIC_API_KEY = "sk-ant-xxx"

# macOS/Linux
export ANTHROPIC_API_KEY="sk-ant-xxx"
```

## 📖 Cách Sử Dụng

### Tùy Chọn 1: Sinh Dữ Liệu (Mặc Định 100 Records)

```bash
python generate_data.py
```

**Output**:
```
============================================================
Starting Fine-tuning Data Generation
============================================================
Target records: 100
Output file: data.json
Batch size: 10
Focus distributions: {'DEBUG_FOCUS': 0.25, ...}
============================================================

[1/100] Sinh: DEBUG_FOCUS (Bank, Mới bắt đầu)...
✅ Lưu records #1

[2/100] Sinh: OPTIMIZATION_FOCUS (Game, Trung bình)...
✅ Lưu records #2
...
```

### Tùy Chọn 2: Túy Chỉnh Số Lượng

```bash
python generate_data.py --num-records 50
```

### Tùy Chọn 3: Túy Chỉnh Output File

```bash
python generate_data.py --output my_data.json --num-records 100
```

### Tùy Chọn 4: Debug Mode

```bash
python generate_data.py --debug
```

### Tùy Chọn 5: Không Backup

```bash
python generate_data.py --no-backup
```

## 📁 Cấu Trúc Thư Mục

```
gen_data_finetune/
├── config.py                  # Cấu hình chính
├── prompts.py                 # LLM prompt templates
├── llm_client.py              # API client + retry logic
├── data_formatter.py          # Format output → JSON
├── data_storage.py            # Lưu/load JSON
├── generate_data.py           # Main script
├── requirements.txt           # Dependencies
├── .env                       # API key (tạo tuỳ)
├── PLAN.md                    # Kế hoạch chi tiết
├── README.md                  # File này
├── data.json                  # Output records
├── generation.log             # Log file
└── data_backup.json           # Backup
```

## ⚙️ Cấu Hình

Tất cả các setting nằm ở `config.py`. Một số tuỳ chọn quan trọng:

```python
# Số records tối đa
NUM_RECORDS = 100

# Batch size (sinh song song bao nhiêu request)
BATCH_SIZE = 10
CONCURRENT_REQUESTS = 5

# Phân bố focus areas
FOCUS_DISTRIBUTIONS = {
    "DEBUG_FOCUS": 0.25,
    "OPTIMIZATION_FOCUS": 0.25,
    "EDGE_CASE_FOCUS": 0.25,
    "CONCEPT_FOCUS": 0.15,
    "SCAFFOLDING_FOCUS": 0.10,
}

# Contexts
CONTEXTS = ["Bank", "Game", "E-commerce", "Healthcare", ...]

# Độ khó
DIFFICULTIES = ["Mới bắt đầu", "Trung bình", "Giỏi"]

# LLM
MODEL_NAME = "claude-3-5-sonnet-20241022"
API_TIMEOUT = 120
MAX_RETRIES = 3
```

## 📊 Output Format

Mỗi record có cấu trúc sau:

```json
{
  "messages": [
    {
      "role": "system",
      "content": "Persona: Gia sư Socratic. Trình độ: [Mới bắt đầu]. Focus: [Debug Focus]."
    },
    {
      "role": "user",
      "content": "Bối cảnh: [Bank]\nĐề bài: ...\nCode:\n...\nLỗi: Segmentation fault"
    },
    {
      "role": "assistant",
      "content": "🔍 **Chẩn đoán lỗi**: ...\n🧠 **Bản chất**: ...\n📚 **Kiến thức**: ...\n💡 **Gợi mở**: ..."
    }
  ]
}
```

## 🔍 Logging

- **Log File**: `generation.log` - Lưu trữ tất cả log
- **Console**: Hiển thị real-time progress
- **Debug Mode**: `python generate_data.py --debug`

## 💰 Ước Tính Chi Phí

Mỗi record cần:
- **LLM Call 1** (Generate problem): ~800 tokens
- **LLM Call 2** (Generate teaching): ~600 tokens
- **Total**: ~1,400 tokens/record

Với Claude 3.5 Sonnet:
- Input: $0.003/1K tokens
- Ước tính: (1,400 / 1000) × 0.003 = $0.0042 / record
- 100 records: ~$0.42
- 1,000 records: ~$4.20

## 🐛 Xử Lý Lỗi

### API Rate Limiting
```
⏳ Rate limit, retry in 2s...
```
Script tự động retry với exponential backoff

### JSON Parse Error
```
❌ Failed to parse problem response: ...
```
Kiểm tra output từ LLM có chứa JSON hợp lệ không

### API Key Missing
```
Error: ANTHROPIC_API_KEY not provided
```
Đảm bảo set environment variable

## 🚀 Advanced Usage

### Tạo Custom Prompt

Chỉnh sửa `prompts.py`:

```python
PROMPTS["DEBUG_FOCUS"]["stage_1_generate"] = """
Custom prompt...
"""
```

### Thêm Focus Area Mới

1. Thêm template vào `prompts.py`
2. Cập nhật `FOCUS_DISTRIBUTIONS` trong `config.py`
3. Tùy chỉnh persona trong `PERSONAS`

### Merge Với Existing Data

```python
storage = DataStorage("data.json")
existing = storage.load_existing()
new_records = [...]
existing.extend(new_records)
storage.save_records(existing, overwrite=True)
```

## 📈 Monitoring

Xem token usage:
```
Token usage: 140,000 tokens (~$0.42)
```

Xem record count:
```
Total records in file: 100
```

## 🔒 Best Practices

1. **Luôn backup trước sinh data**: `--no-backup` chỉ dùng khi chắc chắn
2. **Kiểm tra output quality**: Xem vài records đầu tiên bằng tay
3. **Sử dụng JSON Lines format** cho large datasets: `USE_JSONL = True` trong config
4. **Test với batch nhỏ**: Sinh 5-10 records trước để test quality

## 📚 Chi Tiết Kỹ Thuật

### Async Pipeline

```
┌─────────────────┐
│ Random Contexts │
└────────┬────────┘
         │
         ▼
┌──────────────────────┐
│ AsyncLLMBatcher      │  (Concurrent requests)
│ - Generate Problem   │  
│ - Generate Teaching  │  
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│ Format & Validate    │
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│ Save to JSON file    │
└──────────────────────┘
```

### Retry Strategy

- **Attempt 1**: Immediate
- **Attempt 2**: Wait 2^1 = 2 seconds
- **Attempt 3**: Wait 2^2 = 4 seconds
- Max 3 attempts total

## 📖 Tài Liệu Tham Khảo

- [Anthropic Claude API](https://docs.anthropic.com/)
- [OpenAI Fine-tuning Format](https://platform.openai.com/docs/tutorials/fine-tuning)
- [Socratic Method](https://en.wikipedia.org/wiki/Socratic_method)

## 🤝 Contribution

Các cách góp ý:
1. Thêm prompt mới cho các kịch bản khác
2. Cải thiện persona definitions
3. Tối ưu token usage
4. Add support cho LLM providers khác (OpenAI, LLaMA, etc.)

## 📝 License

MIT License - Tự do sử dụng và sửa đổi

---

**Tác giả**: Gen Data Finetune System  
**Ngày tạo**: 2024  
**Phi bản**: 1.0
#   g e n _ d a t a _ f i n e t u n e  
 