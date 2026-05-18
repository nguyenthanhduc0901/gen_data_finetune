# USER STORIES & ACCEPTANCE CRITERIA

**Dự án:** CodeMentor AI  
**Phiên bản:** 1.1.0  
**Quy ước ưu tiên:** MVP, V1, V2

---

## 1. Epic A: Sinh viên làm bài trong VS Code

### US-A1: Đăng nhập extension

**Là** sinh viên, **tôi muốn** đăng nhập trong VS Code Extension, **để** xem bài tập của các lớp mình tham gia.

Acceptance criteria:

- Sinh viên đăng nhập bằng email/password hoặc token do web cấp.
- Extension lưu access token an toàn theo cơ chế của VS Code.
- Nếu token hết hạn, extension yêu cầu đăng nhập lại.
- Sinh viên chỉ thấy lớp mà mình là thành viên.

Priority: MVP

### US-A2: Xem danh sách bài tập

**Là** sinh viên, **tôi muốn** xem danh sách bài tập trong sidebar, **để** biết bài nào cần làm và trạng thái hiện tại.

Acceptance criteria:

- Danh sách hiển thị title, deadline, status, số lần nộp.
- Có filter theo lớp và trạng thái.
- Bài quá hạn được đánh dấu rõ.
- Click vào bài mở mô tả bài trong panel.

Priority: MVP

### US-A3: Nộp bài từ VS Code

**Là** sinh viên, **tôi muốn** nộp file code hiện tại, **để** hệ thống chấm tự động.

Acceptance criteria:

- Sinh viên chọn bài tập và ngôn ngữ trước khi nộp.
- Extension gửi source_code, language, assignment_id.
- Backend trả trạng thái pending/accepted/failed.
- Nếu judge lỗi hệ thống, sinh viên thấy thông báo không tính là fail học tập.

Priority: MVP

### US-A4: Nhận gợi ý khi submission fail

**Là** sinh viên, **tôi muốn** AI Mentor tự mở khi bài fail, **để** được hướng dẫn debug.

Acceptance criteria:

- Chat chỉ tự mở khi submission fail.
- AI biết đề bài, code, error log, failed tests được phép hiển thị.
- Phản hồi không chứa lời giải hoàn chỉnh.
- Mỗi hint được lưu với level và submission_id.
- Khi hết hint budget, AI yêu cầu sinh viên thử lại/tạm dừng.

Priority: MVP

### US-A5: Reflection sau khi pass

**Là** sinh viên, **tôi muốn** ghi lại lỗi mình vừa sửa, **để** củng cố kiến thức.

Acceptance criteria:

- Sau submission accepted, extension/web nhắc reflection ngắn.
- Reflection được lưu vào learning_events.
- AI có thể dùng reflection để cập nhật learning summary.
- Sinh viên có thể bỏ qua nếu giảng viên không bắt buộc.

Priority: V1

---

## 2. Epic B: Giảng viên quản lý lớp và bài tập

### US-B1: Tạo lớp

**Là** giảng viên, **tôi muốn** tạo lớp và mời sinh viên, **để** quản lý bài tập theo lớp.

Acceptance criteria:

- Giảng viên tạo class name, term.
- Hệ thống sinh class code duy nhất.
- Sinh viên join bằng class code.
- Giảng viên có thể thêm trợ giảng.

Priority: MVP

### US-B2: Tạo bài tập thủ công

**Là** giảng viên, **tôi muốn** tạo bài tập kèm test case, **để** giao cho lớp.

Acceptance criteria:

- Bài có title, description, difficulty, tags.
- Có visible và hidden test cases.
- Có hint policy.
- Bài ở trạng thái draft trước khi publish.
- Không thể publish nếu thiếu test case tối thiểu.

Priority: MVP

### US-B3: Xem dashboard lớp

**Là** giảng viên, **tôi muốn** xem dashboard lớp, **để** biết lớp đang học như thế nào.

Acceptance criteria:

- Hiển thị completion rate, average attempts, hint density.
- Hiển thị knowledge gaps theo tags.
- Cho phép lọc theo bài, thời gian, nhóm sinh viên.
- Dữ liệu dashboard lấy từ analytics_snapshots hoặc query đã tối ưu.

Priority: MVP

### US-B4: Xem hồ sơ sinh viên

**Là** giảng viên, **tôi muốn** xem hồ sơ năng lực từng sinh viên, **để** hỗ trợ cá nhân hóa.

Acceptance criteria:

- Hiển thị mastery map, common pitfalls, independence score.
- Có lịch sử bài đã làm và lỗi thường gặp.
- Có learning summaries theo assignment.
- Không dùng ngôn ngữ quy kết tiêu cực.

Priority: MVP

---

## 3. Epic C: Chatbot web cho giảng viên

### US-C1: Hỏi tình trạng chung của lớp

**Là** giảng viên, **tôi muốn** hỏi chatbot về tình trạng chung của lớp, **để** nắm nhanh điểm yếu và ưu tiên giảng lại.

Acceptance criteria:

- Chatbot trả lời dựa trên class_id hiện tại.
- Câu trả lời có evidence: metric, khoảng thời gian, số submission.
- Có đề xuất hành động.
- Nếu thiếu dữ liệu, chatbot nói rõ không đủ dữ liệu.

Priority: V1

### US-C2: Hỏi về một sinh viên cụ thể

**Là** giảng viên, **tôi muốn** hỏi chatbot về một sinh viên cụ thể, **để** biết sinh viên đó đang kẹt ở đâu.

Acceptance criteria:

- Chatbot chỉ trả lời nếu sinh viên thuộc lớp của giảng viên.
- Trả lời gồm tiến độ, lỗi lặp lại, hint usage, bài đang kẹt.
- Có đề xuất can thiệp phù hợp.
- Không hiển thị source code đầy đủ nếu không cần.

