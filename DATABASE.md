# TÀI LIỆU THIẾT KẾ CƠ SỞ DỮ LIỆU

**Dự án:** CodeMentor AI  
**Phiên bản:** 1.1.0  
**CSDL chính:** PostgreSQL  
**Ghi chú:** Các bảng dưới đây là schema logic phục vụ thiết kế. Tên field có thể được chuẩn hóa lại khi viết migration.

---

## 1. Quy ước chung

- Khóa chính ưu tiên `UUID`.
- Mọi bảng nghiệp vụ quan trọng nên có `created_at`, `updated_at`.
- Các enum nên được quản lý bằng migration rõ ràng.
- Dữ liệu AI linh hoạt dùng `JSONB`, nhưng các field cần query thường xuyên phải tách thành cột riêng.
- Không lưu raw prompt chứa dữ liệu nhạy cảm nếu không cần. Với audit, ưu tiên input summary và trace_id.

---

## 2. Người dùng, lớp học và phân quyền

### 2.1. `users`

| Trường | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | UUID, PK | ID người dùng. |
| `role` | enum | `student`, `teacher`, `ta`, `admin`. |
| `full_name` | varchar(150) | Họ tên hiển thị. |
| `email` | varchar(150), unique | Email đăng nhập. |
| `password_hash` | text | Mật khẩu đã hash. |
| `status` | enum | `active`, `invited`, `disabled`. |
| `last_login_at` | timestamptz | Lần đăng nhập gần nhất. |
| `created_at` | timestamptz | Thời gian tạo. |
| `updated_at` | timestamptz | Thời gian cập nhật. |

### 2.2. `classes`

| Trường | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | UUID, PK | ID lớp. |
| `teacher_id` | UUID, FK `users.id` | Giảng viên chính. |
| `name` | varchar(200) | Tên lớp. |
| `code` | varchar(50), unique | Mã mời vào lớp. |
| `term` | varchar(50) | Học kỳ/khóa. |
| `status` | enum | `active`, `archived`. |
| `created_at` | timestamptz | Thời gian tạo. |
| `updated_at` | timestamptz | Thời gian cập nhật. |

### 2.3. `class_members`

| Trường | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `class_id` | UUID, FK `classes.id` | Lớp. |
| `user_id` | UUID, FK `users.id` | Thành viên. |
| `member_role` | enum | `student`, `ta`, `teacher`. |
| `joined_at` | timestamptz | Thời gian tham gia. |

Khóa chính gợi ý: `(class_id, user_id)`.

---

## 3. Bài tập và nội dung học tập

### 3.1. `assignments`

| Trường | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | UUID, PK | ID bài tập. |
| `class_id` | UUID, FK `classes.id` | Lớp được giao. |
| `created_by` | UUID, FK `users.id` | Người tạo. |
| `source_draft_id` | UUID, nullable | Draft AI nếu bài được tạo từ AI. |
| `type` | enum | `coding`, `reverse_teaching`, `quiz`, `reading_reflection`. |
| `title` | varchar(200) | Tiêu đề. |
| `description` | text | Đề bài markdown. |
| `language_policy` | JSONB | Ngôn ngữ cho phép, version runtime. |
| `knowledge_tags` | JSONB | Tags kỹ năng. |
| `difficulty` | enum | `easy`, `medium`, `hard`. |
| `hint_policy` | JSONB | Hint budget, max level, cooldown. |
| `rubric` | JSONB | Rubric chấm điểm. |
| `time_limit_ms` | int | Giới hạn thời gian chạy. |
| `memory_limit_kb` | int | Giới hạn bộ nhớ. |
| `deadline` | timestamptz | Hạn nộp. |
| `status` | enum | `draft`, `published`, `closed`, `archived`. |
| `created_at` | timestamptz | Thời gian tạo. |
| `updated_at` | timestamptz | Thời gian cập nhật. |

### 3.2. `test_cases`

| Trường | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | UUID, PK | ID test case. |
| `assignment_id` | UUID, FK `assignments.id` | Bài tập. |
| `name` | varchar(100) | Tên test. |
| `input_data` | text | Input. |
| `expected_output` | text | Output mong đợi. |
| `is_hidden` | boolean | Test ẩn hay hiện. |
| `weight` | numeric | Trọng số. |
| `explanation` | text | Giải thích cho test hiện nếu cần. |
| `created_at` | timestamptz | Thời gian tạo. |

