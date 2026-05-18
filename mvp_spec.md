# MVP 1.0 SPECIFICATION

**Dự án:** CodeMentor AI  
**Mục tiêu:** mô tả MVP hoàn chỉnh có thể pilot trong một lớp lập trình nhập môn.

---

## 1. Định nghĩa MVP 1.0

MVP 1.0 là phiên bản sản phẩm đủ để một giảng viên dùng CodeMentor AI cho một lớp học thật trong một học phần ngắn. MVP bao gồm đầy đủ chu trình:

1. Giảng viên tạo lớp và bài tập.
2. Sinh viên nhận bài trong VS Code.
3. Sinh viên nộp code và được judge tự động.
4. AI Mentor hỗ trợ khi fail mà không đưa lời giải.
5. Giảng viên xem dashboard lớp và từng sinh viên.
6. Giảng viên hỏi chatbot về tình trạng lớp/cá nhân.
7. Sinh viên xem dashboard cá nhân và hỏi chatbot về tiến độ.
8. Giảng viên dùng AI tạo bài tập nháp và approve.
9. Sinh viên làm bài Reverse Teaching để chứng minh hiểu sâu.
10. Hệ thống lưu learning events, analytics, audit và profile năng lực.

---

## 2. MVP modules

| Module | Bắt buộc MVP | Kết quả người dùng |
| :--- | :--- | :--- |
| Auth/RBAC | Có | User đăng nhập đúng vai trò. |
| Class Management | Có | Giảng viên tạo lớp, sinh viên tham gia. |
| Assignment Management | Có | Giảng viên tạo/giao bài coding và reverse teaching. |
| Judge Sandbox | Có | Sinh viên nộp code và nhận kết quả. |
| VS Code Extension | Có | Sinh viên làm bài ngay trong IDE. |
| AI Mentor | Có | Sinh viên nhận hint khi fail. |
| Teacher Dashboard | Có | Giảng viên xem tình trạng lớp và cá nhân. |
| Student Dashboard | Có | Sinh viên xem tiến độ cá nhân. |
| Teacher Chatbot | Có | Giảng viên hỏi đáp dựa trên dữ liệu lớp. |
| Student Chatbot | Có | Sinh viên hỏi tiến độ và được điều hướng. |
| AI Exercise Drafting | Có | Giảng viên tạo draft, review, approve. |
| Reverse Teaching | Có | Sinh viên giải thích lại cho agent và được chấm rubric. |
| Analytics Snapshot | Có | Dashboard/chatbot phản hồi nhanh và có evidence. |
| Audit/Guardrail | Có | AI an toàn, kiểm tra được. |

---

## 3. MVP personas và quyền

| Vai trò | Quyền chính | Không được |
| :--- | :--- | :--- |
| Student | Xem lớp của mình, làm bài, nộp bài, chat với mentor, xem dashboard cá nhân. | Xem dữ liệu sinh viên khác, hidden test, analytics lớp. |
| Teacher | Quản lý lớp/bài tập, xem dashboard lớp/sinh viên, hỏi chatbot, approve draft. | Xem lớp không phụ trách, publish draft chưa review. |
| TA | Xem dashboard, hỗ trợ review submission/chat, tạo draft nếu được cấp quyền. | Thay đổi cấu hình hệ thống. |
| Admin | Quản lý user, policy, audit, model config. | Can thiệp điểm học tập nếu không có quy trình. |

---

## 4. MVP success journey

### 4.1. Teacher success journey

1. Đăng nhập web.
2. Tạo lớp `Nhập môn lập trình Python`.
3. Mời sinh viên bằng class code.
4. Tạo bài coding thủ công hoặc bằng AI draft.
5. Review test case/rubric và publish.
6. Theo dõi dashboard sau khi sinh viên nộp bài.
7. Hỏi chatbot: "Lớp đang yếu phần nào nhất?"
8. Mở hồ sơ một sinh viên đang kẹt.
9. Tạo một bài Reverse Teaching để kiểm tra hiểu sâu.
10. Dùng insight để chuẩn bị buổi học tiếp theo.

### 4.2. Student success journey

