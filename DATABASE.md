# TÀI LIỆU THIẾT KẾ CƠ SỞ DỮ LIỆU (DATABASE SCHEMA)
**Dự án:** CodeMentor AI (Socrates Code Tutor)
**Loại CSDL:** PostgreSQL (Hỗ trợ tốt JSONB cho LangGraph và AI Data)

---

## CỤM 1: QUẢN LÝ NGƯỜI DÙNG, LỚP HỌC & TRÍ NHỚ DÀI HẠN

Cụm này quản lý thông tin định danh, cấu trúc lớp học của giáo viên và "Hồ sơ năng lực" do AI ngầm đánh giá qua thời gian.

### 1.1. Bảng: `users`
| Trường dữ liệu | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | PK, UUID | Khóa chính. |
| `role` | Enum | `'student'`, `'teacher'`, `'admin'`. |
| `full_name` | String(100) | Họ và tên người dùng. |
| `email` | String(100), Unique | Địa chỉ email đăng nhập. |
| `password_hash` | String | Mật khẩu đã được mã hóa. |
| `created_at` | Timestamp | Thời gian tạo tài khoản. |
| `updated_at` | Timestamp | Thời gian cập nhật tài khoản gần nhất. |

### 1.2. Bảng: `classes`
| Trường dữ liệu | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | PK, UUID | Khóa chính. |
| `teacher_id` | FK (`users.id`) | Khóa ngoại trỏ đến giảng viên tạo lớp. |
| `class_name` | String(200) | Tên lớp học (VD: "Nhập môn Lập trình Python"). |
| `class_code` | String(50), Unique| Mã lớp (Dùng để sinh viên nhập vào và join lớp). |
| `created_at` | Timestamp | Thời gian tạo lớp. |

### 1.3. Bảng: `class_members` (Bảng trung gian n-n)
| Trường dữ liệu | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `class_id` | PK, FK (`classes.id`) | Khóa ngoại trỏ đến lớp học. |
| `student_id` | PK, FK (`users.id`) | Khóa ngoại trỏ đến sinh viên. |
| `joined_at` | Timestamp | Thời gian sinh viên tham gia lớp. |

### 1.4. Bảng: `user_ai_profiles` (Long-term Memory)
*Bảng này chứa dữ liệu để LangGraph đọc mỗi khi khởi tạo Node `Strategy_Planner_Node`. Nó quyết định AI sẽ đối xử với học sinh này như thế nào.*

| Trường dữ liệu | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `student_id` | PK, FK (`users.id`) | Khóa chính đồng thời là khóa ngoại. |
| `mastery_map` | JSONB | Mức độ thành thạo các kỹ năng. VD: `{"loops": 80, "arrays": 40, "recursion": 10}`. |
| `common_pitfalls` | JSONB | Các lỗi kinh niên. VD: `["forget_semicolon", "index_out_of_bounds"]`. |
| `independence_score`| Float | Tỉ lệ tự lập (0.0 - 1.0). Càng cao AI càng hỏi khó. |
| `frustration_count` | Int | Số lần học sinh bỏ cuộc (dùng để AI tăng sự đồng cảm). |
| `last_analyzed_at` | Timestamp | Lần cuối AI cập nhật hồ sơ này. |

---

## CỤM 2: QUẢN LÝ BÀI TẬP & JUDGE ENGINE (HỆ THỐNG CHẤM)

Cụm này lưu trữ đề bài, test case và lịch sử nộp bài, cung cấp đủ Context (Ngữ cảnh) để ném vào Prompt cho AI phân tích.

### 2.1. Bảng: `assignments`
| Trường dữ liệu | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | PK, UUID | Khóa chính. |
| `class_id` | FK (`classes.id`) | Lớp chứa bài tập này. |
| `title` | String(200) | Tiêu đề bài tập. |
| `description` | Text | Nội dung đề bài (Markdown). Ném cái này cho AI hiểu đề. |
| `knowledge_tags`| JSONB | Các thẻ kiến thức của bài. VD: `["loops", "conditions"]`. Quan trọng để AI update `mastery_map`. |
| `time_limit_ms` | Int | Giới hạn thời gian chạy code (milliseconds). |
| `memory_limit_kb`| Int | Giới hạn RAM cho phép (kilobytes). |
| `deadline` | Timestamp | Hạn chót nộp bài. |

### 2.2. Bảng: `test_cases`
| Trường dữ liệu | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | PK, UUID | Khóa chính. |
| `assignment_id` | FK (`assignments.id`)| Khóa ngoại trỏ đến bài tập tương ứng. |
| `input_data` | Text | Dữ liệu đầu vào của test case. |
| `expected_output` | Text | Kết quả đầu ra mong đợi. |
| `is_hidden` | Boolean | `true`: Test case ẩn để hệ thống chấm điểm.<br>`false`: Test case hiện để sinh viên tự test. |

