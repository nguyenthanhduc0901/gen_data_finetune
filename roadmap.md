# ROADMAP TRIỂN KHAI

**Dự án:** CodeMentor AI  
**Phiên bản:** 1.1.0

---

## 1. Mục tiêu roadmap

Roadmap này chia dự án thành các giai đoạn có thể triển khai, kiểm thử và demo được. Ưu tiên của dự án là hoàn thiện trải nghiệm học tập cốt lõi trước, sau đó mở rộng chatbot web và bài tập đảo ngược.

---

## 2. Phase 0: Chuẩn hóa tài liệu và quyết định nền tảng

Mục tiêu: thống nhất phạm vi sản phẩm và kiến trúc trước khi code.

Deliverables:

- PRD cập nhật.
- Architecture LangGraph mới.
- Database schema logic.
- User stories.
- API contracts.
- Roadmap.

Trạng thái: đã hoàn thành trong bộ tài liệu hiện tại.

Quyết định cần chốt tiếp:

- Framework frontend web.
- Cơ chế sandbox judge.
- Model provider và fallback.
- Chính sách lưu source code/chat logs.

---

## 3. Phase 1: MVP nền tảng học lập trình

Mục tiêu: sinh viên làm bài trong VS Code, nộp bài, nhận gợi ý AI khi fail; giảng viên xem dashboard cơ bản.

Scope:

- Auth và RBAC cơ bản.
- Class management.
- Assignment CRUD.
- Test case CRUD.
- Submission API.
- Judge Sandbox cho Python.
- VS Code Extension: login, assignment list, submit, mentor chat.
- StudentMentorGraph: analyze error, choose scaffolding, generate hint, guardrail.
- Database: users, classes, assignments, test_cases, submissions, chat_threads, chat_messages, learning_events.
- Teacher dashboard cơ bản: completion, attempts, hint density.

Không scope:

- AI tạo bài tập.
- Chatbot web cho giảng viên.
- Reverse Teaching.
- Fine-tune production model.

Success criteria:

- Sinh viên có thể hoàn thành một bài Python từ VS Code.
- Submission fail kích hoạt mentor chat.
- AI không lộ lời giải trong bộ test guardrail.
- Giảng viên xem được trạng thái lớp.

---

## 4. Phase 2: Web chatbot và analytics

Mục tiêu: giảng viên và sinh viên có chatbot web dựa trên dữ liệu thật.

Scope:

- Analytics snapshots.
- TeacherInsightGraph.
- StudentCoachGraph.
- Teacher chatbot trên dashboard lớp.
- Student learning dashboard.
- Student chatbot có navigation action.
- Hồ sơ năng lực: mastery map, common pitfalls, independence score.
- Teacher query logs và AI audit logs.

Success criteria:

- Giảng viên hỏi được tình trạng lớp và nhận câu trả lời có evidence.
- Sinh viên hỏi được tiến độ cá nhân và được điều hướng đến bài phù hợp.
- RBAC ngăn truy cập dữ liệu ngoài scope.

---

## 5. Phase 3: AI Exercise Drafting

Mục tiêu: AI hỗ trợ giảng viên tạo bài tập nhưng không tự publish.

Scope:

- ExerciseDraftGraph.
- `exercise_drafts`, `exercise_draft_versions`.
- UI tạo draft từ prompt.
- Validation report cho statement/test/rubric.
- Review, edit, approve, reject.
- Publish assignment từ draft approved.

Success criteria:

- AI tạo được draft bài coding hợp lệ.
- Giảng viên chỉnh sửa và approve được.
- Version history lưu đầy đủ.
- Draft không thể publish nếu chưa approve.

---

## 6. Phase 4: Reverse Teaching Exercise

Mục tiêu: thêm dạng bài tập đảo ngược để đánh giá năng lực giải thích.

Scope:

- Assignment type `reverse_teaching`.
- ReverseTeachingGraph.
- Rubric scoring.
- Reverse teaching session UI.
- Teacher view kết quả rubric và transcript.
- Cập nhật mastery map từ reverse summary.

Success criteria:

- Sinh viên hoàn thành một phiên Explain Back.
- Agent hỏi follow-up khi giải thích thiếu.
- Hệ thống tạo rubric score và learning summary.
- Giảng viên xem được kết quả.

---

## 7. Phase 5: Fine-tune và tối ưu AI

Mục tiêu: giảm chi phí/tăng chất lượng cho các node chuyên môn.

Scope:

- Dataset schema cho debug analyzer, safe hint, reverse scoring.
- Evaluation harness.
- Baseline report.
- Fine-tune adapter.
- Model routing trong LLM Gateway.
- Regression tests cho no-code leakage.

Success criteria:

- Root cause accuracy vượt baseline.
- JSON validity cao.
- No-code leakage thấp hơn ngưỡng policy.
- Có rollback plan.

---

## 8. Rủi ro chính

| Rủi ro | Ảnh hưởng | Giảm thiểu |
| :--- | :--- | :--- |
| AI lộ lời giải | Cao | Guardrail, hint policy, audit, review sample. |
| Judge sandbox không an toàn | Cao | Container isolation, no network, resource limits. |
| Analytics chậm | Trung bình | Snapshot, index, background jobs. |
| LangGraph quá phức tạp | Trung bình | Single orchestrated graph, node nhỏ, typed state. |
| AI tạo bài sai | Trung bình | Draft-only, validation, teacher approval. |
| Dữ liệu sinh viên nhạy cảm | Cao | RBAC, retention policy, audit, anonymization. |

---

## 9. Các tài liệu nên bổ sung sau roadmap này

- `security_privacy.md`: threat model, RBAC, retention, PII.
- `testing_strategy.md`: backend, frontend, judge, AI eval, e2e.
- `deployment.md`: Docker, env, migration, observability.
- `ui_ux_spec.md`: wireframe, navigation, states, empty/loading/error.
- `prompt_library.md`: prompt versioning và regression cases.
