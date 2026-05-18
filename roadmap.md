# ROADMAP TRIỂN KHAI MVP 1.0

**Dự án:** CodeMentor AI  
**Mục tiêu:** đưa một MVP hoàn chỉnh ra pilot trong lớp lập trình nhập môn, sau đó mở rộng theo dữ liệu sử dụng thật.

---

## 1. Định hướng roadmap

Roadmap này không định nghĩa MVP như một bản thiếu tính năng. MVP 1.0 của CodeMentor AI đã bao gồm đủ product loop:

- VS Code Extension cho sinh viên.
- Teacher Web Dashboard.
- Student Web Dashboard.
- Chatbot web cho giảng viên.
- Chatbot web cho sinh viên.
- AI Exercise Drafting có review/approve.
- Reverse Teaching Exercise.
- Exam Mode có chatbot quota, scaffolding limit và integrity signals.
- Quick Challenge phát bài realtime về VS Code và tính điểm cộng.
- Analytics, guardrail, audit, security, testing và deployment.

Các phase bên dưới là thứ tự triển khai nội bộ để giảm rủi ro, không phải cắt bớt phạm vi sản phẩm.

---

## 2. Milestone 0: Product & Architecture Freeze

Mục tiêu: chốt tài liệu và contract để các team làm song song.

Deliverables:

- `README.md`
- `mvp_spec.md`
- `user_stories.md`
- `ui_ux_spec.md`
- `technical_architecture.md`
- `database.md`
- `api_contracts.md`
- `chatbot.md`
- `security_privacy.md`
- `testing_strategy.md`
- `deployment.md`
- `prompt_library.md`

Exit criteria:

- MVP definition được chốt.
- UI flow được chốt.
- API contract đủ cho frontend/extension mock.
- Database schema đủ cho migration đầu tiên.

---

## 3. Milestone 1: Core Platform

Mục tiêu: dựng nền backend, auth, database, lớp học và bài tập.

Scope:

- Auth/RBAC.
- User/class/class_members.
- Assignment CRUD.
- Test case CRUD.
- Database migrations.
- OpenAPI schema.
- Basic admin seed.

Exit criteria:

- Teacher tạo lớp và bài tập được.
- Student join lớp được.
- RBAC tests pass.
- API contract tests pass.

---

## 4. Milestone 2: Judge & VS Code Extension

Mục tiêu: sinh viên làm bài và nộp code từ IDE.

Scope:

- Judge worker cho Python.
- Submission lifecycle.
- VS Code login.
- Assignment tree.
- Submit current file.
- Submission result panel.
- Reflection prompt after pass.

Exit criteria:

- Student submit wrong/accepted code từ VS Code.
- Judge sandbox security tests pass.
- Extension không block editor.

---

## 5. Milestone 3: StudentMentorGraph

Mục tiêu: AI Mentor hỗ trợ debug an toàn khi submission fail.

Scope:

- LangGraph runtime.
- StudentMentorGraph nodes.
- Prompt library v1.
- No-code leakage guardrail.
- Chat threads/messages.
- Learning events.
- Hint budget.

Exit criteria:

- Submission fail tự mở Mentor chat.
- Hint không lộ lời giải trong regression suite.
- Learning event được lưu.
- Trace_id và audit log hoạt động.

---

## 6. Milestone 4: Teacher & Student Dashboards

Mục tiêu: web dashboard có giá trị product rõ cho hai vai trò chính.

Scope:

- Teacher overview dashboard.
- Student detail dashboard.
- Assignment insights.
- Student My Learning dashboard.
- Mastery map.
- Common pitfalls.
- Reflection history.
- Analytics snapshots.

Exit criteria:

- Teacher thấy completion, hint density, weak tags.
- Student thấy tiến độ và bài nên làm tiếp.
- Empty/loading/error states đầy đủ.

---

## 7. Milestone 5: Web Chatbots

Mục tiêu: giảng viên và sinh viên hỏi đáp trên web dựa trên dữ liệu thật.

Scope:

- TeacherInsightGraph.
- StudentCoachGraph.
- Evidence drawer.
- Navigation actions.
- Teacher query logs.
- Privacy guard.

Exit criteria:

