# ĐÁNH GIÁ BỘ TÀI LIỆU DỰ ÁN

**Dự án:** CodeMentor AI  
**Ngày rà soát:** 2026-05-18  
**Kết luận ngắn:** Trước khi bổ sung, tài liệu ở mức ý tưởng tốt nhưng chưa đủ chi tiết để triển khai đồng bộ. Sau khi cập nhật, bộ docs đã có PRD, architecture, chatbot spec, database, user stories, API và roadmap.

---

## 1. Mức độ chi tiết trước khi chỉnh

| Hạng mục | Mức cũ | Nhận xét |
| :--- | :--- | :--- |
| Tầm nhìn sản phẩm | Trung bình | Có định hướng AI Mentor rõ, nhưng thiếu phạm vi web chatbot và student dashboard. |
| Tính năng | Thấp đến trung bình | Nêu feature ở mức headline, thiếu acceptance criteria và priority. |
| User story | Thiếu | Chưa có file riêng, chưa mô tả vai trò, hành vi, điều kiện hoàn thành. |
| LangGraph | Trung bình nhưng hơi phức tạp | Có node cơ bản, nhưng đang nghiêng multi-agent trong khi MVP chưa cần. |
| Database | Trung bình | Có bảng lõi, thiếu reverse teaching, exercise drafting, analytics snapshot, audit. |
| API | Thiếu | Chưa có contract endpoint/request/response. |
| Chatbot web | Thiếu | Chưa có chatbot giảng viên/sinh viên trên web. |
| AI safety | Thấp | Có no-code rule nhưng thiếu guardrail, privacy, audit, evaluation. |
| Roadmap | Thiếu | Chưa có thứ tự MVP/V1/rủi ro. |
| Fine-tune | Trung bình | Có pipeline nhưng chưa gắn rõ vào kiến trúc sản phẩm và policy. |

---

## 2. Dự án còn thiếu file gì

Trước khi cập nhật, repo chỉ có:

- `README.md`
- `technical_architecture.md`
- `chatbot.md`
- `database.md`
- `finetune_gemma.md`

Các file còn thiếu để một dự án tài liệu sản phẩm/kỹ thuật đầy đủ hơn:

| File cần có | Trạng thái sau cập nhật | Lý do cần |
| :--- | :--- | :--- |
| `docs_audit.md` | Đã thêm | Ghi lại đánh giá mức độ chi tiết, thiếu sót và quyết định bổ sung. |
| `user_stories.md` | Đã thêm | Làm rõ nhu cầu theo vai trò, acceptance criteria, priority. |
| `api_contracts.md` | Đã thêm | Giúp frontend, backend, extension và AI runtime tích hợp thống nhất. |
| `roadmap.md` | Đã thêm | Chia MVP/V1/V2, giảm mơ hồ khi triển khai. |
| `security_privacy.md` | Chưa thêm | Nên có file riêng khi bước vào implementation vì dữ liệu sinh viên và code rất nhạy cảm. |
| `deployment.md` | Chưa thêm | Cần cho Docker, env, migration, observability, CI/CD. |
| `testing_strategy.md` | Chưa thêm | Cần cho unit/integration/e2e/AI evaluation. |
| `ui_ux_spec.md` | Chưa thêm | Cần nếu bắt đầu thiết kế màn hình chi tiết. |
| `data_retention_policy.md` | Chưa thêm | Cần quyết định lưu code/chat/log bao lâu. |

---

## 3. Những phần đã bổ sung vào file hiện có

### `README.md`

- Viết lại thành PRD rõ hơn.
- Bổ sung web chatbot cho giảng viên và sinh viên.
- Bổ sung AI Exercise Drafting và luồng approve.
- Bổ sung Reverse Teaching Exercise.
- Bổ sung KPI và trạng thái hoàn thiện tính năng.
- Bổ sung bản đồ tài liệu.

### `technical_architecture.md`

- Thiết kế lại LangGraph theo hướng **Single Orchestrated Graph + Specialized Routes**.
- Tách workflow: StudentMentor, TeacherInsight, StudentCoach, ExerciseDraft, ReverseTeaching.
- Bổ sung state schema, data flow, security và khuyến nghị MVP.

### `chatbot.md`

- Mở rộng thành spec AI đầy đủ.
- Bổ sung chatbot giảng viên, chatbot sinh viên, chatbot tạo bài tập.
- Bổ sung Reverse Teaching, rubric, prompt policy, guardrail, memory update.

### `database.md`

- Bổ sung role `ta`.
- Bổ sung `assignment.type`, `hint_policy`, `rubric`.
- Bổ sung `reverse_teaching_configs`, `reverse_teaching_sessions`.
- Bổ sung `exercise_drafts`, `exercise_draft_versions`.
- Bổ sung `learning_events`, `analytics_snapshots`, `teacher_ai_queries`, `ai_audit_logs`.

### `finetune_gemma.md`

- Chuyển từ tài liệu fine-tune rời rạc sang tài liệu tích hợp model vào sản phẩm.
- Bổ sung task safe hint, reverse scoring, exercise draft support.
- Bổ sung evaluation, model routing và rủi ro policy.

---

## 4. Tính năng đã hoàn thiện chưa?

Theo góc nhìn tài liệu: **chưa hoàn thiện trước bản cập nhật này**. Các thiếu sót chính là:

- Chưa mô tả chatbot web cho giảng viên.
- Chưa mô tả chatbot web cho sinh viên.
- Chưa có bài tập đảo ngược.
- Chưa có user story chi tiết.
- Chưa có API contract.
- Kiến trúc LangGraph còn có xu hướng phức tạp hơn mức cần thiết.
- Database chưa đủ bảng để vận hành AI drafting, approval, reverse teaching và analytics.

Sau cập nhật này, tài liệu đã đủ tốt để bước sang giai đoạn thiết kế UI, viết migration, dựng API skeleton và prototype LangGraph.

---

## 5. Khuyến nghị tiếp theo

1. Thêm `security_privacy.md` trước khi lưu dữ liệu code/chat thật.
2. Thêm `testing_strategy.md` trước khi triển khai AI guardrail.
3. Thêm `ui_ux_spec.md` khi bắt đầu thiết kế màn hình.
4. Bổ sung bài báo gốc về Reverse Teaching vào repo hoặc trích dẫn cụ thể để cập nhật thuật ngữ/rubric chính xác hơn.
