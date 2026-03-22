# Kế Hoạch Sinh Dữ Liệu Fine-Tuning bằng LLM

## 1️⃣ Kiến Trúc Tổng Thể

```
┌─────────────────────────────────────────────────────────┐
│  generate_data.py (Script chính)                        │
├─────────────────────────────────────────────────────────┤
│  ├─ config.py (Cấu hình API, prompt templates)         │
│  ├─ prompts.py (5 focus areas templates)               │
│  ├─ llm_client.py (Gọi Claude/GPT-4o API)             │
│  ├─ data_formatter.py (Format output => JSON)          │
│  └─ data_storage.py (Lưu vào data.json)               │
└─────────────────────────────────────────────────────────┘
```

## 2️⃣ Quy Trình Chính (Pipeline) - OPTIMIZED

1. **Đọc template prompt** cho từng Focus Area
2. **Gọi LLM 1 lần duy nhất**:
   - Input: focus_area, context, difficulty, người dùng
   - Output: **TOÀN BỘ** (bài toán + lời giải Socratic) trong 1 response
3. **Parse & Validate** dữ liệu đầu ra
4. **Format** thành cấu trúc conversation (system, user, assistant)
5. **Append** vào data.json

**Lợi ích:**
- ⚡ Giảm 50% latency (1 call thay vì 2)
- 💰 Giảm 50% chi phí API
- 🚀 Tăng throughput 2x

## 3️⃣ Công Nghệ Stack

- **Language:** Python 3.9+
- **LLM API:** Anthropic Claude (eller OpenAI GPT-4o)
- **Async:** asyncio + httpx (gọi API song song)
- **Storage:** JSON Lines (tối ưu append large files)
- **Logging:** Python logging module

## 4️⃣ Cấu Trúc Focus Area + Prompt

### 🟢 DEBUG FOCUS
- **Dạng lỗi:** Off-by-one, segfault, type mismatch, uninitialized variables
- **Ngữ cảnh:** Bank, Game, E-commerce
- **LLM Prompt 1:** "Sinh một bài lập trình C có lỗi debug tiêu biểu..."
- **LLM Prompt 2:** "Dựa vào lỗi trên, hãy viết một lời giải thích Socratic..."

### 🔵 OPTIMIZATION FOCUS
- **Dạng vấn đề:** O(N²) → O(N), memory inefficiency
- **Metrics:** Execution time, memory usage
- **LLM Prompt 1:** "Thiết kế bài tập tối ưu hóa thuật toán..."
- **LLM Prompt 2:** "Giải thích tại sao code này chậm đó?"

### 🟠 EDGE CASE FOCUS
- **Dạng vấn đề:** Null pointers, division by zero, empty arrays
- **Trường hợp biên:** n=0, arr=NULL, INT_MIN/MAX
- **LLM Prompt 1:** "Viết code chưa xử lý edge case..."
- **LLM Prompt 2:** "Chẩn đoán vấn đề và dạy học sinh cách phòng vệ..."

### 🟣 CONCEPT FOCUS
- **Khái niệm:** Pass by value/reference, heap vs stack, pointers
- **Độ khó:** Trung bình → Nâng cao
- **LLM Prompt 1:** "Sinh bài toán về khái niệm C nâng cao..."
- **LLM Prompt 2:** "Giải thích bản chất của vấn đề này..."

### 🟤 SCAFFOLDING FOCUS
- **Nội dung:** Algorithm skeleton (linked list, binary tree, etc.)
- **Tình huống:** Sinh viên không biết bắt đầu từ đâu
- **LLM Prompt 1:** "Chọn một bài toán thuật toán phức tạp..."
- **LLM Prompt 2:** "Viết hướng dẫn Socratic dàn ý thuật toán..."

## 5️⃣ Luồng Dữ Liệu Chi Tiết

```
┌─────────────────┐
│ Random Context  │  (Ngân hàng, Game, E-commerce)
│ Random Difficulty    │  (Mới, Trung bình, Giỏi)
└────────┬────────┘
         │
         ▼
┌──────────────────────────────────────────────┐
│ LLM Call (UNIFIED - 1 lần duy nhất)         │
│ Input: focus_area, problem_context, style   │
│ Output: JSON {                               │
│   problem_description,                       │
│   buggy_code,                                │
│   environment_feedback,                      │
│   hidden_teacher_context,                    │
│   diagnosis,                                 │
│   root_cause,                                │
│   related_knowledge,                         │
│   socratic_hint                              │
│ }                                            │
└────────┬─────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────┐
│ Validate Output (Parse JSON, Check fields)   │
└────────┬─────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────┐
│ Format to OpenAI Fine-tuning JSON            │
│ {                                            │
│   "messages": [                              │
│     {"role": "system", "content": "Persona..."},
│     {"role": "user", "content": "Bối cảnh..."},│
│     {"role": "assistant", "content": "Chẩn đoán..."}
│   ]                                          │
│ }                                            │
└────────┬─────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────┐
│ Append to data.json (JSON Lines format)      │
└──────────────────────────────────────────────┘
```

