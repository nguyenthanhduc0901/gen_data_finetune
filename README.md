# SOFTWARE REQUIREMENTS SPECIFICATION (SRS)
## DỰ ÁN: SOCRATES CODE TUTOR - GIA SƯ LẬP TRÌNH AI & HỆ SINH THÁI LỚP HỌC

---

## 1. GIỚI THIỆU (INTRODUCTION)

### 1.1 Mục tiêu dự án
Xây dựng một VS Code Extension đóng vai trò "Gia sư lập trình" (AI Tutor) dẫn dắt bằng phương pháp Socratic, đi kèm với một nền tảng Web quản lý bài tập dành cho giảng viên và hệ thống theo dõi lịch sử học tập cho sinh viên.

Hệ thống được thiết kế với **2 chế độ hoạt động (Dual Modes)** nhằm phục vụ mọi nhu cầu học lập trình:

*   **Chế độ Tự học (Free Mode - Tính năng cốt lõi):** Bất kỳ ai cũng có thể cài đặt Extension và sử dụng ngay lập tức không cần đăng nhập. AI hoạt động liên tục như một người bạn đồng hành, hỗ trợ sinh viên giải quyết các khó khăn (bug, logic, cú pháp) trong quá trình tự làm project cá nhân hoặc học ngôn ngữ mới.
*   **Chế độ Lớp học (Classroom Mode - Tính năng mở rộng):** Sinh viên đăng nhập vào Extension để liên kết với hệ thống của trường. Chế độ này biến VS Code thành một môi trường thi/làm bài tập khép kín. Sinh viên nhận đề bài, code và ấn "Nộp bài" (Compile & Run) qua Judge Server.

Dù ở chế độ nào, AI luôn tuân thủ **3 triết lý giáo dục nền tảng**:
1.  **Socratic Method (Phương pháp Socratic):** Tuyệt đối không đưa code đáp án trực tiếp. Tri thức được hình thành qua đối thoại và chất vấn.
2.  **Scaffolding (Giàn giáo nhận thức):** Cung cấp các bước hỗ trợ (gợi ý) theo từng bậc, và rút dần khi sinh viên đã hiểu vấn đề.
3.  **Formative Feedback (Phản hồi định dạng):** Giúp sinh viên trả lời 3 câu hỏi: Mình đang đi đâu? Mình đang ở đâu? Bước tiếp theo là gì?

### 1.2 Đối tượng mục tiêu
*   **Người tự học (Self-learner):** Dùng VS Code Extension không cần tài khoản để hỏi AI mỗi khi kẹt bug.
*   **Sinh viên trong trường (Primary User):** Đăng nhập Extension để lấy bài tập của lớp, dùng AI để hỗ trợ khi bí ý tưởng, nộp bài lấy điểm. Đồng thời truy cập nền tảng Web để xem lại lịch sử lỗi và rút kinh nghiệm.
*   **Giảng viên (Secondary User):** Quản lý lớp học, giao bài tập qua Web. Xem Dashboard phân tích lỗi để điều chỉnh giáo án.

---

## 2. NHÂN VẬT VÀ CÂU CHUYỆN NGƯỜI DÙNG (PERSONAS & USER STORIES)

### 2.1 Nhân vật (Personas)
*   **Bình (Người tự học):** Bình đang tự học Python trên YouTube. Bình cài Socrates Extension. Khi code bị báo lỗi `IndentationError`, Bình bôi đen đoạn code và hỏi chat: "Lỗi này là sao?". Bình không muốn phải tạo tài khoản lằng nhằng.
*   **An (Sinh viên):** Đang học Kỹ thuật lập trình. An đăng nhập tài khoản trường vào Extension. An click chọn bài "Tìm mảng âm" từ danh sách. Trong lúc code, An không biết bắt đầu từ đâu nên chat hỏi AI xin gợi ý. Sau khi code xong, An ấn "Submit", nếu trượt test case, AI tiếp tục nhảy ra phân tích lỗi sai giúp An. Thi thoảng AI hiện ra một ô trống nhỏ hỏi dò An xem biến đếm hiện tại bằng mấy, An nhập đáp án vào ô đó để kiểm tra tư duy. Tối đến, An lên Web App để xem lại bài tập này mình đã mắc lỗi gì và AI đã khuyên gì.
*   **Thầy Huy (Giảng viên):** Giao bài tập cho lớp của An. Thầy dùng Dashboard trên Web để xem 50 sinh viên lớp mình thường mắc lỗi tư duy nào nhất trong bài tập tuần này.

### 2.2 Câu chuyện người dùng (User Stories)