### 2.3. Bảng: `submissions` (Lịch sử nộp bài)
| Trường dữ liệu | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | PK, UUID | Khóa chính. |
| `student_id` | FK (`users.id`) | Người nộp bài. |
| `assignment_id` | FK (`assignments.id`) | Bài tập được nộp. |
| `source_code` | Text | Mã nguồn sinh viên viết. |
| `language` | String(50) | Ngôn ngữ sử dụng (`'python'`, `'cpp'`, `'java'`...). |
| `status` | Enum | `'Pending'`, `'Accepted'`, `'Wrong Answer'`, `'Runtime Error'`, `'Syntax Error'`. |
| `passed_tests` | Int | Số lượng test case đã vượt qua. |
| `total_tests` | Int | Tổng số test case của bài tập. |
| `error_log` | Text | Dòng log lỗi thô từ Judge System (Ném cho Node 1 của LangGraph đọc). |
| `hints_used` | Int | Số lượt sinh viên chat với AI để sửa được lần nộp này (Phục vụ biểu đồ Dashboard). |
| `submitted_at` | Timestamp | Thời điểm nộp bài. |

---

## CỤM 3: HỆ SINH THÁI AI MENTOR (SHORT-TERM MEMORY & CONTEXT)

Cụm này đồng bộ hóa dữ liệu State của LangGraph lên Database quan hệ để quản lý và hiển thị trên web cho giáo viên/học sinh.

### 3.1. Bảng: `chat_threads`
*Trong LangGraph, đây chính là `thread_id` định danh cho Short-term Memory.*

| Trường dữ liệu | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | PK, String | Khóa chính. Phải format theo chuẩn: `"{student_id}_{assignment_id}"`. |
| `student_id` | FK (`users.id`) | Sinh viên chat. |
| `assignment_id` | FK (`assignments.id`)| Bài tập đang làm. |
| `scaffolding_level`| Int | Mức độ gợi ý hiện tại của phiên chat (1-4). AI lấy biến này để quyết định chiến lược. |
| `is_resolved` | Boolean | `true` khi học sinh Pass bài. Đóng thread. |
| `started_at` | Timestamp | Bắt đầu phiên chat. |
| `last_activity_at`| Timestamp | Thời gian tương tác cuối cùng. |

### 3.2. Bảng: `chat_messages`
*Chứa nội dung chat chi tiết hiển thị cho người dùng.*

| Trường dữ liệu | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | PK, UUID | Khóa chính. |
| `thread_id` | FK (`chat_threads.id`)| Thuộc luồng hội thoại nào. |
| `sender_role` | Enum | `'student'`, `'mentor'`, `'system_error'`. |
| `content` | Text | Nội dung tin nhắn chat. |
| `node_source` | String | (Internal) Tên Node của LangGraph sinh ra tin nhắn này (VD: `Response_Generator_Node`) để dễ debug AI. |
| `created_at` | Timestamp | Thời gian gửi tin nhắn. |

### 3.3. Bảng: `langgraph_checkpoints` (Tự động bởi LangGraph)
> **Lưu ý Kỹ thuật:** Bảng này không cần tự code tay. Khi dùng `PostgresSaver` của thư viện `langgraph-checkpoint-postgres`, nó sẽ tự động tạo bảng này để lưu toàn bộ `State` dưới dạng nhị phân (Binary) sau mỗi bước chạy của đồ thị AI.

### 3.4. Bảng: `learning_summaries` (Dành cho Dashboard Giáo viên)
*Được Node 4 (Memory_Updater_Node) tạo ra sau khi sinh viên pass bài.*

| Trường dữ liệu | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | PK, UUID | Khóa chính. |
| `student_id` | FK (`users.id`) | Khóa ngoại trỏ đến sinh viên. |
| `assignment_id` | FK (`assignments.id`)| Khóa ngoại trỏ đến bài tập. |
| `struggle_time_mins`| Int | Tổng thời gian loay hoay (Từ lúc Submit Fail đầu tiên đến lúc Pass). |
| `common_errors` | JSONB | Mảng lỗi gặp trong bài (VD: `["Logic Error in for loop"]`). |
| `ai_summary` | Text | Đoạn văn tóm tắt của AI. VD: "Sinh viên đã hiểu vòng lặp sau 3 gợi ý Socratic..." |
| `generated_at` | Timestamp | Thời điểm AI tự động tổng hợp. |

---

## 4. CHI TIẾT CẤU TRÚC JSON (JSON SCHEMA DEEP DIVE)

### Cấu trúc `mastery_map` trong bảng `user_ai_profiles`
Giúp giáo viên nhìn vào biểu đồ mạng nhện (Radar Chart) để biết học sinh mạnh/yếu phần nào.
```json
{
  "syntax_basics": 95,
  "conditional_logic": 80,
  "loops": 45,
  "functions": 60,
  "arrays": 30,
  "recursion": 0
}
```

### Cấu trúc `common_pitfalls` trong bảng `user_ai_profiles`
Giúp Node `Strategy_Planner_Node` nhận diện thói quen xấu của sinh viên để nhắc nhở kịp thời.
```json
[
  {
    "error_pattern": "IndexError",
    "frequency": 12,
    "last_seen": "2026-04-18T10:00:00Z"
  },
  {
    "error_pattern": "Off-by-one",
    "frequency": 5,
    "last_seen": "2026-04-15T14:30:00Z"
  }
]
```