### 3.3. `reverse_teaching_configs`

| Trường | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `assignment_id` | UUID, PK/FK `assignments.id` | Bài reverse teaching. |
| `mode` | enum | `explain_back`, `agent_misconception`, `prompt_to_teach`, `diagnose_agent_answer`, `edge_case_interview`. |
| `scenario` | text | Tình huống agent đưa ra. |
| `agent_persona` | JSONB | Mức hiểu biết/hiểu lầm của agent. |
| `expected_concepts` | JSONB | Khái niệm cần xuất hiện. |
| `rubric` | JSONB | Rubric chi tiết. |
| `max_turns` | int | Số lượt hỏi đáp tối đa. |
| `created_at` | timestamptz | Thời gian tạo. |

---

## 4. Submission và Judge

### 4.1. `submissions`

| Trường | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | UUID, PK | ID submission. |
| `student_id` | UUID, FK `users.id` | Sinh viên nộp. |
| `assignment_id` | UUID, FK `assignments.id` | Bài tập. |
| `source_code` | text | Code nộp. |
| `language` | varchar(50) | Ngôn ngữ. |
| `status` | enum | `pending`, `accepted`, `wrong_answer`, `runtime_error`, `syntax_error`, `time_limit_exceeded`, `memory_limit_exceeded`, `judge_error`. |
| `passed_tests` | int | Số test pass. |
| `total_tests` | int | Tổng test. |
| `score` | numeric | Điểm nếu có. |
| `error_log` | text | Log lỗi tóm tắt. |
| `judge_metadata` | JSONB | Runtime, memory, container id, failed test summary. |
| `hints_used` | int | Số hint gắn với submission. |
| `submitted_at` | timestamptz | Thời điểm nộp. |
| `judged_at` | timestamptz | Thời điểm chấm xong. |

### 4.2. `submission_test_results`

| Trường | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | UUID, PK | ID kết quả. |
| `submission_id` | UUID, FK `submissions.id` | Submission. |
| `test_case_id` | UUID, nullable | Test case, null nếu không lộ hidden id. |
| `status` | enum | `passed`, `failed`, `skipped`, `error`. |
| `actual_output` | text | Output thực tế, có thể mask với hidden test. |
| `execution_time_ms` | int | Thời gian chạy. |
| `memory_used_kb` | int | Bộ nhớ dùng. |
| `public_feedback` | text | Feedback hiển thị cho sinh viên. |

---

## 5. Chat, LangGraph và learning events

### 5.1. `chat_threads`

| Trường | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | varchar(200), PK | Thread id LangGraph. |
| `thread_type` | enum | `mentor`, `teacher_insight`, `student_coach`, `exercise_draft`, `reverse_teaching`. |
| `user_id` | UUID, FK `users.id` | Người khởi tạo/chủ thread. |
| `class_id` | UUID, nullable | Scope lớp. |
| `assignment_id` | UUID, nullable | Scope bài tập. |
| `submission_id` | UUID, nullable | Scope submission. |
| `status` | enum | `open`, `resolved`, `closed`, `archived`. |
| `scaffolding_level` | int | Level hiện tại nếu là mentor. |
| `metadata` | JSONB | Context phụ. |
| `started_at` | timestamptz | Thời gian bắt đầu. |
| `last_activity_at` | timestamptz | Tương tác gần nhất. |

### 5.2. `chat_messages`

| Trường | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | UUID, PK | ID tin nhắn. |
| `thread_id` | varchar(200), FK `chat_threads.id` | Thread. |
| `sender_role` | enum | `student`, `teacher`, `ta`, `mentor`, `system`, `tool`. |
| `content` | text | Nội dung hiển thị. |
| `content_type` | enum | `text`, `markdown`, `json`, `navigation_action`. |
| `node_source` | varchar(100) | Node LangGraph sinh ra. |
| `policy_flags` | JSONB | Kết quả guardrail. |
| `created_at` | timestamptz | Thời gian gửi. |

