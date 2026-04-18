# TÀI LIỆU TỔNG QUAN SẢN PHẨM (PRD)
**Tên dự án:** CodeMentor AI
**Phiên bản tài liệu:** 1.0.0
**Loại sản phẩm:** VS Code Extension & Web Dashboard
**Công nghệ lõi AI:** LangGraph (Stateful Multi-Agent), LLM.

---

## 1. Tóm tắt Dự án (Executive Summary)
**CodeMentor AI** không phải là một công cụ sinh mã (Code Generator) như GitHub Copilot. Nó là một **Trợ lý Sư phạm (AI Mentor)** được tích hợp trực tiếp vào VS Code. 
Sản phẩm hoạt động theo nguyên lý "Thụ động" (Passive Intervention) và phương pháp "Socratic & Scaffolding". Chatbot chỉ can thiệp khi học sinh nộp bài và gặp lỗi từ hệ thống chấm (Judge). Thay vì cung cấp lời giải, hệ thống sử dụng bộ nhớ dài hạn (Long-term Memory) để hiểu trình độ học sinh, từ đó đưa ra các câu hỏi gợi mở, giúp học sinh tự tư duy và sửa lỗi.

## 2. Vấn đề & Giải pháp (Problem & Solution)
### Vấn đề (Pain points)
* **Với Học sinh:** Quá lạm dụng ChatGPT/Copilot. Khi gặp lỗi, thói quen copy-paste toàn bộ code lên AI để lấy đáp án khiến tư duy logic và kỹ năng debug bị thui chột.
* **Với Giáo viên:** Giao bài tập trên các nền tảng truyền thống nhưng mù tịt về quá trình làm bài của học sinh. Không biết học sinh mất bao lâu để giải, kẹt ở dòng code nào, hay mắc lỗi tư duy cơ bản nào.

### Giải pháp
* **Chặn đứt luồng copy-paste:** Tích hợp thẳng danh sách bài tập và công cụ chat vào VS Code.
* **Ép buộc "va chạm":** Chatbot bị "khoá" cho đến khi học sinh thực sự viết code và chạy thử ra lỗi.
* **Cá nhân hóa:** Chatbot ghi nhớ các lỗi sai trong quá khứ để nhắc nhở và điều chỉnh độ khó của gợi ý (Hint Level).

---

## 3. Chân dung Người dùng (User Personas)

### Persona 1: Học sinh / Sinh viên (End-user)
* **Mục tiêu:** Hoàn thành bài tập, hiểu rõ bản chất của ngôn ngữ lập trình, nâng cao kỹ năng fix bug.
* **Nỗi đau:** Đọc log báo lỗi của compiler không hiểu gì. Dễ nản khi nộp bài sai quá 5 lần.
* **Hành vi mong muốn:** Tự tin hơn khi đọc lỗi, biết cách dùng "Rubber Ducking" để phân tích code.

### Persona 2: Giáo viên / Trợ giảng (Admin/Manager)
* **Mục tiêu:** Đánh giá đúng năng lực thực sự của học sinh, thiết kế bài tập phù hợp với trình độ chung của lớp.
* **Nỗi đau:** Chấm bài thủ công, không biết học sinh tự làm hay chép code mạng.
* **Hành vi mong muốn:** Xem Dashboard báo cáo xem câu nào học sinh phải xin gợi ý nhiều nhất để hôm sau lên lớp giảng lại phần đó.

---

## 4. Tính năng Cốt lõi (Core Features)

### 4.1. Phía VS Code Extension (Dành cho Học sinh)
* **F1: Danh sách bài tập tích hợp:** Fetch danh sách bài tập từ server hiển thị trên Sidebar của VS Code.
* **F2: Nộp bài & Bắt lỗi (Auto-Trigger):** Tích hợp nút `Submit Code`. Extension tự động gửi code đến Judge System. Nếu có lỗi (Syntax, Runtime, Logic), tự động kích hoạt Chatbot.
* **F3: Socratic Chat Interface:** Chatbot sẽ điều hướng cuộc hội thoại dựa trên Scaffolding Level.
* **F4: Ngữ cảnh tự động (Context Binding):** Chatbot tự động biết học sinh đang làm bài nào, code hiện tại là gì và log lỗi ra sao mà không cần học sinh phải copy-paste vào khung chat.

