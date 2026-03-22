# Hướng Dẫn Chuyển Từ 2-Stage Sang 1-Stage LLM Call

## 📋 Tóm Tắt Thay Đổi

| File | Thay Đổi |
|------|---------|
| **prompts.py** | Thay stage_1 + stage_2 → "unified" key (1 prompt) |
| **llm_client.py** | Xóa generate_problem() + generate_teaching() → generate_complete_record() |
| **data_formatter.py** | Nhận complete_data (không phải problem_data + response) |
| **generate_data.py** | 1 LLM call thay vì 2, logic đơn giản hơn |
| **config.py** | TOKENS_PER_UNIFIED_CALL = 1200 (thay vì 1400) |

---

## 🔧 Chi Tiết Thay Đổi

### 1️⃣ prompts.py

**TỪ (Old):**
```python
PROMPTS = {
    "DEBUG_FOCUS": {
        "stage_1_generate": """...""",
        "stage_2_teach": """...""",
    }
}
```

**THÀNH (New):**
```python
PROMPTS = {
    "DEBUG_FOCUS": {
        "unified": """
        Sinh một bài toán lập trình C cho sinh viên {difficulty} trong bối cảnh {context}.
        
        YÊU CẦU - Sinh ra TẤT CẢ các phần:
        1. problem_description
        2. buggy_code
        3. environment_feedback
        4. hidden_teacher_context
        5. diagnosis
        6. root_cause
        7. related_knowledge
        8. socratic_hint
        
        FORMAT OUTPUT (JSON):
        {
            "problem_description": "...",
            "buggy_code": "...",
            "environment_feedback": "...",
            "hidden_teacher_context": "...",
            "diagnosis": "🔍 ...",
            "root_cause": "🧠 ...",
            "related_knowledge": "📚 ...",
            "socratic_hint": "💡 ..."
        }
        """
    }
}
```

➡️ **Thực hiện:** Replace tất cả 5 focus areas (DEBUG, OPTIM, EDGE, CONCEPT, SCAFFOLDING) với unified template

---

### 2️⃣ llm_client.py

**TỪ (Old):**
```python
async def generate_problem(self, focus_area, context, difficulty):
    # LLM Call 1
    return problem_data

async def generate_teaching_response(self, focus_area, problem_data, difficulty):
    # LLM Call 2
    return teaching_response
```

**THÀNH (New):**
```python
async def generate_complete_record(
    self,
    focus_area: str,
    context: str,
    difficulty: str,
) -> Dict[str, Any]:
    """
    Gọi LLM 1 lần duy nhất để sinh toàn bộ dữ liệu
    """
    # Build prompt từ PROMPTS[focus_area]["unified"]
    template = PROMPTS[focus_area]["unified"]
    prompt = template.format(
        focus_area=focus_area,
        context=context,
        difficulty=difficulty,
        bug_type=random.choice(config.BUG_TYPES) if focus_area == "DEBUG_FOCUS" else "",
    )
    
    # 1 LLM call duy nhất
    messages = [{"role": "user", "content": prompt}]
    response = await self._call_api(messages, max_tokens=1500)
    
    # Parse JSON output
    json_str = self._extract_json(response)
    complete_data = json.loads(json_str)
    
    # Validate: Phải có 8 fields
    required_fields = [
        "problem_description",
        "buggy_code",
        "environment_feedback",
        "hidden_teacher_context",
        "diagnosis",
        "root_cause",
        "related_knowledge",
        "socratic_hint",
    ]
    
    for field in required_fields:
        if field not in complete_data:
            raise ValueError(f"Missing field: {field}")
    
    return complete_data
```

➡️ **Thực hiện:** Replace tất cả 2 method cũ bằng 1 method mới

---

### 3️⃣ data_formatter.py

**TỪ (Old):**
```python
def to_fine_tune_format(
    focus_area, context, difficulty,
    problem_data,      # Output 1 từ Stage 1
    teaching_response, # Output từ Stage 2
):
    return {
        "messages": [
            {"role": "system", "content": "Persona..."},
            {"role": "user", "content": f"Bối cảnh...\n{problem_data['buggy_code']}"},
            {"role": "assistant", "content": teaching_response}
        ]
    }
```