- Teacher hỏi được tình trạng lớp/cá nhân với evidence.
- Student hỏi được tiến độ cá nhân và mở bài tập phù hợp.
- Out-of-scope data access bị chặn.

---

## 8. Milestone 6: AI Exercise Drafting

Mục tiêu: AI giúp tạo bài tập nhưng giảng viên giữ quyền kiểm duyệt.

Scope:

- ExerciseDraftGraph.
- Draft payload.
- Validation report.
- Draft version history.
- Review/edit/approve/reject UI.
- Publish assignment from approved draft.

Exit criteria:

- Teacher tạo draft từ prompt.
- Validation report hiển thị.
- Draft chỉ publish sau approval.
- Version history lưu thay đổi.

---

## 9. Milestone 7: Reverse Teaching

Mục tiêu: sinh viên chứng minh hiểu sâu bằng cách giảng lại cho agent.

Scope:

- Reverse teaching assignment config.
- ReverseTeachingGraph.
- Session UI.
- Rubric scoring.
- Transcript.
- Learning summary and mastery update candidate.

Exit criteria:

- Student hoàn thành một reverse session.
- Agent hỏi follow-up khi câu trả lời thiếu.
- Teacher xem rubric score và summary.

---

## 10. Milestone 8: Exam Mode & Quick Challenge

Mục tiêu: hỗ trợ kiểm tra có policy rõ ràng và hoạt động bài tập nhanh trên lớp.

Scope:

- Assessment Runtime.
- `assessment_sessions`, `assessment_participants`, `integrity_events`.
- Exam Mode setup UI.
- VS Code exam banner, countdown, chatbot quota.
- Integrity event ingestion.
- Quick Challenge launcher.
- Realtime notification to VS Code Extension.
- Live leaderboard and bonus points finalization.

Exit criteria:

- Teacher tạo và launch exam session.
- Student làm bài trong VS Code với policy hiển thị rõ.
- Chatbot quota/max scaffolding không bị bypass.
- Teacher launch quick challenge và leaderboard finalize đúng.

---

## 11. Milestone 9: Hardening & Pilot

Mục tiêu: đưa MVP vào pilot an toàn.

Scope:

- E2E demo script.
- AI regression suite.
- RBAC/security suite.
- Load smoke test.
- Monitoring dashboard.
- Backup/restore test.
- Pilot runbook.

Exit criteria:

- Release gates trong `testing_strategy.md` pass.
- Deployment checklist pass.
- Teacher/student pilot accounts ready.
- Rollback plan ready.

---

## 12. Post-MVP growth

Sau pilot, các hướng mở rộng:

- Fine-tune debug analyzer/safe hint adapter bằng dữ liệu thật đã ẩn danh.
- Hỗ trợ C/C++/Java.
- LMS integration.
- Parent/department-level reporting nếu cần.
- A/B testing scaffolding strategies.
- Advanced recommendation engine.
- Lockdown browser/native proctoring integration nếu tổ chức cần giám sát thi nghiêm ngặt hơn proctoring-lite.

---

## 13. Rủi ro và cách giảm thiểu

| Rủi ro | Ảnh hưởng | Giảm thiểu |
| :--- | :--- | :--- |
| AI lộ lời giải | Cao | Prompt policy, guardrail, regression, audit. |
| Dashboard thiếu giá trị | Cao | UI tập trung action, evidence, weak tags, intervention. |
| LangGraph phức tạp | Trung bình | Single orchestrated graph, typed state, node nhỏ. |
| Judge sandbox rủi ro | Cao | No-network, resource limit, process isolation. |
| Chatbot trả lời không evidence | Cao | Analytics snapshot, answer schema, evidence drawer. |
| AI draft sai test | Trung bình | Validation report, teacher approval, test preview. |
| Pilot quá tải vận hành | Trung bình | Monitoring, runbook, rollback, seed scripts. |
| Exam Mode bị hiểu là khóa tuyệt đối thiết bị | Cao | Tài liệu và UI dùng wording proctoring-lite, chỉ ghi nhận integrity signals trong phạm vi kỹ thuật cho phép. |
| Quick Challenge notification chậm | Trung bình | Realtime gateway, retry, fallback polling trong extension. |