1. Đăng nhập VS Code Extension.
2. Chọn lớp và bài tập.
3. Viết code, submit.
4. Nếu fail, nhận hint Socratic.
5. Sửa code, submit lại đến khi pass.
6. Gửi reflection ngắn.
7. Mở web dashboard cá nhân.
8. Hỏi chatbot: "Mình nên làm bài nào tiếp?"
9. Làm Reverse Teaching để giải thích lại khái niệm.
10. Thấy mastery map được cập nhật.

---

## 5. MVP feature acceptance

### 5.1. VS Code Extension

- Login hoạt động với token.
- Sidebar hiển thị lớp, bài tập, deadline, trạng thái.
- Submit code từ file hiện tại.
- Hiển thị kết quả judge.
- Chat panel mở khi fail.
- Chat lưu lịch sử theo assignment.
- Khi hết hint budget, AI dừng hỗ trợ trực tiếp.

### 5.2. Teacher Web

- Dashboard lớp có completion rate, average attempts, hint density, weak tags.
- Bảng sinh viên có status, progress, independence score.
- Hồ sơ sinh viên có mastery map, pitfalls, learning summaries.
- Chatbot trả lời có evidence.
- Exercise Builder tạo được coding assignment.
- AI Draft tạo bài tập nháp và luồng approve hoạt động.

### 5.3. Student Web

- Dashboard hiển thị bài cần làm, deadline, mastery map, lỗi hay gặp.
- Chatbot trả lời theo dữ liệu cá nhân.
- Chatbot có navigation action đến bài tập.
- Reflection history hiển thị theo bài.

### 5.4. Reverse Teaching

- Giảng viên tạo assignment type `reverse_teaching`.
- Sinh viên bắt đầu session và trao đổi với agent.
- Agent hỏi follow-up khi câu trả lời thiếu evidence.
- Hệ thống chấm rubric và lưu summary.
- Giảng viên xem được kết quả.

---

## 6. Product quality bar

| Tiêu chí | Ngưỡng MVP |
| :--- | :--- |
| Uptime pilot | 99% trong giờ học thử nghiệm. |
| Submission feedback | < 10 giây cho bài Python cơ bản. |
| AI first response | < 8 giây nếu không stream, < 2 giây đến token đầu nếu stream. |
| No-code leakage | 0 lỗi nghiêm trọng trong regression suite trước release. |
| Teacher chatbot evidence | 100% câu trả lời phân tích có evidence hoặc nói rõ thiếu dữ liệu. |
| RBAC | 100% endpoint có kiểm tra quyền. |
| Audit | 100% AI workflow có trace_id. |

---

## 7. Demo script MVP

1. Admin tạo giảng viên và sinh viên mẫu.
2. Giảng viên tạo lớp.
3. Sinh viên join lớp.
4. Giảng viên dùng AI tạo bài "Tổng số chẵn trong mảng".
5. Giảng viên review và publish.
6. Sinh viên mở VS Code, thấy bài, nộp code sai.
7. AI Mentor đưa hint không lộ lời giải.
8. Sinh viên sửa và pass.
9. Dashboard lớp cập nhật.
10. Giảng viên hỏi chatbot về lỗi phổ biến.
11. Sinh viên hỏi chatbot web bài tiếp theo.
12. Sinh viên hoàn thành Reverse Teaching.

---

## 8. Non-functional requirements

- Backend API có OpenAPI schema.
- Database migration versioned.
- Sandbox không có network outbound.
- Logs có trace_id xuyên suốt API, Judge và AI.
- UI có loading, empty, error states.
- Frontend responsive cho desktop và tablet; student web dùng được trên mobile.
- Extension không block editor khi đang submit.
- Dữ liệu nhạy cảm được mask trong audit.

---

## 9. MVP release checklist

- PRD và user stories đã chốt.
- UI/UX spec đã chốt.
- API contract đã chốt.
- Database migration đã khớp schema logic.
- Guardrail regression pass.
- E2E demo script pass.
- Teacher và student pilot accounts sẵn sàng.
- Monitoring dashboard sẵn sàng.
- Rollback plan sẵn sàng.
