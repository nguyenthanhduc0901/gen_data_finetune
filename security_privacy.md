# SECURITY & PRIVACY SPECIFICATION

**Dự án:** CodeMentor AI  
**Mục tiêu:** bảo vệ dữ liệu sinh viên, code submission, lớp học và hành vi AI trong MVP 1.0.

---

## 1. Security principles

- Least privilege theo role và class scope.
- Không tin input từ user, code, comment hoặc prompt.
- Sandbox mọi code execution.
- AI output phải qua guardrail trước khi hiển thị.
- Audit mọi workflow AI quan trọng.
- Dữ liệu nhạy cảm cần retention policy rõ.

---

## 2. Data classification

| Loại dữ liệu | Mức nhạy cảm | Ví dụ | Chính sách |
| :--- | :--- | :--- | :--- |
| Public course metadata | Thấp | Tên bài, tags đã publish | User trong lớp được xem. |
| Student identity | Cao | Tên, email, class membership | RBAC nghiêm ngặt. |
| Source code | Cao | Code submission | Chỉ student, teacher/TA cùng lớp. |
| Hidden tests | Rất cao | Input/output test ẩn | Không hiển thị cho student. |
| Chat transcript | Cao | Mentor chat, teacher chat | Scope theo user/class. |
| Integrity events | Cao | Paste, focus lost, window blur signals | Chỉ teacher/TA/admin có quyền trong lớp. |
| AI audit | Cao | Trace, policy flags | Admin/authorized engineer. |
| Analytics aggregate | Trung bình | Completion rate, weak tags | Teacher/TA cùng lớp. |

---

## 3. RBAC matrix

| Resource | Student | Teacher | TA | Admin |
| :--- | :--- | :--- | :--- | :--- |
| Own profile | Read | Read if same class | Read if assigned | Read |
| Other student profile | No | Read if same class | Read if assigned | Read |
| Class dashboard | No | Read/write own class | Read assigned class | Read |
| Assignment draft | No | CRUD own class | Create/review if allowed | Read |
| Publish assignment | No | Yes | Optional permission | Yes |
| Hidden tests | No | Read/write own class | Read/write if allowed | Read |
| AI audit logs | No | Own class limited | Own class limited | Full |
| Integrity report | Own signals only | Own class | Assigned class | Full |
| Model config | No | No | No | CRUD |

---

## 4. Threat model

| Threat | Scenario | Mitigation |
| :--- | :--- | :--- |
| Prompt injection | Sinh viên viết comment "ignore previous instructions". | Treat code as data, system prompt priority, guardrail. |
| Code exfiltration | Code submission cố truy cập network/file system. | Sandbox no-network, resource limit, filesystem isolation. |
| Hidden test leakage | AI nhắc expected output hidden. | Do not pass hidden raw output to mentor response, guardrail. |
| Cross-class data leak | Teacher hỏi chatbot về sinh viên lớp khác. | Scope check before retrieval. |
| Over-permissive AI draft | AI tạo bài có lời giải trong hint. | Draft validation and teacher review. |
| Audit data leakage | Logs lưu raw PII/prompt quá nhiều. | Masking, retention, access control. |
| Exam mode overclaim | Sản phẩm hứa khóa tab/OS tuyệt đối nhưng extension không kiểm soát được toàn bộ môi trường. | Proctoring-lite wording, signal logging, policy transparency. |
| Chatbot abuse in exam | Sinh viên dùng chatbot quá quota hoặc nhận hint sâu hơn policy. | Session quota, max scaffolding level, policy guard before LLM call. |

---

## 5. Sandbox policy

- Network disabled by default.
- CPU/time/memory limit per language.
- Read-only runtime image.
- Per-submission temp directory.
- Kill process tree after timeout.
- Store only public feedback for student.
- Hidden test actual output masked unless teacher view.

MVP Python limits:

| Resource | Value |
| :--- | :--- |
| CPU time | 2s default, configurable per assignment |
| Memory | 128MB default |
| Wall time | 5s |
| Network | Disabled |
| File write | Temp directory only |

---

## 6. AI guardrails

### Input guardrails

- Strip or isolate code comments as untrusted content.
- Limit context size.
- Mask PII not needed for task.
- Validate user role and scope before retrieval.

### Output guardrails

- No full solution for active assignments.
- No hidden test disclosure.
- No unauthorized personal data.
- No unsupported claims in teacher analytics.
- Regenerate or refuse if violation detected.
- In Exam Mode/Quick Challenge, enforce session policy before model invocation.

---

## 7. Exam integrity policy

Exam Mode và Quick Challenge dùng cơ chế **integrity signals**, không tự động kết luận gian lận nếu không có quy định học vụ. Các signal gồm:

- Paste detected.
- Focus lost/window blur.
- Focus returned.
- Chat quota exceeded.
- Late submit.
- Manual flag by teacher/TA.

Nguyên tắc:

- Sinh viên phải thấy integrity notice trước khi bắt đầu.
- Sự kiện phải có timestamp, session_id, event_type, severity.
- Payload không lưu nội dung clipboard đầy đủ; chỉ lưu metadata như char_count và file_name.
- Giảng viên xem report theo ngôn ngữ trung tính: "signals", "warnings", "needs review".
- Policy không hứa khóa tuyệt đối tab/browser/OS. Extension chỉ ghi nhận những tín hiệu có thể quan sát trong phạm vi VS Code và app.

---

## 8. Privacy and retention

MVP retention defaults:

| Data | Retention |
| :--- | :--- |
| User account | Until account deletion or admin disable. |
| Submission source code | Course duration + 180 days. |
| Submission metadata | Course duration + 2 years aggregate. |
| Chat transcript | Course duration + 180 days. |
| AI audit logs | 180 days. |
| Integrity events | Course duration + 180 days. |
| Analytics snapshots | 2 years aggregate. |
| Hidden tests | Until assignment deletion/archive policy. |

Deletion:

- Student deletion anonymizes analytics where possible.
- Source code and chat transcripts are deleted or anonymized by policy.
- Audit logs may keep trace metadata without content for security.

---

## 9. Audit requirements

Every AI workflow logs:

- `trace_id`
- workflow name
- user_id
- role
- class_id/assignment_id if present
- model name
- policy flags
- session_id for exam/quick challenge workflows
- latency
- token usage if available
- input/output summary with sensitive data masked

---

## 10. Security acceptance checklist

- Every API endpoint has auth middleware.
- Every class-scoped endpoint checks membership/role.
- Hidden tests never appear in student API responses.
- Judge sandbox blocks network.
- AI mentor regression suite has zero critical code leakage.
- Teacher chatbot cannot answer outside class scope.
- Audit logs are visible only to authorized roles.
- Exam/Quick Challenge chatbot quota cannot be bypassed by direct API calls.
- Integrity event payload does not store raw clipboard content.