### 5.3. `learning_events`

| Trường | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | UUID, PK | ID event. |
| `student_id` | UUID, FK `users.id` | Sinh viên. |
| `class_id` | UUID, FK `classes.id` | Lớp. |
| `assignment_id` | UUID, nullable | Bài liên quan. |
| `submission_id` | UUID, nullable | Submission liên quan. |
| `event_type` | enum | `submission_fail`, `submission_pass`, `hint_given`, `reflection_submitted`, `reverse_answer_scored`, `profile_updated`. |
| `knowledge_tags` | JSONB | Tags liên quan. |
| `payload` | JSONB | Dữ liệu event. |
| `created_at` | timestamptz | Thời điểm event. |

### 5.4. `learning_summaries`

| Trường | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | UUID, PK | ID summary. |
| `student_id` | UUID, FK `users.id` | Sinh viên. |
| `assignment_id` | UUID, FK `assignments.id` | Bài tập. |
| `struggle_time_mins` | int | Thời gian từ fail đầu đến pass/close. |
| `hint_count` | int | Số hint. |
| `common_errors` | JSONB | Lỗi gặp. |
| `concept_outcomes` | JSONB | Kết quả theo tag. |
| `ai_summary` | text | Tóm tắt cho giảng viên/sinh viên. |
| `generated_at` | timestamptz | Thời gian sinh. |

### 5.5. `user_ai_profiles`

| Trường | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `student_id` | UUID, PK/FK `users.id` | Sinh viên. |
| `mastery_map` | JSONB | Điểm kỹ năng 0-100 hoặc 0-1. |
| `common_pitfalls` | JSONB | Lỗi lặp lại. |
| `independence_score` | numeric | Mức tự lập. |
| `frustration_signals` | JSONB | Tín hiệu nản/khó khăn. |
| `learning_preferences` | JSONB | Cách học phù hợp. |
| `last_analyzed_at` | timestamptz | Lần cập nhật gần nhất. |

---

## 6. AI drafting và approval

### 6.1. `exercise_drafts`

| Trường | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | UUID, PK | ID draft. |
| `class_id` | UUID, FK `classes.id` | Lớp dự kiến. |
| `requested_by` | UUID, FK `users.id` | Giảng viên yêu cầu. |
| `prompt` | text | Yêu cầu của giảng viên. |
| `draft_payload` | JSONB | Đề, tests, rubric, tags. |
| `validation_report` | JSONB | Kết quả kiểm tra tự động. |
| `status` | enum | `draft`, `needs_review`, `approved`, `rejected`, `published`. |
| `review_notes` | text | Ghi chú review. |
| `approved_by` | UUID, nullable | Người approve. |
| `approved_at` | timestamptz | Thời gian approve. |
| `created_at` | timestamptz | Thời gian tạo. |
| `updated_at` | timestamptz | Thời gian cập nhật. |

### 6.2. `exercise_draft_versions`

| Trường | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | UUID, PK | Version id. |
| `draft_id` | UUID, FK `exercise_drafts.id` | Draft. |
| `version_number` | int | Số version. |
| `payload` | JSONB | Nội dung version. |
| `changed_by` | UUID, FK `users.id` | AI hoặc user chỉnh sửa. |
| `change_summary` | text | Tóm tắt thay đổi. |
| `created_at` | timestamptz | Thời gian tạo. |

---

## 7. Reverse Teaching sessions

### 7.1. `reverse_teaching_sessions`

| Trường | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | UUID, PK | ID session. |
| `assignment_id` | UUID, FK `assignments.id` | Bài reverse. |
| `student_id` | UUID, FK `users.id` | Sinh viên. |
| `thread_id` | varchar(200), FK `chat_threads.id` | Thread chat. |
| `status` | enum | `in_progress`, `completed`, `abandoned`. |
| `turn_count` | int | Số lượt hỏi đáp. |
| `final_score` | numeric | Điểm rubric. |
| `rubric_scores` | JSONB | Điểm từng tiêu chí. |
| `summary` | text | Tóm tắt năng lực giải thích. |
| `started_at` | timestamptz | Bắt đầu. |
| `completed_at` | timestamptz | Kết thúc. |

