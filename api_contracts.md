# API CONTRACTS

**Dự án:** CodeMentor AI  
**Phiên bản:** 1.1.0  
**Base URL:** `/api/v1`

---

## 1. Quy ước chung

### Auth

Tất cả endpoint trừ đăng nhập dùng header:

```http
Authorization: Bearer <access_token>
```

### Error response

```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "You do not have access to this class.",
    "trace_id": "tr_..."
  }
}
```

### Pagination

```json
{
  "items": [],
  "page": 1,
  "page_size": 20,
  "total": 132
}
```

---

## 2. Auth

### `POST /auth/login`

Request:

```json
{
  "email": "student@example.com",
  "password": "secret"
}
```

Response:

```json
{
  "access_token": "...",
  "refresh_token": "...",
  "user": {
    "id": "uuid",
    "role": "student",
    "full_name": "Nguyen Van A"
  }
}
```

### `POST /auth/refresh`

Request:

```json
{
  "refresh_token": "..."
}
```

Response:

```json
{
  "access_token": "..."
}
```

---

## 3. Classes

### `GET /classes`

Trả về danh sách lớp user có quyền xem.

Response:

```json
{
  "items": [
    {
      "id": "uuid",
      "name": "Nhập môn lập trình Python",
      "role": "student",
      "term": "2026-S1"
    }
  ]
}
```

### `POST /classes`

Role: `teacher`, `admin`

Request:

```json
{
  "name": "Nhập môn lập trình Python",
  "term": "2026-S1"
}
```

### `POST /classes/{class_id}/join`

Request:

```json
{
  "class_code": "PY101-A"
}
```

---

## 4. Assignments

### `GET /classes/{class_id}/assignments`

Query:

- `status=published|draft|closed`
- `type=coding|reverse_teaching`

Response:

```json
{
  "items": [
    {
      "id": "uuid",
      "title": "Tính giai thừa",
      "type": "coding",
      "difficulty": "easy",
      "deadline": "2026-05-30T23:59:00+07:00",
      "student_status": "not_started"
    }
  ]
}
```

### `GET /assignments/{assignment_id}`

Response:

```json
{
  "id": "uuid",
  "title": "Tính giai thừa",
  "description": "...",
  "type": "coding",
  "knowledge_tags": ["loops", "accumulator"],
  "hint_policy": {
    "max_hints_per_failed_submission": 5
  },
  "visible_test_cases": [
    {
      "input_data": "5",
      "expected_output": "120"
    }
  ]
}
```

### `POST /assignments`

Role: `teacher`, `ta`

Request:

```json
{
  "class_id": "uuid",
  "type": "coding",
  "title": "Tổng số chẵn",
  "description": "...",
  "knowledge_tags": ["loops", "arrays"],
  "difficulty": "easy",
  "test_cases": [
    {
      "input_data": "5\n1 2 3 4 5",
      "expected_output": "6",
      "is_hidden": false
    }
  ],
  "hint_policy": {
    "max_hints_per_failed_submission": 5
  }
}
```

---

## 5. Submissions

### `POST /submissions`

Role: `student`

Request:

```json
{
  "assignment_id": "uuid",
  "language": "python",
  "source_code": "n = int(input())\n..."
}
```

Response:

```json
{
  "submission_id": "uuid",
  "status": "wrong_answer",
  "passed_tests": 2,
  "total_tests": 5,
  "public_feedback": "Một số test chưa đúng.",
  "mentor_available": true,
  "thread_id": "mentor:student_id:assignment_id"
}
```

### `GET /submissions/{submission_id}`

Response:

```json
{
  "id": "uuid",
  "status": "accepted",
  "score": 100,
  "submitted_at": "2026-05-18T10:00:00+07:00",
  "judge_metadata": {
    "execution_time_ms": 120
  }
}
```

---

## 6. AI cho sinh viên

### `POST /ai/student/mentor`

Dùng khi submission fail trong VS Code.

Request:

```json
{
  "thread_id": "mentor:student_id:assignment_id",
  "submission_id": "uuid",
  "message": "Em không hiểu vì sao test 3 sai."
}
```

Response:

```json
{
  "message": "Bạn thử kiểm tra giá trị ban đầu của biến tích lũy. Với phép nhân, phần tử trung hòa là gì?",
  "scaffolding_level": 2,
  "hint_budget_remaining": 3,
  "policy_flags": {
    "no_code_leakage": true
  }
}
```

### `POST /ai/student/chat`

Dùng cho web dashboard sinh viên.

Request:

```json
{
  "message": "Mình đang yếu phần nào?",
  "class_id": "uuid"
}
```

Response:

