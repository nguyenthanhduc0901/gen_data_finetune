# TÀI LIỆU CHI TIẾT HỆ THỐNG AI MENTOR (CORE INTELLIGENCE & MEMORY)

## 1. Triết lý Sư phạm Độc quyền (Core Philosophy)
Hệ thống không vận hành như một công cụ hỗ trợ code thông thường. Chatbot được thiết kế để **Trì hoãn sự hỗ trợ (Delayed Support)** và **Gợi mở tư duy (Scaffolding)**.
- **Passive Trigger:** Chatbot chỉ hoạt động khi có tín hiệu "Fail" từ Judge System.
- **Socratic Method:** Luôn đặt câu hỏi thay vì khẳng định.
- **No-Code Policy:** Tuyệt đối không in ra đoạn mã sửa lỗi hoàn chỉnh (Snippet).

---

## 2. Kiến trúc Não bộ (LangGraph Nodes)

Hệ thống chia làm 4 Nodes xử lý tuần tự để đảm bảo tính logic và sư phạm:

1. **Analyze_Error_Node:**
   - **Nhiệm vụ:** Đọc thầm code và lỗi để tìm ra Root Cause.
   - **Output:** JSON chứa loại lỗi, dòng lỗi và khái niệm kiến thức cần xem lại.
2. **Strategy_Planner_Node:**
   - **Nhiệm vụ:** Dựa vào `Short-term Memory` (đã gợi ý gì rồi?) và `Long-term Memory` (học sinh này giỏi hay yếu?) để chọn mức độ gợi ý.
   - **Output:** Quyết định chọn Level 1 (Nhắc nhở) -> Level 4 (Ví dụ tương đồng).
3. **Response_Generator_Node:**
   - **Nhiệm vụ:** Chuyển chiến lược thành câu nói tự nhiên, lịch sự, khích lệ.
   - **Output:** Tin nhắn hiển thị trên VS Code.
4. **Memory_Updater_Node:**
   - **Nhiệm vụ:** Khi bài tập hoàn thành (Pass), tổng hợp lại hành trình để lưu vào bộ nhớ dài hạn.

---

## 3. Hệ thống Trí nhớ (Memory Architecture)

Đây là phần quan trọng nhất để chatbot "hiểu" từng người dùng:

### 3.1. Short-term Memory (Trí nhớ ngắn hạn - Session Context)
- **Cơ chế:** Sử dụng `MemorySaver` của LangGraph.
- **Phạm vi:** Một bài tập cụ thể (`thread_id = user_id + exercise_id`).
- **Nội dung lưu trữ:**
  * Lịch sử các lần nộp bài lỗi trong phiên đó.
  * Các gợi ý đã được đưa ra để tránh nói lại ý cũ.
  * Trạng thái cảm xúc/độ nản lòng (Frustration level) dựa trên số lần fail liên tiếp.

### 3.2. Long-term Memory (Trí nhớ dài hạn - User Profile Store)
- **Cơ chế:** Sử dụng `BaseStore` (không dùng RAG để tối ưu tốc độ).
- **Phạm vi:** Toàn bộ quá trình học của học sinh (`user_id`).
- **Nội dung lưu trữ:**
  * **Mastery Map:** Danh sách các Node kiến thức (VD: `loop: 80%`, `recursion: 30%`).
  * **Recurring Pitfalls:** Những lỗi "kinh niên" mà học sinh này hay gặp (VD: "Thường xuyên quên khởi tạo biến").
  * **Adaptation Level:** Điều chỉnh chatbot thành "khó tính" (Socratic thuần) hoặc "tận tình" (Scaffolding nhiều) tùy theo năng lực học sinh.

---

## 4. Hệ thống Prompt Engineering (The Brain Prompts)

### 4.1. Prompt Phân tích (Analyze_Error_Node)
```text
Bạn là chuyên gia phân tích mã nguồn. Hãy xác định Root Cause.
ĐẦU VÀO: <student_code>, <error_log>.
RÀNG BUỘC: CHỈ trả về JSON. KHÔNG giao tiếp.
{
  "error_type": "...", 
  "root_cause": "...",
  "hint_focus": "Dòng code hoặc biến cụ thể cần học sinh chú ý"
}
```

### 4.2. Prompt Sinh phản hồi (Response_Generator_Node)
```text
Bạn là Mentor. Hãy tạo câu hỏi dựa trên Chiến lược: {strategy}.
NGUYÊN TẮC:
- Dưới 3 lần sai: Chỉ dùng câu hỏi khơi gợi (Socratic).
- Trên 3 lần sai: Đưa ra ví dụ tương đồng (Scaffolding).
- Tuyệt đối không cho code giải bài này.
- Kết hợp Long-term Memory: Nếu học sinh hay sai lỗi này, hãy nhắc lại lịch sử.
```

---

## 5. Cẩm nang Scaffolding (Intervention Levels)

| Level | Loại gợi ý | Mục đích | Ví dụ |
| :--- | :--- | :--- | :--- |
| 1 | **Location Hint** | Chỉ vị trí lỗi. | "Nhìn lại dòng 5 xem, có gì đó chưa ổn." |
| 2 | **Concept Probe** | Hỏi về khái niệm. | "Biến `i` của bạn bắt đầu từ mấy và kết thúc ở đâu?" |
| 3 | **Logic Bridge** | Liên kết logic. | "Nếu mẫu số là 0 thì phép chia này sẽ như thế nào?" |
| 4 | **Parallel Example** | Ví dụ tương tự. | "Thử xem cách khai báo mảng trong bài mẫu này nhé..." |

---

## 6. Dashboard Insights (Cho Giáo viên)
Dựa trên Memory của Chatbot, hệ thống xuất ra các chỉ số:
- **Hint Density:** Bài tập nào học sinh phải "cầu cứu" AI nhiều nhất.
- **Learning Curve:** Biểu đồ thể hiện sự tiến bộ (số lần cần gợi ý giảm dần theo thời gian).
- **Common Obstacles:** Tổng hợp những lỗi sai phổ biến của cả lớp để giáo viên giảng lại.

---
**Lưu ý:** Tất cả các luồng xử lý trên phải đảm bảo tính bảo mật Sandbox khi chạy code của học sinh để tránh tấn công hệ thống.