| ID | Vai trò | Chế độ | Mong muốn | Lý do |
| :--- | :--- | :--- | :--- | :--- |
| **US.1** | Người tự học | Free Mode | Sử dụng Chatbot AI trên VS Code ngay lập tức mà không cần đăng nhập. | Để sửa lỗi code cá nhân một cách nhanh chóng, tránh rào cản thao tác. |
| **US.2** | Sinh viên | Free & Class | Gửi đoạn code đang chọn (highlight) và lỗi Terminal cho AI phân tích bất cứ lúc nào. | Để được AI dẫn dắt gỡ lỗi ngay trong quá trình đang code. |
| **US.3** | Giảng viên | Web App | Tạo bài tập, cấu hình bộ Test case (ẩn/hiện) và giao cho Lớp. | Để đồng bộ hóa tiến độ kiểm tra, đánh giá. |
| **US.4** | Sinh viên | Class Mode | Đăng nhập và xem danh sách Bài tập (TreeView) trực tiếp trên VS Code Sidebar. | Tập trung 100% trên IDE, không cần mở trình duyệt lấy đề bài. |
| **US.5** | Sinh viên | Class Mode | Nhấn nút "Submit" để nộp bài và tự động nhận câu hỏi dẫn dắt từ AI nếu bị rớt Test case. | Để hiểu tại sao thuật toán của mình sai so với yêu cầu của giảng viên. |
| **US.6** | Giảng viên | Web App | Xem Dashboard thống kê các cụm lỗi (Syntax, Logic) chung của lớp trên 1 bài tập. | Để biết sinh viên hổng kiến thức chỗ nào và ôn tập trên lớp. |
| **US.7** | Sinh viên | Web App | Đăng nhập Web để xem tóm tắt (Summary) các lỗi và gợi ý của bài tập đã hoàn thành. | Để ôn tập, nhìn lại chặng đường gỡ lỗi và rút kinh nghiệm cho kỳ thi. |
| **US.8** | Sinh viên | Free & Class | Trả lời các câu hỏi kiểm tra nhanh của AI thông qua một ô nhập liệu (Input Box) riêng biệt. | Để đảm bảo mình đang hiểu đúng dòng code đó thay vì chỉ đọc text của AI. |
| **US.9** | Sinh viên | Free & Class | Chuyển đổi giữa chế độ gợi ý Ngắn gọn (Hint) và Chi tiết (Explain). | Để tự chủ mức độ hỗ trợ tùy thuộc vào mức độ bế tắc của bản thân. |

---

## 3. KỊCH BẢN SỬ DỤNG CHI TIẾT (USE CASE SCENARIOS)

### 3.1 Scenario 1: Free Mode - Gỡ lỗi code cá nhân liên tục (Không đăng nhập)
*   **Bối cảnh:** Bình đang code một tool nhỏ bằng Python, chưa đăng nhập tài khoản nào trên Extension.
*   **Luồng sự kiện:**
    1.  Bình viết lệnh đọc file nhưng bị lỗi `FileNotFoundError`. Bình đang vội nên chọn chế độ gợi ý "Ngắn gọn (Hint)".
    2.  Bình bôi đen đoạn code `open('data.txt', 'r')`, mở tab Socrates Chat và hỏi: "Tại sao nó báo lỗi không tìm thấy file?"
    3.  Extension tự động thu thập đoạn code được bôi đen và gửi lên Socratic Engine.
    4.  **Socrates (AI):** "Lỗi FileNotFoundError. Bạn hãy kiểm tra lại xem file 'data.txt' đang nằm ở thư mục gốc hay thư mục 'assets'?" (Gợi ý ngắn gọn)
    5.  Bình: "À, nó nằm trong thư mục assets."
    6.  Bình sửa thành `open('assets/data.txt', 'r')` và chương trình chạy thành công.

### 3.2 Scenario 2: Classroom Mode - Đặt câu hỏi tương tác (Interactive Input)
*   **Bối cảnh:** An đang kẹt ở vòng lặp bài Tìm giá trị lớn nhất mảng. An chọn chế độ "Chi tiết (Explain)".
*   **Luồng sự kiện:**
    1.  An chat: "Code của tôi chạy sai ở lần lặp thứ 2."
    2.  **Socrates (AI):** "Chúng ta cùng kiểm tra nhé. Mảng của bạn là a = [2, 5, 1]. Ở vòng lặp i = 1..."
    3.  Trình duyệt Chatbox hiển thị một câu hỏi theo dõi: "Tại a[1] giá trị sẽ bằng mấy?" và kèm theo một **[ Ô nhập liệu / Input Box ]**.
    4.  An nhập số 5 vào ô và nhấn Enter.
    5.  **Socrates (AI):** "Chính xác! Vậy nếu max đang là 2, thuật toán của bạn so sánh 2 với 5 sẽ xảy ra chuyện gì tiếp theo? Dưới đây là giải thích chi tiết về nguyên lý so sánh biến tạm..." (Giải thích dài)