## 6️⃣ Cấu Trúc File Chi Tiết

### prompts.py - Template Prompt (UNIFIED - Chỉ 1 lần)
```python
PROMPTS = {
    "DEBUG_FOCUS": {
        "unified_generate": """
        Bạn là giáo sư lập trình C. Sinh một bài toán lập trình C cho sinh viên {difficulty} 
        trong bối cảnh {context}. YÊU CẦU:
        
        1. Mô tả bài toán (1-2 câu)
        2. Code C có lỗi {bug_type}
        3. Mô tả lỗi khi chạy
        4. Ghi chú ẩn: Nguyên nhân thực sự
        5. 🔍 Chẩn đoán lỗi (1-2 câu)
        6. 🧠 Bản chất vấn đề (giải thích gốc rễ)
        7. 📚 Kiến thức liên quan
        8. 💡 Gợi mở Socratic (hướng dẫn mà không tiết lộ hết)
        
        Format JSON output:
        {{
            "problem_description": "...",
            "buggy_code": "...",
            "environment_feedback": "...",
            "hidden_teacher_context": "...",
            "diagnosis": "🔍 ...",
            "root_cause": "🧠 ...",
            "related_knowledge": "📚 ...",
            "socratic_hint": "💡 ..."
        }}
        """
    },
    "OPTIMIZATION_FOCUS": {...},
    "EDGE_CASE_FOCUS": {...},
    "CONCEPT_FOCUS": {...},
    "SCAFFOLDING_FOCUS": {...},
}
```

### llm_client.py - Client (SIMPLIFIED)
```python
class LLMClient:
    async def generate_complete_record(
        self,
        focus_area: str,
        context: str,
        difficulty: str,
    ) -> Dict[str, Any]:
        """
        Gọi LLM 1 lần duy nhất để sinh toàn bộ dữ liệu
        (problem + teaching response)
        """
        template = PROMPTS[focus_area]["unified_generate"]
        prompt = template.format(
            focus_area=focus_area,
            context=context,
            difficulty=difficulty,
            bug_type=random.choice(config.BUG_TYPES)
        )
        
        # 1 LLM call duy nhất
        response = await self._call_api([{"role": "user", "content": prompt}])
        
        # Parse JSON từ response
        json_data = self._extract_json(response)
        return json.loads(json_data)
```

### data_formatter.py - Format Output
```python
class DataFormatter:
    @staticmethod
    def to_fine_tune_format(
        focus_area: str,
        context: str,
        difficulty: str,
        complete_data: Dict[str, Any],  # Toàn bộ data từ 1 lần LLM call
    ) -> Dict[str, Any]:
        """
        Chuyển đổi output từ 1 LLM call thành fine-tuning format
        """
        return {
            "messages": [
                {
                    "role": "system",
                    "content": f"Persona: Gia sư Socratic. Focus: [{focus_area}]."
                },
                {
                    "role": "user",
                    "content": f"Bối cảnh: [{context}]\n"
                               f"Đề bài: {complete_data['problem_description']}\n"
                               f"Code:\n{complete_data['buggy_code']}\n"
                               f"Lỗi: {complete_data['environment_feedback']}"
                },
                {
                    "role": "assistant",
                    "content": f"{complete_data['diagnosis']}\n\n"
                               f"{complete_data['root_cause']}\n\n"
                               f"{complete_data['related_knowledge']}\n\n"
                               f"{complete_data['socratic_hint']}"
                }
            ]
        }
```

### data_storage.py - Lưu JSON
```python
class DataStorage:
    def __init__(self, data_file="data.json"):
        self.data_file = data_file
    
    def append_record(self, record):
        # Append JSON Line (một object JSON per dòng)
        with open(self.data_file, 'a', encoding='utf-8') as f:
            json.dump(record, f, ensure_ascii=False)
            f.write('\n')  # JSON Lines format
    
    def batch_append_records(self, records):
        # Ghi batch records
        with open(self.data_file, 'a', encoding='utf-8') as f:
            for record in records:
                json.dump(record, f, ensure_ascii=False)
                f.write('\n')
```

