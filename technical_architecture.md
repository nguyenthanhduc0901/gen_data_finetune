# TÀI LIỆU KỸ THUẬT & KIẾN TRÚC HỆ THỐNG (TECHNICAL ARCHITECTURE)

## 1. Tổng quan Kiến trúc Hệ thống (System Architecture)
Hệ thống được thiết kế theo mô hình **Client-Server-Agent**. Trong đó, VS Code Extension đóng vai trò là Client thu thập dữ liệu, Backend đóng vai trò điều phối và AI Agent (LangGraph) đóng vai trò là bộ não xử lý sư phạm.

### Các thành phần chính:
* **VS Code Extension (Frontend):** Xây dựng bằng TypeScript. Quản lý UI Chat, bắt sự kiện lưu file/nộp bài.
* **API Gateway / Backend Server:** Xây dựng bằng FastAPI (Python). Xử lý xác thực, quản lý danh sách bài tập và điều phối các yêu cầu đến AI Engine.
* **LangGraph AI Engine:** Trái tim của hệ thống, quản lý luồng tư duy Socratic và bộ nhớ người dùng.
* **Data Layer:**
    * **PostgreSQL:** Lưu trữ thông tin người dùng, bài tập và lịch sử nộp bài.
    * **LangGraph Store (SQLite/Postgres):** Lưu trữ Checkpoints (Short-term) và User Profiles (Long-term).

---

## 2. Thiết kế AI Agent (LangGraph Workflow)
Hệ thống sử dụng LangGraph để duy trì trạng thái hội thoại. Thay vì một luồng tuyến tính, đồ thị cho phép quay vòng (loop) khi học sinh chưa sửa được lỗi.

### Định nghĩa State (Graph State):
```python
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    code_context: str          # Nội dung code hiện tại
    error_message: str         # Log lỗi từ hệ thống chấm
    scaffolding_level: int     # Mức độ gợi ý (1-5)
    exercise_id: str           # ID bài tập để truy xuất metadata
    user_id: str               # ID người dùng cho bộ nhớ dài hạn
```

### Các Nodes chính:
1. **Analyze_Error_Node:** Sử dụng LLM để xác định nguyên nhân gốc rễ của lỗi (Root cause) mà không tiết lộ cho người dùng.
2. **Strategy_Node:** Dựa vào `scaffolding_level` và hồ sơ năng lực để chọn phương pháp (Gợi ý cú pháp, hỏi câu hỏi Socratic, hoặc yêu cầu giải thích code).
3. **Response_Generator_Node:** Tạo văn bản phản hồi tuân thủ nguyên tắc không đưa code giải.
4. **Memories_Update_Node:** Sau khi bài tập được "Pass", node này sẽ cập nhật các khái niệm đã nắm vững vào Long-term Store.

---

## 3. Quản lý Bộ nhớ (Memory Management)

### 3.1. Short-term Memory (Session-based)
* Sử dụng cơ chế **Checkpointer** của LangGraph.
* Mỗi `thread_id` được tạo ra bằng tổ hợp `user_id + exercise_id`.
* Giúp chatbot nhớ các bước gợi ý đã thực hiện trong cùng một bài tập.

### 3.2. Long-term Memory (Persistence Store)
* Sử dụng **LangGraph Store** để lưu trữ đối tượng `UserProfile`.
* Thông tin lưu trữ bao gồm:
    * `mastery_score`: Điểm thành thạo từng kỹ năng (Loops, Array, Logic...).
    * `common_pitfalls`: Danh sách các loại lỗi người dùng thường xuyên gặp lại.
    * `learning_pace`: Tốc độ phản hồi và sửa lỗi trung bình.

---

## 4. Giao tiếp Dữ liệu (Communication Protocol)

### API Endpoints:
* `POST /submit`: Nhận code và ID bài tập. Trả về kết quả chấm bài (Pass/Fail). Nếu Fail, kích hoạt luồng LangGraph.
* `GET /exercises`: Lấy danh sách bài tập cho sidebar.
* `GET /profile`: Lấy dữ liệu thống kê tiến độ học tập.

### Cơ chế Real-time:
* Sử dụng **WebSockets** hoặc **Server-Sent Events (SSE)** để stream câu trả lời từ AI Agent về VS Code, tạo cảm giác mượt mà khi nhận gợi ý.

---

## 5. Bảo mật và Hiệu suất (Security & Performance)
* **Sandbox Execution:** Hệ thống chấm bài (Judge System) phải chạy trong Docker container bị giới hạn tài nguyên để tránh mã độc từ học sinh.
* **Prompt Shield:** Sử dụng các kỹ thuật lọc đầu vào/đầu ra để ngăn chặn "Prompt Injection" (ví dụ: học sinh yêu cầu AI bỏ qua luật và đưa code giải).
* **Caching:** Lưu trữ kết quả phân tích cho các đoạn code lỗi phổ biến để giảm chi phí gọi API LLM.