Priority: V1

### US-C3: Đề xuất nội dung ôn tập

**Là** giảng viên, **tôi muốn** chatbot đề xuất nội dung ôn tập, **để** chuẩn bị buổi học tiếp theo.

Acceptance criteria:

- Đề xuất dựa trên top weak tags.
- Có danh sách bài tập liên quan.
- Có lý do vì sao nên ôn chủ đề đó.
- Giảng viên có thể tạo draft bài tập từ đề xuất.

Priority: V1

### US-C4: AI tạo bài tập nháp

**Là** giảng viên, **tôi muốn** AI tạo bài tập nháp, **để** tiết kiệm thời gian soạn nội dung.

Acceptance criteria:

- Giảng viên nhập chủ đề, độ khó, ngôn ngữ, số test case.
- AI tạo title, statement, examples, test cases, tags, rubric.
- Draft có validation_report.
- Draft không được publish khi chưa approve.

Priority: V1

### US-C5: Review và approve bài tập AI

**Là** giảng viên, **tôi muốn** review và approve draft do AI tạo, **để** kiểm soát chất lượng trước khi giao.

Acceptance criteria:

- Giảng viên chỉnh sửa mọi phần của draft.
- Hệ thống lưu version history.
- Approve tạo assignment ở trạng thái draft hoặc published theo lựa chọn.
- Reject yêu cầu nhập lý do hoặc ghi chú.

Priority: V1

---

## 4. Epic D: Chatbot web cho sinh viên

### US-D1: Hỏi tiến độ cá nhân

**Là** sinh viên, **tôi muốn** hỏi chatbot về tình trạng học tập của mình, **để** biết nên cải thiện gì.

Acceptance criteria:

- Chatbot chỉ dùng dữ liệu của sinh viên đang đăng nhập.
- Trả lời mastery map bằng ngôn ngữ dễ hiểu.
- Có gợi ý bài nên làm tiếp.
- Không so sánh cá nhân với bạn học khác nếu không có policy cho phép.

Priority: V1

### US-D2: Điều hướng đến bài tập

**Là** sinh viên, **tôi muốn** chatbot đưa tôi đến bài tập phù hợp, **để** học tiếp nhanh hơn.

Acceptance criteria:

- Câu trả lời có navigation_action.
- Link mở đúng assignment.
- Nếu bài chưa publish hoặc không thuộc lớp, link không hiển thị.
- Chatbot giải thích lý do chọn bài đó.

Priority: V1

### US-D3: Xem lại lỗi thường gặp

**Là** sinh viên, **tôi muốn** xem lại lỗi mình hay mắc, **để** tránh lặp lại.

Acceptance criteria:

- Chatbot liệt kê common pitfalls theo tags.
- Có ví dụ mô tả lỗi ở mức khái niệm, không phơi toàn bộ code cũ nếu policy không cho.
- Có gợi ý cách tự kiểm tra trước khi nộp.

Priority: V1

---

## 5. Epic E: Reverse Teaching Exercise

### US-E1: Làm bài dạng Explain Back

**Là** sinh viên, **tôi muốn** giải thích lại thuật toán cho agent, **để** chứng minh mình hiểu bài.

Acceptance criteria:

- Assignment có type `reverse_teaching`.
- Agent hỏi theo scenario và expected_concepts.
- Sinh viên trả lời bằng text.
- Hệ thống chấm rubric và lưu summary.

Priority: V1

### US-E2: Agent hỏi lại khi sinh viên giải thích thiếu

**Là** sinh viên, **tôi muốn** agent hỏi lại điểm tôi giải thích chưa rõ, **để** tôi hoàn thiện reasoning.

Acceptance criteria:

- Nếu rubric chưa đủ evidence, agent hỏi follow-up.
- Số lượt hỏi không vượt `max_turns`.
- Follow-up tập trung vào điểm thiếu, không đổi chủ đề.
- Kết thúc khi đủ evidence hoặc hết lượt.

Priority: V1

### US-E3: Giảng viên xem kết quả Reverse Teaching

**Là** giảng viên, **tôi muốn** xem rubric và summary của bài đảo ngược, **để** biết sinh viên có hiểu sâu không.

Acceptance criteria:

- Hiển thị final_score, rubric_scores, summary.
- Có transcript nếu giảng viên có quyền.
- Có tags được cập nhật vào mastery map.

Priority: V1

---

## 6. Epic F: Admin, safety và audit

### US-F1: Audit tương tác AI

**Là** admin, **tôi muốn** xem audit log của AI, **để** điều tra lỗi và kiểm soát policy.

Acceptance criteria:

- Mỗi request AI có trace_id.
- Lưu workflow, user, model, latency, policy_flags.
- Không lưu dữ liệu nhạy cảm vượt policy.
- Có filter theo workflow, user, ngày.

Priority: V1

### US-F2: Cấu hình model routing

**Là** admin, **tôi muốn** cấu hình model cho từng workflow, **để** cân bằng chất lượng và chi phí.

Acceptance criteria:

- Có config model theo workflow/node.
- Có fallback model.
- Có rate limit.
- Thay đổi config được audit.

Priority: V2

---

## 7. Definition of Done

Một tính năng được coi là xong khi:

- Có API hoặc UI behavior rõ ràng.
- Có kiểm tra quyền truy cập.
- Có test tối thiểu cho backend logic.
- Có audit/log cho tương tác AI quan trọng.
- Có guardrail nếu output AI hiển thị cho người dùng.
- Có cập nhật tài liệu nếu thay đổi contract hoặc schema.
