# CƠ SỞ DỮ LIỆU: SOCRATES CODE TUTOR

Tài liệu thiết kế cơ sở dữ liệu (Database Schema) cho hệ thống Socrates Code Tutor, được chia thành 3 cụm logic chính.

---

## Cụm 1: Quản lý Người dùng và Lớp học (User & Access Control)

### Bảng: `users`
| Trường dữ liệu | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | PK, UUID | Khóa chính. |
| `role` | Enum | Các quyền: `'student'`, `'teacher'`, `'admin'`. |
| `full_name` | String | Họ và tên người dùng. |
| `email` | String | Địa chỉ email. |
| `password_hash` | String | Mật khẩu đã được mã hóa. |
| `created_at` | Timestamp | Thời gian tạo tài khoản. |
| `updated_at` | Timestamp | Thời gian cập nhật tài khoản gần nhất. |

### Bảng: `classes`
| Trường dữ liệu | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | PK, UUID | Khóa chính. |
| `teacher_id` | FK (`users.id`) | Khóa ngoại trỏ đến giảng viên tạo lớp. |
| `class_name` | String | Tên lớp học. |
| `class_code` | String | Mã lớp (Dùng để sinh viên nhập vào và join lớp). |

### Bảng: `class_members` (Bảng trung gian n-n)
| Trường dữ liệu | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `class_id` | FK (`classes.id`) | Khóa ngoại trỏ đến lớp học. |
| `student_id` | FK (`users.id`) | Khóa ngoại trỏ đến sinh viên. |
| `joined_at` | Timestamp | Thời gian sinh viên tham gia lớp. |

---

## Cụm 2: Quản lý Bài tập và Chấm điểm (Judge Engine Data)

### Bảng: `assignments`
> **Ghi chú:** Tương ứng với yêu cầu chức năng FR.9

| Trường dữ liệu | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | PK, UUID | Khóa chính. |
| `class_id` | FK (`classes.id`) | Khóa ngoại trỏ đến lớp chứa bài tập này. |
| `title` | String | Têu đề bài tập. |
| `description` | Text/Markdown | Nội dung đề bài. |
| `time_limit_ms` | Int | Giới hạn thời gian chạy code (milliseconds). |
| `memory_limit_kb` | Int | Giới hạn RAM cho phép (kilobytes). |
| `deadline` | Timestamp | Hạn chót nộp bài. |

### Bảng: `test_cases`
| Trường dữ liệu | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | PK, UUID | Khóa chính. |
| `assignment_id` | FK (`assignments.id`) | Khóa ngoại trỏ đến bài tập tương ứng. |
| `input_data` | Text | Dữ liệu đầu vào của test case. |
| `expected_output` | Text | Kết quả đầu ra mong đợi. |
| `is_hidden` | Boolean | `true`: Test case ẩn để hệ thống chấm điểm.<br>`false`: Test case hiện để sinh viên tự test. |

### Bảng: `submissions` (Lịch sử nộp bài)
| Trường dữ liệu | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | PK, UUID | Khóa chính. |
| `student_id` | FK (`users.id`) | Sinh viên nộp bài. |
| `assignment_id` | FK (`assignments.id`) | Bài tập được nộp. |
| `source_code` | Text | Mã nguồn sinh viên viết. |
| `language` | String | Ngôn ngữ sử dụng (`'python'`, `'cpp'`, `'java'`...). |
| `status` | Enum | Trạng thái: `'Pending'`, `'Accepted'`, `'Wrong Answer'`, `'Time Limit Exceeded'`, `'Runtime Error'`. |
| `passed_tests` | Int | Số lượng test case đã vượt qua. |
| `total_tests` | Int | Tổng số test case của bài tập. |
| `submitted_at` | Timestamp | Thời gian nộp bài. |

---

## Cụm 3: Hệ sinh thái AI Socratic (Lõi khác biệt của hệ thống)

### Bảng: `chat_sessions` (Quản lý phiên hội thoại)
| Trường dữ liệu | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | PK, UUID | Khóa chính. |
| `session_mode` | Enum | Chế độ: `'Free'` hoặc `'Class'`. |
| `device_id` | String | Dùng để track người dùng ở Free Mode (không cần login), phục vụ giới hạn Rate Limit. |
| `student_id` | FK (`users.id`) | Sinh viên chat (Nullable nếu ở Free Mode). |
| `assignment_id` | FK (`assignments.id`)| Bài tập đang làm (Nullable nếu ở Free Mode). |
| `started_at` | Timestamp | Thời gian bắt đầu phiên chat. |
| `last_activity_at` | Timestamp | Thời gian tương tác cuối cùng. |

### Bảng: `chat_messages` (Chi tiết từng câu chat)
| Trường dữ liệu | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | PK, UUID | Khóa chính. |
| `session_id` | FK (`chat_sessions.id`)| Thuộc phiên hội thoại nào. |
| `sender_role` | Enum | Người gửi: `'user'`, `'ai'`, `'system'`.<br>*(System dùng để đẩy lỗi Terminal hoặc đề bài ngầm vào Context).* |
| `content` | Text | Nội dung tin nhắn chat. |
| `interactive_metadata`| JSONB | Lưu trữ dữ liệu cho FR.8 (Câu hỏi Input Box).<br>Ví dụ: `{"type": "guess_variable", "variable": "i", "expected_value": "5", "student_answer": "4", "is_correct": false}`. |
| `suggestion_mode` | Enum | Chế độ hỗ trợ của AI: `'Hint'` hoặc `'Explain'`. |
| `created_at` | Timestamp | Thời gian gửi tin nhắn. |

### Bảng: `learning_summaries` (Bản tóm tắt học tập)
> **Ghi chú:** Tương ứng với yêu cầu chức năng FR.11 & Scenario 4

| Trường dữ liệu | Kiểu / Ràng buộc | Mô tả |
| :--- | :--- | :--- |
| `id` | PK, UUID | Khóa chính. |
| `student_id` | FK (`users.id`) | Khóa ngoại trỏ đến sinh viên. |
| `assignment_id` | FK (`assignments.id`) | Khóa ngoại trỏ đến bài tập. |
| `common_errors` | JSONB | Mảng các lỗi mắc phải. <br>Ví dụ: `["Logic Error in for loop", "Index out of bounds"]` |
| `core_hints_received` | JSONB | Mảng lưu trữ các lời khuyên/gợi ý cốt lõi từ AI. |
| `lessons_learned` | Text | Bài học / Kinh nghiệm rút ra được AI tổng hợp. |
| `generated_at` | Timestamp | Thời điểm AI tự động tổng hợp (sau khi nộp bài Pass). |