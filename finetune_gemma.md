# TÀI LIỆU KỸ THUẬT: FINE-TUNING GEMMA CHO CODE DEBUGGING & AI MENTOR

**Dự án:** CodeMentor AI  
**Phiên bản:** 1.1.0  
**Mục tiêu:** định nghĩa vai trò của mô hình fine-tune trong hệ thống, pipeline huấn luyện/evaluation và cách kiểm soát rủi ro khi đưa model vào AI Mentor.

---

## 1. Vai trò của mô hình fine-tune

Mô hình fine-tune không nên được dùng như chatbot duy nhất cho toàn hệ thống. Trong kiến trúc CodeMentor AI, model fine-tune phù hợp nhất cho các tác vụ chuyên môn hẹp:

- Phân loại lỗi lập trình.
- Định vị vùng code nghi ngờ.
- Sinh phân tích root cause nội bộ.
- Đánh giá lời giải thích của sinh viên trong Reverse Teaching.
- Gợi ý test case hoặc misconception khi tạo bài tập nháp.
- Sinh hint an toàn trong Exam Mode với `max_scaffolding_level` và `allowed_hint_types` bị giới hạn.

Các tác vụ cần tính an toàn, quyền dữ liệu và truy vấn database vẫn phải đi qua LangGraph workflow, guardrail và backend policy.

---

## 2. Tác vụ huấn luyện

| Task | Tên | Input | Output | Metric |
| :--- | :--- | :--- | :--- | :--- |
| T1 | Bug Localization | Đề bài, code lỗi, log/test fail | Dòng/vùng nghi ngờ | Accuracy/F1 |
| T2 | Bug Identification | Code lỗi, log | Loại lỗi và concept tag | Accuracy/F1 |
| T3 | Root Cause Explanation | Code lỗi, failed test | JSON root cause nội bộ | Human/LLM-as-judge + schema validity |
| T4 | Safe Hint Generation | Root cause, hint level | Gợi ý không lộ lời giải | Policy pass rate + helpfulness |
| T5 | Reverse Explanation Scoring | Câu hỏi, câu trả lời sinh viên, rubric | Điểm rubric JSON | Correlation với human score |
| T6 | Exercise Draft Support | Chủ đề, độ khó | Draft đề/test/rubric | Teacher approval rate |
| T7 | Assessment-safe Hinting | Root cause, assessment policy | Hint không vượt quota/mức gợi ý | Policy compliance |

Lưu ý: nếu dùng benchmark như DebugEval hoặc COAST, cần ghi rõ version dataset, split, ngày chạy, script evaluation và commit hash. Các kết quả trong tài liệu chỉ có giá trị khi có artifact tái lập.

---

## 3. Dữ liệu huấn luyện

### 3.1. Nguồn dữ liệu

- Public benchmark về code debugging.
- Submission lỗi đã được ẩn danh.
- Chat mentor đã được giảng viên/TA review.
- Bài tập và rubric do giảng viên tạo.
- Reverse Teaching sessions đã được chấm.

### 3.2. Quy tắc dữ liệu

- Ẩn danh `student_id`, email, tên riêng.
- Không đưa hidden test case nhạy cảm vào dữ liệu sinh hint trực tiếp nếu có nguy cơ lộ.
- Tách dữ liệu dùng để phân tích nội bộ và dữ liệu dùng để sinh phản hồi cho sinh viên.
- Gắn nhãn policy violation cho các mẫu "đưa lời giải quá mức".

### 3.3. Format mẫu cho root cause

```json
{
  "instruction": "Analyze the student's code and failed tests. Return JSON only.",
  "input": {
    "assignment_summary": "Compute factorial of n.",
    "student_code": "...",
    "failed_tests": [
      {
        "input": "5",
        "expected": "120",
        "actual": "0"
      }
    ],
    "error_log": ""
  },
  "output": {
    "error_type": "wrong_answer",
    "root_cause": "accumulator initialized to 0 for multiplication",
    "concept_tags": ["loops", "accumulator"],
    "suspicious_lines": [3],
    "confidence": 0.86
  }
}
```

### 3.4. Format mẫu cho safe hint

```json
{
  "instruction": "Generate a Socratic hint without revealing the solution.",
  "input": {
    "root_cause": "accumulator initialized incorrectly",
    "hint_level": 2,
    "student_profile": {
      "independence_score": 0.72,
      "common_pitfalls": ["wrong_accumulator_initialization"]
    }
  },
  "output": {
    "message": "Bạn thử tự hỏi: với phép nhân lặp lại, giá trị ban đầu nên là phần tử trung hòa nào?",
    "policy_tags": ["no_solution", "concept_probe"]
  }
}
```