### 3.3 Scenario 3: Classroom Mode - Tự động Socratic khi nộp bài sai (Submit Fail)
*   **Bối cảnh:** An đã viết xong code cho bài PROB_01 và tự tin ấn "Submit".
*   **Luồng sự kiện:**
    1.  Extension gom code và ID bài tập gửi lên Judge Server Backend.
    2.  Judge Server trả về: `[Failed] - Sai Test Case: Input(9) | Expected(False) | Got(True)`.
    3.  Cửa sổ Chat tự động bật mở, AI chủ động lên tiếng.
    4.  **Socrates (AI):** "Hệ thống vừa chấm đoạn code của bạn. Với N = 9, code của bạn cho rằng đây là số nguyên tố. Nhưng 9 có chia hết cho số nào khác ngoài 1 và 9 không?"
    5.  An nhận ra lỗi logic, sửa code và Submit lại thành công. Khi Pass toàn bộ, Extension ngầm tổng hợp lại toàn bộ lịch sử lỗi và gửi về Database.

### 3.4 Scenario 4: Web App - Sinh viên ôn tập lịch sử học tập
*   **Bối cảnh:** Cuối tuần, An muốn ôn lại các bài đã làm để chuẩn bị thi giữa kỳ.
*   **Luồng sự kiện:**
    1.  An đăng nhập vào nền tảng Web (Student Portal).
    2.  An click vào bài PROB_01 đã hoàn thành.
    3.  Giao diện Web hiển thị một thẻ **"Lịch sử gỡ lỗi (Bug History Summary)"**:
        *   Lỗi từng mắc: Nhận diện sai điều kiện vòng lặp (Logic Error).
        *   Gợi ý cốt lõi từ AI: "Chú ý điều kiện chia hết cho các số từ 2 đến căn bậc 2 của N."
    4.  An ghi chú lại kinh nghiệm này vào sổ tay.

---

## 4. YÊU CẦU CHỨC NĂNG (FUNCTIONAL REQUIREMENTS)

### 4.1 Module VS Code Extension - Tính năng Cốt lõi (Hoạt động Offline/Free Mode)
*   **FR.1 - Context Capture:** Nút "Ask Socrates" hoặc phím tắt cho phép tự động trích xuất: Đoạn code đang bôi đen (hoặc toàn bộ file hiện tại), ngôn ngữ lập trình, và lỗi hiển thị ở Terminal.
*   **FR.2 - Socratic Chat & Interactive UI:** Giao diện Webview hiển thị cửa sổ chat. Có khả năng hiển thị các câu hỏi theo dõi người dùng (Tracking Questions) đi kèm với khung nhập liệu (Input Box) chuyên biệt để sinh viên nhập đáp án thực hành (VD: dự đoán giá trị biến). Sau khi nộp đáp án, AI sẽ nhận diện, đánh giá đúng/sai và tiếp tục lí giải. (Không có nút Copy code đáp án).
*   **FR.3 - Suggestion Modes (Chế độ gợi ý):** Giao diện cung cấp tùy chọn (Toggle/Dropdown) cho phép người dùng chọn mức độ can thiệp của AI:
    *   **Ngắn gọn (Hint):** AI chỉ đưa ra từ khóa, mớm lời nhanh chóng.
    *   **Chi tiết (Explain):** AI giải thích cặn kẽ nguyên lý của lỗi và lý thuyết đằng sau đó.
*   **FR.4 - Anonymous Session:** Khởi tạo phiên làm việc với AI qua thiết bị (Device ID) mà không cần yêu cầu thông tin đăng nhập.

### 4.2 Module VS Code Extension - Tính năng Lớp học (Classroom Mode)
*   **FR.5 - Native Authentication:** Giao diện Đăng nhập (Student Account) tích hợp ngay trong Extension. Trạng thái lưu bằng JWT.
*   **FR.6 - Assignment TreeView:** Sau khi đăng nhập, hiển thị Sidebar chứa Danh sách Bài tập (Active Assignments).
*   **FR.7 - Workspace Auto-Setup:** Click vào bài tập tự động mở 1 tab Markdown (Đề bài) và tạo 1 file code trống (main.cpp/main.py).
*   **FR.8 - Code Submission & Session Summarization:** Nút "Run & Submit". Gửi file lên Judge Server.
    *   Nếu Failed: Tự động chuyển tín hiệu sang Chat UI.
    *   Nếu Passed: Extension tự động tóm tắt (Summarize) toàn bộ lịch sử hội thoại của bài tập này và gửi dữ liệu về Database để lưu trữ.