**THÀNH (New):**
```python
def to_fine_tune_format(
    focus_area: str,
    context: str,
    difficulty: str,
    complete_data: Dict[str, Any],  # Output từ 1 LLM call
) -> Dict[str, Any]:
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
                "content": (
                    f"{complete_data['diagnosis']}\n\n"
                    f"{complete_data['root_cause']}\n\n"
                    f"{complete_data['related_knowledge']}\n\n"
                    f"{complete_data['socratic_hint']}"
                )
            }
        ]
    }
```

➡️ **Thực hiện:** Update method signature + logic

---

### 4️⃣ generate_data.py

**TỪ (Old):**
```python
async def main():
    for i in range(num_records):
        # Stage 1: Generate problem
        problem_data = await llm.generate_problem(...)
        
        # Validate
        assert "buggy_code" in problem_data
        
        # Stage 2: Generate teaching
        teaching_response = await llm.generate_teaching(problem_data)
        
        # Format
        record = formatter.to_fine_tune_format(
            problem_data, teaching_response, focus_area
        )
        
        # Save
        storage.append_record(record)
```

**THÀNH (New):**
```python
async def main():
    for i in range(num_records):
        # 1 LLM call duy nhất - sinh toàn bộ
        complete_data = await llm.generate_complete_record(
            focus_area, context, difficulty
        )
        
        # Validate - check 8 required fields
        required_fields = [
            "problem_description", "buggy_code",
            "diagnosis", "socratic_hint",
            "environment_feedback", "hidden_teacher_context",
            "root_cause", "related_knowledge"
        ]
        assert all(field in complete_data for field in required_fields)
        
        # Format
        record = formatter.to_fine_tune_format(
            focus_area, context, difficulty, complete_data
        )
        
        # Save
        storage.append_record(record)
```

➡️ **Thực hiện:** Giảm 2 LLM calls xuống 1

---

### 5️⃣ config.py

**TỪ (Old):**
```python
TOKENS_PER_PROBLEM_GEN = 800      # LLM call 1
TOKENS_PER_TEACHING_GEN = 600     # LLM call 2
TOTAL_TOKENS_PER_RECORD = TOKENS_PER_PROBLEM_GEN + TOKENS_PER_TEACHING_GEN  # 1400
```

**THÀNH (New):**
```python
TOKENS_PER_UNIFIED_CALL = 1200    # Một lần call (problem + teaching)
TOTAL_TOKENS_PER_RECORD = TOKENS_PER_UNIFIED_CALL
```

---

## ✅ Verification Checklist

Sau khi thay đổi, kiểm tra:

- [ ] prompts.py có "unified" key cho tất cả 5 focus areas
- [ ] llm_client.py có method `generate_complete_record()`
- [ ] Method này return dict với 8 required fields
- [ ] data_formatter.py nhận `complete_data` parameter
- [ ] generate_data.py chỉ gọi LLM 1 lần per record
- [ ] config.py cập nhật token tracking
- [ ] Test với 2-3 records để verify output format

---

## 🚀 Lệnh Test

```bash
# Test với 3 records
python generate_data.py --num-records 3 --debug

# Xem structure output
python -c "
import json
with open('data.json', 'r', encoding='utf-8') as f:
    records = json.load(f)
    print(f'Total records: {len(records)}')
    print(f'First record messages: {[m[\"role\"] for m in records[0][\"messages\"]]}')
    print(f'Assistant message preview: {records[0][\"messages\"][2][\"content\"][:100]}...')
"
```

---

## 💡 Lợi Ích Của Thay Đổi

| Tiêu Chí | Old (2 calls) | New (1 call) |
|---------|---|---|
| **Latency** | 200-300ms | 100-150ms |
| **Tokens/record** | 1,400 | 1,200 |
| **Chi phí/100 records** | $0.42 | $0.36 |
| **Code complexity** | Complex | Simple |
| **Error handling** | Khó (2 stages) | Dễ (1 stage) |

---

## 📝 Công Việc Tiếp Theo

1. ✅ Cập nhật 5 file chính
2. ⬜ Test với 5-10 records
3. ⬜ Sinh 100+ records production
4. ⬜ Validate output quality
5. ⬜ Upload lên OpenAI để fine-tune