---

## 8. Analytics và chatbot logs

### 8.1. `analytics_snapshots`

| Trường | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | UUID, PK | ID snapshot. |
| `scope_type` | enum | `class`, `assignment`, `student`. |
| `scope_id` | UUID | ID tương ứng. |
| `metric_date` | date | Ngày snapshot. |
| `metrics` | JSONB | Metric tổng hợp. |
| `generated_at` | timestamptz | Thời gian tạo. |

### 8.2. `teacher_ai_queries`

| Trường | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | UUID, PK | ID query. |
| `teacher_id` | UUID, FK `users.id` | Giảng viên. |
| `class_id` | UUID, nullable | Scope lớp. |
| `question` | text | Câu hỏi. |
| `answer` | text | Câu trả lời. |
| `evidence_refs` | JSONB | Dẫn chứng nội bộ. |
| `confidence` | enum | `high`, `medium`, `low`. |
| `created_at` | timestamptz | Thời gian hỏi. |

### 8.3. `ai_audit_logs`

| Trường | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | UUID, PK | ID log. |
| `trace_id` | varchar(100) | Trace chung của request. |
| `workflow` | varchar(100) | Tên workflow. |
| `user_id` | UUID, FK `users.id` | Người gọi. |
| `model_name` | varchar(100) | Model dùng. |
| `input_summary` | JSONB | Tóm tắt input đã giảm nhạy cảm. |
| `output_summary` | JSONB | Tóm tắt output. |
| `policy_flags` | JSONB | Guardrail result. |
| `latency_ms` | int | Độ trễ. |
| `token_usage` | JSONB | Token/cost nếu có. |
| `created_at` | timestamptz | Thời gian tạo. |

---

## 9. Cấu trúc JSON khuyến nghị

### 9.1. `mastery_map`

```json
{
  "syntax_basics": { "score": 0.86, "evidence_count": 18 },
  "loops": { "score": 0.62, "evidence_count": 11 },
  "arrays": { "score": 0.41, "evidence_count": 7 },
  "recursion": { "score": 0.18, "evidence_count": 2 }
}
```

### 9.2. `common_pitfalls`

```json
[
  {
    "pattern": "off_by_one",
    "knowledge_tags": ["loops", "arrays"],
    "frequency": 6,
    "last_seen": "2026-05-18T09:00:00+07:00",
    "resolved_trend": "improving"
  }
]
```

### 9.3. `hint_policy`

```json
{
  "max_hints_per_failed_submission": 5,
  "max_scaffolding_level": 4,
  "cooldown_after_budget_exhausted_minutes": 5,
  "allow_parallel_examples": true,
  "allow_code_snippets": false
}
```

### 9.4. `draft_payload`

```json
{
  "title": "Tổng các số chẵn trong mảng",
  "type": "coding",
  "description": "...",
  "knowledge_tags": ["loops", "arrays", "conditions"],
  "difficulty": "easy",
  "test_cases": [
    {
      "input_data": "5\n1 2 3 4 5",
      "expected_output": "6",
      "is_hidden": false
    }
  ],
  "rubric": {
    "correctness": 70,
    "edge_cases": 20,
    "code_quality": 10
  }
}
```

---

## 10. Index khuyến nghị

- `users(email)`
- `class_members(class_id, user_id)`
- `assignments(class_id, status, deadline)`
- `submissions(student_id, assignment_id, submitted_at)`
- `learning_events(student_id, event_type, created_at)`
- `analytics_snapshots(scope_type, scope_id, metric_date)`
- `chat_threads(user_id, thread_type, last_activity_at)`
- `teacher_ai_queries(teacher_id, class_id, created_at)`

---

## 11. Những điểm cần quyết định khi triển khai

- Có lưu raw source code lâu dài không, hay chỉ lưu với retention policy?
- Hidden test output có được lưu trong `submission_test_results.actual_output` hay luôn mask?
- Mastery score dùng thang 0-1 hay 0-100 trong code implementation?
- Analytics snapshot refresh theo event, theo lịch, hay hybrid?
- Có cần row-level security ở PostgreSQL hay enforce hoàn toàn ở application layer?