### 4.3 Module Nền tảng Web (Teacher & Student Portal)
*   **FR.9 - Course & Assignment Management:** Giảng viên tạo/quản lý Lớp học. Tạo bài tập (Đề bài, Giới hạn thời gian, Bộ Test case Input/Output).
*   **FR.10 - Teacher Dashboard:** Phân tích dữ liệu học tập. Hiển thị tỷ lệ Pass/Fail, phân loại lỗi phổ biến (Syntax, Time Limit, Logic) cho từng bài tập cụ thể.
*   **FR.11 - Student Learning History (Lịch sử học tập):** Sinh viên có thể đăng nhập trên nền tảng Web. Đối với mỗi bài tập đã giải xong, hệ thống hiển thị bảng tóm tắt quan sát lại chặng đường: Đã mắc những lỗi gì? Nhận được những gợi ý (Hint/Explain) cốt lõi nào từ AI? giúp học sinh đối chiếu và rút kinh nghiệm.

### 4.4 Module Hệ thống Backend (AI & Judge Engine)
*   **FR.12 - Socratic AI Layer:**
    *   Trường hợp Free Mode: System Prompt + Code sinh viên + Chế độ gợi ý (Hint/Explain) + Câu hỏi.
    *   Trường hợp Class Mode: System Prompt + Code sinh viên + Đề bài + Kết quả Judge Server + Lịch sử lỗi.
*   **FR.13 - Anti-Solution Guard:** Lớp rào chắn (Parser & System Prompt cực nghiêm) chặn tuyệt đối LLM sinh ra khối code hoàn chỉnh đưa cho sinh viên trong mọi hoàn cảnh.
*   **FR.14 - Judge Server Execution:** Môi trường Sandbox (Docker) biên dịch và thực thi code sinh viên nộp an toàn, chống mã độc. So sánh kết quả với Test case.

---

## 5. KIẾN TRÚC HỆ THỐNG (SYSTEM ARCHITECTURE)

Hệ thống được thiết kế linh hoạt để đáp ứng 2 luồng API độc lập:

1.  **VS Code Client (TypeScript):** Chứa lõi thu thập ngữ cảnh (Context) và giao diện hiển thị (bao gồm cả các component Interactive Input Box). Có bộ quản lý State để phân biệt đang ở Free Mode hay Classroom Mode và trạng thái Hint/Explain.
2.  **API Gateway (Node.js/Go):**
    *   Endpoint `/api/chat/free`: Chấp nhận request không cần token (Giới hạn Rate Limit theo IP/Device để tránh spam).
    *   Endpoint `/api/class/*`: Yêu cầu JWT Token. Xử lý logic lấy bài tập, nộp bài, và tiếp nhận bản Summarize lịch sử chat từ Extension gửi lên.
3.  **Judge Server (Python/C++ Sandbox):** Chạy độc lập, chuyên nhận Job chấm code và trả về kết quả (Pass/Fail/Error).
4.  **Socratic Logic Engine:** Lớp trung gian nhận dữ liệu từ API Gateway. Nhào nặn Context thành Prompt sư phạm và gửi tới LLM (OpenAI GPT-4o / Gemini 1.5). Trả phản hồi về cho VS Code (bao gồm text và JSON cho các Interactive Question).
5.  **Database (PostgreSQL/MongoDB):** Lưu trữ tài khoản, lớp học, bài tập, test case, log hội thoại của sinh viên và Bản tóm tắt lịch sử lỗi, gợi ý phục vụ cho Dashboard của Giáo viên lẫn Web Portal của Sinh viên.

---

## 6. QUY TRÌNH DỮ LIỆU VÀ PROMPT STRATEGY (CỐT LÕI)

Để AI hoạt động linh hoạt, System Prompt (Quy tắc hệ thống) phải phân biệt được sinh viên đang hỏi tự do hay đang làm bài tập, đồng thời tuân thủ độ dài gợi ý (Hint/Explain).

**Nguyên tắc chung của AI (Strict Rule):** "Bạn là Socrates. Không viết lại code. Dùng Formative Feedback. Thỉnh thoảng hãy trả về định dạng JSON `<interactive_question>` để yêu cầu sinh viên nhập đáp án dự đoán giá trị biến."