---

## 4. Pipeline fine-tune

### 4.1. Training approach

- Dùng SFT cho structured outputs và safe hint style.
- Dùng QLoRA nếu phần cứng hạn chế.
- Tách adapter theo tác vụ nếu dữ liệu khác biệt lớn:
  - `debug_analyzer_adapter`
  - `safe_hint_adapter`
  - `reverse_scoring_adapter`
- Không trộn dữ liệu code repair trực tiếp với dữ liệu mentor nếu output repair làm tăng nguy cơ model đưa lời giải.

### 4.2. Cấu hình QLoRA tham khảo

| Tham số | Giá trị khởi điểm |
| :--- | :--- |
| Quantization | 4-bit NF4 |
| Compute dtype | bfloat16 nếu GPU hỗ trợ |
| LoRA rank | 16 hoặc 32 |
| LoRA alpha | 32 hoặc 64 |
| Target modules | q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj |
| Learning rate | 1e-4 đến 2e-4 |
| Epochs | 2-4, tùy overfit |
| Max sequence length | Theo độ dài code/log thực tế |

### 4.3. Validation trong training

- Schema validity: output JSON parse được.
- Policy validity: không chứa lời giải hoàn chỉnh khi task là hint.
- Task accuracy: phân loại/định vị đúng.
- Regression set: các ca prompt injection và yêu cầu "cho đáp án".

---

## 5. Evaluation

### 5.1. Bộ chỉ số bắt buộc

| Nhóm | Metric | Ngưỡng mong muốn trước production |
| :--- | :--- | :--- |
| Structured output | JSON validity | > 98% |
| Debug | Root cause accuracy | > baseline ít nhất 10% |
| Hint safety | No-code policy pass | > 99% |
| Hint usefulness | Teacher/TA rating | >= 4/5 trên sample |
| Reverse Teaching | Rubric correlation | >= 0.7 với human score |
| Robustness | Prompt injection pass | > 98% |

### 5.2. Human review

Mỗi version model cần review thủ công ít nhất:

- 50 phản hồi hint.
- 30 phân tích root cause.
- 30 bài Reverse Teaching scoring.
- 20 draft bài tập/test case.
- 20 phản hồi hint trong Exam Mode/Quick Challenge với quota và scaffolding limit.
- 20 ca adversarial/prompt injection.

### 5.3. Báo cáo kết quả

Mỗi lần chạy evaluation cần lưu:

- Model base và adapter version.
- Dataset version.
- Script/commit hash.
- Hardware/runtime.
- Bảng metric.
- Sample lỗi nghiêm trọng.
- Quyết định: promote, hold, rollback.

---

## 6. Tích hợp vào LangGraph

### 6.1. Model routing

| Workflow | Model đề xuất | Lý do |
| :--- | :--- | :--- |
| `analyze_error` | fine-tune debug analyzer | Cần hiểu code/log. |
| `generate_hint` | general LLM + guardrail hoặc safe-hint adapter | Cần tone sư phạm và an toàn. |
| `teacher_insight` | general LLM | Cần tổng hợp dữ liệu/evidence. |
| `exercise_draft` | general LLM + validation | Cần sáng tạo có kiểm soát. |
| `reverse_scoring` | reverse scoring adapter hoặc general LLM rubric | Cần đánh giá lời giải thích. |

### 6.2. Không dùng model fine-tune để bypass policy

Ngay cả khi model fine-tune trả lời tốt, output vẫn phải đi qua:

- Schema validator.
- No-code leakage guard.
- Privacy guard.
- Audit log.
- Fallback nếu confidence thấp.

---

## 7. Rủi ro và biện pháp

| Rủi ro | Biện pháp |
| :--- | :--- |
| Model học cách sửa code hoàn chỉnh rồi lộ lời giải | Tách adapter repair và mentor; guardrail output. |
| Dataset chứa thông tin cá nhân | Anonymization pipeline và review sample. |
| Overfit benchmark | Giữ test set nội bộ theo bài tập thật. |
| JSON không ổn định | Constrained decoding hoặc repair parser có giới hạn. |
| Scoring Reverse Teaching thiên lệch | Human calibration, rubric rõ, sample review. |
| Chi phí inference cao | Routing chỉ dùng fine-tune ở node cần thiết. |

---

## 8. Bước tiếp theo

1. Xác định base model thật sự được dùng và version chính xác.
2. Chuẩn hóa dataset schema cho 6 task.
3. Viết evaluation harness có thể chạy lại.
4. Tạo bộ adversarial tests cho no-code leakage.
5. Chạy baseline trước khi fine-tune.
6. Chỉ đưa model vào production sau khi có báo cáo evaluation đầy đủ.