```json
{
  "answer": "Bạn đang cần luyện thêm về mảng và vòng lặp lồng nhau...",
  "navigation_actions": [
    {
      "type": "open_assignment",
      "assignment_id": "uuid",
      "label": "Mở bài Mảng một chiều cơ bản"
    }
  ],
  "confidence": "high"
}
```

---

## 7. AI cho giảng viên

### `POST /ai/teacher/chat`

Request:

```json
{
  "class_id": "uuid",
  "message": "Tuần này lớp đang yếu phần nào nhất?"
}
```

Response:

```json
{
  "answer": "Trong 7 ngày gần nhất, nhóm kỹ năng arrays có hint density cao nhất...",
  "evidence": [
    {
      "type": "analytics_snapshot",
      "id": "uuid",
      "metric": "hint_density",
      "value": 3.4
    }
  ],
  "recommended_actions": [
    "Ôn lại index bắt đầu từ 0.",
    "Giao thêm bài luyện mảng một chiều mức dễ."
  ],
  "confidence": "high"
}
```

### `POST /ai/teacher/exercise-drafts`

Request:

```json
{
  "class_id": "uuid",
  "topic": "vòng lặp và mảng",
  "difficulty": "easy",
  "language": "python",
  "requirements": "Tạo bài có 2 visible tests và 3 hidden tests."
}
```

Response:

```json
{
  "draft_id": "uuid",
  "status": "needs_review",
  "draft_payload": {
    "title": "Tổng các số chẵn trong mảng",
    "description": "...",
    "test_cases": []
  },
  "validation_report": {
    "status": "passed_with_warnings",
    "warnings": ["Nên thêm edge case mảng rỗng nếu đề cho phép."]
  }
}
```

### `POST /exercise-drafts/{draft_id}/approve`

Request:

```json
{
  "publish": false,
  "review_notes": "Đã kiểm tra test cases."
}
```

Response:

```json
{
  "assignment_id": "uuid",
  "status": "draft"
}
```

---

## 8. Reverse Teaching

### `POST /reverse-teaching/sessions`

Role: `student`

Request:

```json
{
  "assignment_id": "uuid"
}
```

Response:

```json
{
  "session_id": "uuid",
  "thread_id": "reverse:student_id:assignment_id:session_id",
  "agent_message": "Tôi nghĩ range(n) chạy từ 1 đến n. Bạn hãy giải thích lại cho tôi bằng ví dụ n = 4."
}
```

### `POST /reverse-teaching/sessions/{session_id}/messages`

Request:

```json
{
  "message": "range(4) tạo ra 0, 1, 2, 3..."
}
```

Response:

```json
{
  "agent_message": "Nếu dùng các giá trị đó làm index cho mảng 4 phần tử, điều này giúp tránh lỗi gì?",
  "status": "in_progress",
  "rubric_progress": {
    "concept_accuracy": 2,
    "edge_case_awareness": 1
  }
}
```

### `GET /reverse-teaching/sessions/{session_id}`

Response:

```json
{
  "status": "completed",
  "final_score": 8,
  "rubric_scores": {
    "concept_accuracy": 2,
    "reasoning_clarity": 2,
    "misconception_handling": 2,
    "edge_case_awareness": 1,
    "teaching_quality": 1
  },
  "summary": "Sinh viên giải thích đúng range và index nhưng cần bổ sung edge case."
}
```

---

## 9. Analytics

### `GET /analytics/classes/{class_id}/overview`

Response:

```json
{
  "class_id": "uuid",
  "range": {
    "from": "2026-05-11",
    "to": "2026-05-18"
  },
  "completion_rate": 0.72,
  "average_attempts": 3.1,
  "hint_density": 2.4,
  "top_weak_tags": [
    {
      "tag": "arrays",
      "score": 0.41
    }
  ]
}
```

### `GET /analytics/students/{student_id}/profile`

Role: `teacher` within class scope or same `student_id`.

Response:

```json
{
  "student_id": "uuid",
  "mastery_map": {
    "loops": {
      "score": 0.62,
      "evidence_count": 11
    }
  },
  "common_pitfalls": [
    {
      "pattern": "off_by_one",
      "frequency": 6
    }
  ],
  "independence_score": 0.68
}
```

---

## 10. Admin

### `GET /admin/ai-audit-logs`

Role: `admin`

Query:

- `workflow`
- `user_id`
- `from`
- `to`

Response: paginated audit logs.

### `GET /admin/model-config`

Role: `admin`

Response:

```json
{
  "workflows": {
    "analyze_error": {
      "model": "debug-analyzer-v1",
      "fallback": "general-llm"
    },
    "teacher_insight": {
      "model": "general-llm"
    }
  }
}
```