### 4.2. Phía Web Application (Dành cho Giáo viên)
* **F5: Quản lý Bài tập (Exercise Builder):** Tạo bài tập, viết mô tả, cấu hình Test Cases (Input/Expected Output), và thiết lập "Tags" kiến thức (VD: Vòng lặp, Đệ quy).
* **F6: Mentor Dashboard (Báo cáo Phân tích):**
    * **Báo cáo lớp học:** Tỉ lệ hoàn thành bài tập, biểu đồ "Điểm mù kiến thức" (những tag kiến thức mà lớp sai nhiều nhất).
    * **Báo cáo cá nhân:** "Hồ sơ năng lực" của từng học sinh (được LangGraph phân tích và lưu ở Long-term Memory). Hiển thị: Mức độ tự lập (Independence Score), Lỗi hay mắc phải (Recurring Errors).

---

## 5. Luồng Trải nghiệm Người dùng (User Flows)

### Luồng Học sinh làm bài:
1. Mở VS Code -> Click vào icon Extension CodeMentor.
2. Đăng nhập -> Chọn Bài tập "Tính giai thừa".
3. Học sinh viết file `main.py` -> Nhấn nút `Submit`.
4. Hệ thống báo lỗi: `Failed Test Case: Expected 120, Actual 0`.
5. Màn hình Chatbot tự động pop-up: *"Hệ thống báo sai kết quả rồi kìa. Bạn thử kiểm tra lại giá trị khởi tạo ban đầu của biến tính tổng xem sao?"*
6. Học sinh chat qua lại với bot tối đa 3 lần.
7. Học sinh tự sửa `sum = 0` thành `sum = 1` -> Nộp lại -> `Passed`.
8. Chatbot khen ngợi: *"Tuyệt! Nhớ nhé, phép nhân thì giá trị khởi tạo phải là 1."* -> LangGraph ngầm lưu trạng thái "Đã hiểu khởi tạo biến" vào Database.

### Luồng Giáo viên quản lý:
1. Giáo viên đăng nhập nền tảng Web.
2. Vào trang Dashboard lớp "Nhập môn Lập trình".
3. Hệ thống cảnh báo: *"Có 70% học sinh kẹt ở bài tập Mảng 2 chiều và phải dùng tối đa số lượt gợi ý của AI."*
4. Giáo viên xem lại lịch sử chat của 1 học sinh tiêu biểu để xem AI đã gợi ý như thế nào và học sinh bí ở đâu.

---

## 6. Yêu cầu Hệ thống (System Constraints & Rules)
* **Rule 1: No Code Spillage (Chống lộ code):** System Prompt của LLM phải được set ở mức nghiêm ngặt cao nhất, cấm tuyệt đối việc in ra quá 2 dòng code liên tiếp mang tính giải pháp.
* **Rule 2: Hint Budget (Ngân sách gợi ý):** Mỗi học sinh chỉ được AI trả lời tối đa 5 lần cho một lần nộp lỗi. Hết 5 lần, AI yêu cầu: *"Bạn hãy thử suy nghĩ thêm 5 phút hoặc xem lại slide bài giảng rồi nộp lại code nhé."*
* **Rule 3: Trạng thái Đồ thị (Graph State):** Hệ thống phải duy trì `thread_id` (để theo dõi lịch sử chat của 1 bài tập) và `user_id` (để truy xuất hồ sơ năng lực dài hạn).

---

## 7. Chỉ số Đo lường Thành công (Key Success Metrics - KPIs)
* **Independence Rate (Tỉ lệ tự lập):** Tỉ lệ học sinh pass bài tập với dưới 2 lượt gợi ý từ AI.
* **Time-to-fix (Tốc độ sửa lỗi):** Thời gian trung bình từ khi AI đưa ra gợi ý đầu tiên đến khi học sinh nộp bài Pass. Nếu chỉ số này giảm dần qua các bài tập -> Bot hướng dẫn hiệu quả.
* **Frustration Drop-off:** Tỉ lệ học sinh bỏ ngang bài tập sau khi gặp lỗi. Hệ thống tốt sẽ giữ chỉ số này ở mức cực thấp.

---
