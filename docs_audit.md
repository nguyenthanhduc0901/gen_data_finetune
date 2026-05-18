# ĐÁNH GIÁ & HOÀN THIỆN BỘ TÀI LIỆU DỰ ÁN

**Dự án:** CodeMentor AI  
**Ngày rà soát:** 2026-05-18  
**Kết luận:** Bộ tài liệu hiện được chuẩn hóa theo hướng **MVP 1.0 hoàn chỉnh**, đủ để team product, design, backend, frontend, extension và AI cùng triển khai một pilot thật.

---

## 1. Mức độ chi tiết hiện tại

| Hạng mục | Mức hiện tại | Nhận xét |
| :--- | :--- | :--- |
| PRD | Hoàn chỉnh cho MVP | Có persona, pain point, scope, feature set, Exam Mode, Quick Challenge, KPI và định nghĩa MVP. |
| User stories | Hoàn chỉnh cho MVP | Có epic theo từng vai trò, acceptance criteria và priority. |
| UI/UX | Hoàn chỉnh cho MVP | Có IA, màn hình, layout, component, Exam/Challenge UI, state, responsive và VS Code extension. |
| Architecture | Hoàn chỉnh cho MVP | Thiết kế LangGraph đơn giản, có workflow rõ cho mentor, dashboard chatbot, exercise drafting, reverse teaching. |
| Database | Hoàn chỉnh cho MVP | Bao phủ user/class/assignment/submission/chat/memory/draft/reverse/exam/quick challenge/analytics/audit. |
| API | Hoàn chỉnh cho MVP | Có contract cho web, extension, AI workflows, analytics. |
| AI/Chatbot | Hoàn chỉnh cho MVP | Có prompt policy, guardrail, memory update, chatbot giảng viên/sinh viên, Reverse Teaching. |
| Security/Privacy | Hoàn chỉnh cho MVP | Có RBAC, threat model, data scope, retention, audit. |
| Testing | Hoàn chỉnh cho MVP | Có test pyramid và AI evaluation. |
| Deployment | Hoàn chỉnh cho MVP | Có môi trường, service topology, CI/CD, observability. |
| Fine-tune | Sẵn sàng sau MVP | Đã định nghĩa vai trò model fine-tune và evaluation, không chặn MVP. |

---

## 2. Bộ tài liệu cuối cùng cần có

| File | Trạng thái | Vai trò |
| :--- | :--- | :--- |
| `README.md` | Đã có | PRD tổng quan và bản đồ tài liệu. |
| `mvp_spec.md` | Đã có | Định nghĩa MVP 1.0 hoàn chỉnh và tiêu chí nghiệm thu. |
| `user_stories.md` | Đã có | User stories và acceptance criteria. |
| `ui_ux_spec.md` | Đã có | Thiết kế UI cho từng user và VS Code extension. |
| `technical_architecture.md` | Đã có | Kiến trúc hệ thống và LangGraph. |
| `database.md` | Đã có | Schema logic PostgreSQL. |
| `api_contracts.md` | Đã có | API request/response. |
| `chatbot.md` | Đã có | AI Mentor, chatbot, Reverse Teaching và guardrail. |
| `security_privacy.md` | Đã có | Bảo mật, phân quyền, dữ liệu, audit. |
| `testing_strategy.md` | Đã có | Chiến lược kiểm thử và AI evaluation. |
| `deployment.md` | Đã có | Triển khai, CI/CD, observability. |
| `prompt_library.md` | Đã có | Prompt lõi, versioning, regression cases. |
| `finetune_gemma.md` | Đã có | Fine-tune và model routing sau MVP. |
| `roadmap.md` | Đã có | Lộ trình pilot và mở rộng. |

---

## 3. Nhận định product

CodeMentor AI có đủ nền tảng để trở thành một sản phẩm mạnh vì giải quyết cả ba lớp giá trị:

1. **Giá trị cho sinh viên:** học bằng cách tự debug, nhận gợi ý đúng lúc, xem tiến độ cá nhân, làm bài đảo ngược để chứng minh hiểu sâu.
2. **Giá trị cho giảng viên:** nhìn thấy tình trạng lớp theo dữ liệu quá trình, hỏi chatbot để ra quyết định nhanh, tạo bài tập nháp bằng AI nhưng vẫn giữ quyền kiểm duyệt.
3. **Giá trị vận hành:** có schema, API, audit, security, testing, deployment và model strategy rõ ràng.

Điểm mạnh nhất của sản phẩm là không định vị AI như công cụ làm hộ, mà như một **learning intelligence layer** nằm giữa IDE, bài tập, dashboard và dữ liệu học tập.

---

## 4. Những quyết định đã chốt trong docs

- MVP 1.0 gồm cả VS Code extension, teacher web, student web, chatbot hai phía, AI exercise drafting và Reverse Teaching.
- MVP 1.0 gồm Exam Mode và Quick Challenge như hai năng lực classroom/assessment chính thức.
- LangGraph không triển khai multi-agent tự trị trong MVP; dùng workflow graph có state và route rõ ràng.
- AI tạo bài tập chỉ tạo draft; giảng viên approve mới publish.
- Chatbot giảng viên trả lời dựa trên evidence và analytics snapshot.
- Chatbot sinh viên chỉ truy cập dữ liệu của chính sinh viên đó.
- Reverse Teaching là assignment type chính thức, không phải demo chat phụ.
- Guardrail, audit và privacy là yêu cầu MVP, không phải phần bổ sung sau.
- Exam Mode dùng proctoring-lite: ghi nhận integrity signals trong phạm vi VS Code/app, không hứa khóa tuyệt đối toàn bộ hệ điều hành.

---

## 5. Phần có thể mở rộng sau MVP

Những phần dưới đây không làm MVP thiếu hoàn chỉnh, mà là hướng tăng trưởng:

- Fine-tune model theo dữ liệu thật sau pilot.
- Thêm ngôn ngữ C/C++/Java với sandbox riêng.
- Tích hợp LMS như Moodle/Canvas/Google Classroom.
- Hệ thống khuyến nghị learning path dài hạn.
- A/B testing các chiến lược scaffolding.
- Báo cáo cấp khoa/trường thay vì chỉ cấp lớp.