*   **Ngữ cảnh 1 (Free Mode): Tự gỡ lỗi**
    *   Dữ liệu đẩy vào: Code hiện tại + Câu hỏi + Mode: Hint.
    *   **AI Hành động:** Nhận diện ngôn ngữ. Đặt câu hỏi mớm lời cực ngắn về các hàm thư viện chuẩn (VD: "Trong Python có hàm tách chuỗi. Bạn thử tìm hiểu hàm .split() nhé?").
*   **Ngữ cảnh 2 (Classroom Mode): Nộp bài rớt Test Case**
    *   Dữ liệu đẩy vào: Đề bài + Code hiện tại + Judge_Result + Mode: Explain.
    *   **AI Hành động:** Focus vào logic sai biệt. Trả về giải thích sâu kèm câu hỏi tương tác yêu cầu nhập giá trị.
*   **Ngữ cảnh 3 (Post-Completion): Tổng hợp lịch sử**
    *   Dữ liệu đẩy vào: Toàn bộ log chat của 1 bài tập.
    *   **AI Hành động (Chạy ngầm):** Tóm tắt lại thành 3 gạch đầu dòng: "Lỗi đã gặp", "Nguyên nhân", "Kinh nghiệm rút ra" và gửi về Database để sinh viên xem trên Web.

---

## 7. YÊU CẦU PHI CHỨC NĂNG (NON-FUNCTIONAL REQUIREMENTS)

*   **NFR.1 - Tiếp cận không độ trễ (Zero-friction Access):** Extension phải hoạt động được tính năng chat AI (Free Mode) ngay sau khi cài đặt thành công từ VS Code Marketplace (< 10 giây setup).
*   **NFR.2 - Hiệu năng AI & Chấm điểm:**
    *   Phản hồi chat thông thường: < 3 giây.
    *   Chấm code qua Judge Server + Phản hồi AI đầu tiên: < 7 giây.
*   **NFR.3 - Bảo mật Judge Server:** Sandbox cô lập hoàn toàn mạng, không có quyền Read/Write ra ngoài thư mục ảo.
*   **NFR.4 - Anti-Solution Reliability:** Tỷ lệ chống "Prompt Injection" (sinh viên lừa AI để lấy đáp án) thành công > 98%.
*   **NFR.5 - Phân tích dữ liệu (Analytics):** Dashboard chỉ tổng hợp dữ liệu từ các sinh viên thuộc Classroom Mode để đảm bảo tính chính xác của phổ điểm và lỗ hổng kiến thức.

---

## 8. KẾ HOẠCH TRIỂN KHAI (DEVELOPMENT ROADMAP)

Sự thay đổi về tính năng đòi hỏi phải triển khai theo phương pháp Agile, ưu tiên làm sản phẩm cốt lõi (Free Mode) trước để kiểm chứng AI Socratic.

### Phase 1: Core Socratic Tutor (Free Mode) (Tuần 1-4)
*   **Mục tiêu:** Xây dựng xong VS Code Extension hoạt động như một AI Chatbot.
*   Thiết kế API Gateway ẩn danh.
*   Tích hợp tính năng bôi đen code, trích xuất lỗi Terminal đẩy vào khung chat.
*   Phát triển giao diện Chat hỗ trợ Form Input (Ô nhập liệu tương tác) và Nút gạt chế độ (Hint/Explain).
*   Nghiên cứu Prompt Engineering: Tinh chỉnh System Prompt cực mạnh để LLM đóng vai trò Gia sư mà không tiết lộ đáp án.

### Phase 2: Web Platform & Judge Engine (Tuần 5-9)
*   **Mục tiêu:** Xây dựng hệ thống quản lý học tập (Backend & Web).
*   Phát triển Web App (Tạo tài khoản Giảng viên/Sinh viên, Tạo Lớp học, Soạn bài tập & Test case).
*   Xây dựng giao diện xem Lịch sử học tập cho Sinh viên trên Web.
*   Thiết lập Judge Server Backend (sử dụng Docker hoặc thư viện Judge0) để có khả năng nhận mã nguồn và tự động chấm điểm.

### Phase 3: Classroom Integration & Dashboard (Tuần 10-14)
*   **Mục tiêu:** Ghép nối hệ sinh thái.
*   Bổ sung tính năng Đăng nhập (JWT) và TreeView Danh sách bài tập vào VS Code Extension.
*   Code nút "Submit", nối luồng: Submit -> Judge Server -> Trigger AI Socratic Chat nếu Fail.
*   Viết logic tự động Summarize lịch sử chat gửi về Database khi sinh viên giải quyết xong bài tập.
*   Hoàn thiện Dashboard phân tích lỗi cho Giảng viên trên Web App.
*   **Beta Testing:** Cài đặt cho một nhóm nhỏ dùng thử ở cả chế độ tự do và chế độ làm bài tập.