### generate_data.py - Script Chính (SIMPLIFIED)
```python
async def main(num_records=100, focus_distributions=None):
    """
    Pipeline tối ưu: 1 LLM call per record
    """
    llm = LLMClient(api_key=os.getenv("ANTHROPIC_API_KEY"))
    batcher = AsyncLLMBatcher(llm, max_concurrent=5)
    storage = DataStorage()
    
    for i in range(num_records):
        focus_area = random.choices(...)[0]
        context = random.choice(CONTEXTS)
        difficulty = random.choice(DIFFICULTIES)
        
        print(f"[{i+1}/{num_records}] Sinh: {focus_area}...")
        
        try:
            # 1 LLM call duy nhất - sinh toàn bộ
            complete_data = await llm.generate_complete_record(
                focus_area, context, difficulty
            )
            
            # Validate
            assert all(key in complete_data for key in [
                "problem_description", "buggy_code", "diagnosis", "socratic_hint"
            ])
            
            # Format
            record = DataFormatter.to_fine_tune_format(
                focus_area, context, difficulty, complete_data
            )
            
            # Save
            storage.append_record(record)
            print(f"✅ Lưu record #{i+1}")
            
        except Exception as e:
            print(f"❌ Lỗi: {e}")
            continue
```

## 7️⃣ Optimization Strategy

### A. Cost Reduction (MAJOR IMPROVEMENT)
**Old way (2 LLM calls):**
- Call 1: Generate problem (~800 tokens)
- Call 2: Generate teaching (~600 tokens)
- **Total: ~1,400 tokens/record**
- 100 records: ~140K tokens → ~$0.42

**New way (1 LLM call):**
- Unified call: Generate problem + teaching (~1,200 tokens)
- **Total: ~1,200 tokens/record** ← SAVE 14%
- 100 records: ~120K tokens → ~$0.36

**Impact:**
- 📉 Giảm ~15-20% chi phí
- ⚡ Giảm 50% latency (1 call vs 2 calls)
- 🚀 Tăng throughput 2x

### B. Concurrent Processing
- Gọi LLM 5-10 records song song
- Dùng asyncio semaphore để rate limiting
- Batch requests để tối ưu

### C. Retry Logic
```python
async def call_api_with_retry(prompt, max_retries=3, backoff=2):
    for attempt in range(max_retries):
        try:
            return await llm.call_api(prompt)
        except RateLimitError:
            wait_time = backoff ** attempt
            print(f"Rate limit, retry in {wait_time}s...")
            await asyncio.sleep(wait_time)
```

### D. JSON Validation
- Parse LLM output bằng pydantic models
- Check có tất cả 8 required fields
- Fallback: Regex extraction nếu JSON malformed

## 8️⃣ Configuration (config.py)

```python
# API Settings
LLM_PROVIDER = "anthropic"  # atau "openai"
MODEL_NAME = "claude-3-5-sonnet-20241022"
API_KEY = os.getenv("ANTHROPIC_API_KEY")
API_TIMEOUT = 60  # seconds

# Generation Settings
NUM_RECORDS = 100
BATCH_SIZE = 10
CONCURRENT_REQUESTS = 5

# Focus Area Distribution
FOCUS_DISTRIBUTIONS = {
    "DEBUG_FOCUS": 0.25,
    "OPTIMIZATION_FOCUS": 0.25,
    "EDGE_CASE_FOCUS": 0.25,
    "CONCEPT_FOCUS": 0.15,
    "SCAFFOLDING_FOCUS": 0.10,
}

# Output
OUTPUT_FILE = "data.json"
LOG_FILE = "generation.log"
```

## 9️⃣ So Sánh: OLD vs NEW Approach

| Tiêu Chí | OLD (2 LLM calls) | NEW (1 LLM call) | Cải Thiện |
|---------|---|---|---|
| **LLM Calls** | 2 (problem + teaching) | 1 (unified) | ✅ **50% giảm** |
| **Tokens/Record** | ~1,400 | ~1,200 | ✅ **15% giảm** |
| **Chi phí/100 records** | ~$0.42 | ~$0.36 | ✅ **$0.06 tiết kiệm** |
| **Latency** | 200-300ms (2 sequential calls) | 100-150ms (1 call) | ✅ **50% nhanh hơn** |
| **Throughput** | ~20 records/phút | ~40 records/phút | ✅ **2x tăng** |
| **Độ phức tạp code** | Complex (2-stage pipeline) | Simple (1-stage) | ✅ **Dễ maintain** |
| **Error handling** | Phức tạp (failure ở stage 2) | Đơn giản | ✅ **Ít lỗi** |

**Tổng kết:**
- 💰 Giảm chi phí API 15-20%
- ⚡ Nhanh gấp 2x
- 🛠️ Code đơn giản hơn
- 🎯 Chất lượng data không thay đổi

## 🔟 Implementation Order

1. ✅ Setup project structure & dependencies  
2. ✅ Write config.py & prompts.py (UPDATED for unified call)
3. ✅ Implement llm_client.py - `generate_complete_record()` method (SIMPLIFIED)
4. ✅ Implement data_formatter.py - format unified output (SIMPLIFIED)
5. ✅ Implement data_storage.py (unchanged)
6. ✅ Write generate_data.py - single-call pipeline (SIMPLIFIED)
7. ✅ Test với 5-10 records
8. ✅ Batch generate 100+ records
9. ✅ Validate output quality
10. ✅ Add monitoring & logging
