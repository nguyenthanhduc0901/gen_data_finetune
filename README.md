# TÀI LIỆU TỔNG QUAN SẢN PHẨM (PRD)

**Tên dự án:** CodeMentor AI  
**Phiên bản tài liệu:** 1.1.0  
**Loại sản phẩm:** VS Code Extension, Web Dashboard, AI Learning Companion  
**Người dùng chính:** Sinh viên lập trình nhập môn, giảng viên, trợ giảng, quản trị viên học vụ  
**Công nghệ lõi:** FastAPI, PostgreSQL, LangGraph, LLM, Judge Sandbox, VS Code Extension, Web Application

---

## 1. Tóm tắt dự án

**CodeMentor AI** là nền tảng hỗ trợ học lập trình theo hướng sư phạm, không phải công cụ sinh lời giải. Hệ thống giúp sinh viên tự debug, tự giải thích suy nghĩ và phát triển năng lực lập trình thông qua các gợi ý có kiểm soát. Với giảng viên, hệ thống cung cấp dashboard và chatbot phân tích tình trạng học tập của lớp, từng sinh viên, từng bài tập và từng nhóm kiến thức.

Sản phẩm gồm ba bề mặt trải nghiệm chính:

1. **VS Code Extension cho sinh viên:** làm bài, nộp bài, nhận gợi ý Socratic khi gặp lỗi.
2. **Web cho giảng viên:** quản lý lớp, bài tập, xem phân tích học tập, hỏi chatbot về lớp/sinh viên, tạo bài tập nháp bằng AI rồi review/approve.
3. **Web cho sinh viên:** theo dõi tiến độ cá nhân, xem năng lực theo kỹ năng, hỏi chatbot về tình trạng học tập của mình và được điều hướng đến bài tập cần làm.

Định hướng cốt lõi của dự án là **AI Mentor có giới hạn**, tức AI có thể phân tích sâu nhưng không đưa lời giải hoàn chỉnh. AI phải ưu tiên câu hỏi gợi mở, ví dụ tương tự, kiểm tra hiểu biết và phản tư học tập.

---

## 2. Vấn đề cần giải quyết

### 2.1. Với sinh viên

- Sinh viên dễ phụ thuộc vào ChatGPT/Copilot để lấy đáp án trực tiếp.
- Khi gặp lỗi compiler, runtime hoặc wrong answer, sinh viên thường không biết bắt đầu debug từ đâu.
- Sinh viên thiếu công cụ theo dõi tiến độ học tập theo từng kỹ năng nhỏ như vòng lặp, mảng, hàm, đệ quy, xử lý chuỗi.
- Sinh viên không nhìn thấy mối liên hệ giữa lỗi hiện tại và thói quen sai trong quá khứ.

### 2.2. Với giảng viên

- Giảng viên khó biết sinh viên thực sự kẹt ở đâu trong quá trình làm bài.
- Dashboard truyền thống thường chỉ hiển thị điểm cuối, không hiển thị hành trình debug.
- Việc tạo bài tập, test case, rubric và gợi ý mẫu tốn thời gian.
- Giảng viên cần một cách hỏi nhanh: "Lớp này đang yếu phần nào?", "Sinh viên A gần đây có tiến bộ không?", "Bài nào nên ôn lại trên lớp?".

### 2.3. Với hệ thống đào tạo

- Cần chuẩn hóa dữ liệu học tập từ code, submission, hint, chat, test case và profile năng lực.
- Cần kiểm soát rủi ro AI làm lộ lời giải, tạo bài tập sai, hoặc phân tích thiên lệch.

---

## 3. Mục tiêu sản phẩm

### 3.1. Mục tiêu chính

- Giúp sinh viên cải thiện năng lực debug và tư duy thuật toán mà không bị phụ thuộc vào lời giải.
- Giúp giảng viên quan sát tiến độ lớp và can thiệp đúng thời điểm.
- Biến dữ liệu làm bài thành hồ sơ năng lực theo từng kỹ năng lập trình.
- Cung cấp AI chatbot cho giảng viên và sinh viên trên web với quyền truy cập dữ liệu phù hợp.
- Hỗ trợ một dạng bài tập mới: **Reverse Teaching Exercise**, trong đó agent đặt câu hỏi ngược lại, sinh viên đóng vai "trợ giảng" và phải prompt/giảng giải để chứng minh mình hiểu.

### 3.2. Mục tiêu ngoài phạm vi MVP

- Không thay thế toàn bộ LMS.
- Không tự động chấm điểm cuối kỳ có tính pháp lý cao.
- Không cho phép AI tự publish bài tập mà không có giảng viên approve.
- Không tối ưu cho mọi ngôn ngữ lập trình ngay từ đầu. MVP ưu tiên Python, sau đó mở rộng C/C++/Java.

---

## 4. Chân dung người dùng

### 4.1. Sinh viên

**Mục tiêu:** hoàn thành bài tập, hiểu lỗi, biết tự debug, biết mình yếu kỹ năng nào.  
**Nỗi đau:** đọc log không hiểu, nộp sai nhiều lần, không biết nên ôn lại bài nào.  
**Hành vi mong muốn:** thử sửa trước khi hỏi, giải thích được ý tưởng, dùng gợi ý như công cụ học chứ không dùng AI để lấy đáp án.

### 4.2. Giảng viên

**Mục tiêu:** thiết kế bài tập đúng trình độ, biết lớp đang kẹt ở đâu, can thiệp kịp thời.  
**Nỗi đau:** thiếu dữ liệu quá trình, khó cá nhân hóa hỗ trợ, mất thời gian tạo bài tập và test case.  
**Hành vi mong muốn:** xem dashboard, hỏi chatbot, review bài tập AI đề xuất, phê duyệt nội dung trước khi giao.

### 4.3. Trợ giảng

**Mục tiêu:** hỗ trợ lớp đông, phát hiện nhóm sinh viên cần giúp, lọc các submission/chat cần xem.  
**Nỗi đau:** không đủ thời gian đọc từng bài và từng đoạn chat.  
**Hành vi mong muốn:** nhận danh sách ưu tiên can thiệp và tóm tắt lỗi thường gặp.

### 4.4. Quản trị viên

**Mục tiêu:** quản lý tài khoản, lớp, quyền truy cập, cấu hình model, chính sách dữ liệu.  
**Nỗi đau:** rủi ro bảo mật, log nhạy cảm, chi phí LLM, quyền xem dữ liệu sinh viên.  
**Hành vi mong muốn:** cấu hình hệ thống ổn định, audit được lịch sử AI và truy cập dữ liệu.

---

## 5. Tính năng cốt lõi

### 5.1. VS Code Extension cho sinh viên

| Mã | Tính năng | Mô tả | Ưu tiên |
| :--- | :--- | :--- | :--- |
| F1 | Đăng nhập và chọn lớp | Sinh viên đăng nhập, chọn lớp, đồng bộ danh sách bài tập. | MVP |
| F2 | Danh sách bài tập | Sidebar hiển thị bài được giao, deadline, trạng thái, số lần nộp. | MVP |
| F3 | Nộp bài | Gửi code, language, assignment_id đến Judge Sandbox. | MVP |
| F4 | Auto-trigger AI Mentor | Chỉ mở chat khi submission fail hoặc khi bài tập cho phép tự luyện. | MVP |
| F5 | Context Binding | AI nhận đề bài, code hiện tại, test fail, log lỗi, lịch sử hint mà sinh viên không cần copy-paste. | MVP |
| F6 | Socratic Chat | AI hỏi gợi mở, tăng mức scaffolding theo số lần fail và năng lực cá nhân. | MVP |
| F7 | Hint Budget | Giới hạn số lượt gợi ý theo policy của bài/lớp. | MVP |
| F8 | Reflection Prompt | Sau khi pass, sinh viên giải thích ngắn lỗi vừa sửa để củng cố kiến thức. | V1 |

### 5.2. Web cho giảng viên

| Mã | Tính năng | Mô tả | Ưu tiên |
| :--- | :--- | :--- | :--- |
| T1 | Quản lý lớp | Tạo lớp, mời sinh viên, xem danh sách, phân quyền trợ giảng. | MVP |
| T2 | Exercise Builder | Tạo đề, test case, tag kiến thức, rubric, giới hạn hint. | MVP |
| T3 | Dashboard lớp | Tỉ lệ hoàn thành, hint density, error clusters, knowledge gaps. | MVP |
| T4 | Hồ sơ sinh viên | Mastery map, recurring pitfalls, independence score, learning trend. | MVP |
| T5 | Chatbot giảng viên | Hỏi đáp về tình trạng lớp, bài tập, từng sinh viên, đề xuất can thiệp. | V1 |
| T6 | AI Exercise Drafting | AI tạo nháp bài tập, test case, rubric, gợi ý sư phạm; giảng viên review và approve. | V1 |
| T7 | Review AI Logs | Xem các quyết định AI quan trọng, prompt output, lý do đưa gợi ý. | V1 |

### 5.3. Web cho sinh viên

| Mã | Tính năng | Mô tả | Ưu tiên |
| :--- | :--- | :--- | :--- |
| S1 | Learning Dashboard | Tổng quan bài đã làm, bài đang kẹt, deadline, kỹ năng yếu. | V1 |
| S2 | Student Chatbot | Sinh viên hỏi về tiến độ cá nhân, nên ôn gì, bài nào cần làm tiếp. | V1 |
| S3 | Assignment Navigation | Chatbot điều hướng đến bài tập, trang luyện tập hoặc tài nguyên liên quan. | V1 |
| S4 | Reflection History | Xem lại lỗi đã gặp, gợi ý đã nhận, bài học rút ra. | V1 |

### 5.4. Reverse Teaching Exercise

Reverse Teaching Exercise là dạng bài tập trong đó sinh viên không chỉ viết code mà còn phải **giảng giải lại** cho agent. Agent đóng vai người học có hiểu biết chưa hoàn chỉnh, đặt câu hỏi ngược, yêu cầu sinh viên diễn giải thuật toán, chỉ ra lỗi trong ví dụ, hoặc prompt cho agent từng bước.

Mục tiêu của dạng bài này:

- Kiểm tra hiểu biết khái niệm thay vì chỉ kiểm tra output.
- Buộc sinh viên externalize reasoning bằng lời.
- Giúp giảng viên đánh giá năng lực giải thích, không chỉ năng lực code.
- Tạo dữ liệu học tập giàu hơn cho `mastery_map`.

Các chế độ Reverse Teaching:

| Chế độ | Mô tả | Ví dụ |
| :--- | :--- | :--- |
| Explain Back | Sinh viên giải thích thuật toán cho agent. | "Hãy giảng cho tôi vì sao vòng lặp này dừng đúng." |
| Agent Confusion | Agent cố tình hiểu sai và hỏi lại. | "Tôi nghĩ index bắt đầu từ 1 trong Python, đúng không?" |
| Prompt-to-Teach | Sinh viên phải viết prompt/hướng dẫn để agent tự sửa lỗi. | "Hãy hướng dẫn tôi sửa lỗi mà không đưa code hoàn chỉnh." |
| Diagnose Agent Answer | Agent đưa lời giải sai một phần, sinh viên phải phản biện. | "Đoạn giải thích này sai ở đâu?" |

---

## 6. Luồng trải nghiệm chính

### 6.1. Sinh viên làm bài trên VS Code

1. Sinh viên đăng nhập extension.
2. Chọn lớp và bài tập.
3. Viết code trong workspace.
4. Nhấn `Submit`.
5. Judge chạy test trong sandbox.
6. Nếu pass, hệ thống ghi nhận submission và yêu cầu reflection ngắn.
7. Nếu fail, AI Mentor mở chat với context đầy đủ.
8. Sinh viên trao đổi với AI trong hint budget.
9. Sinh viên sửa code và nộp lại.
10. Khi pass, LangGraph cập nhật learning summary và long-term memory.

### 6.2. Giảng viên hỏi chatbot về lớp

1. Giảng viên mở dashboard lớp.
2. Hỏi: "Tuần này lớp đang yếu phần nào nhất?"
3. Chatbot truy vấn analytics snapshot, submissions, learning summaries và mastery map.
4. Chatbot trả lời bằng số liệu, dẫn chứng và đề xuất hành động.
5. Giảng viên có thể click vào nhóm sinh viên/bài tập liên quan.

### 6.3. Giảng viên tạo bài tập bằng AI

1. Giảng viên chọn chủ đề, độ khó, kỹ năng cần kiểm tra.
2. AI tạo draft gồm đề bài, input/output, test case, rubric, tags, hint policy.
3. Hệ thống đánh dấu các phần cần review.
4. Giảng viên chỉnh sửa và approve.
5. Bài tập chỉ được publish sau khi có approval.

### 6.4. Sinh viên dùng chatbot web

1. Sinh viên mở dashboard cá nhân.
2. Hỏi: "Mình đang yếu phần nào?"
3. Chatbot trả lời dựa trên dữ liệu của chính sinh viên đó.
4. Chatbot gợi ý bài tập cần làm tiếp và điều hướng bằng link nội bộ.
5. Chatbot không tiết lộ đáp án của bài chưa hoàn thành.

### 6.5. Reverse Teaching

1. Sinh viên chọn bài tập dạng Reverse Teaching.
2. Agent đưa tình huống hoặc code có lỗi.
3. Sinh viên giải thích/prompt/đặt câu hỏi hướng dẫn agent.
4. Agent hỏi lại để kiểm tra hiểu biết.
5. Hệ thống chấm theo rubric: đúng khái niệm, rõ ràng, không bỏ sót edge case, khả năng sửa hiểu lầm.
6. Kết quả được ghi vào learning summary.

---

## 7. Chính sách AI và sư phạm

- **Không đưa lời giải hoàn chỉnh:** AI không sinh toàn bộ code giải bài đang giao.
- **Ưu tiên câu hỏi:** dưới ngưỡng can thiệp, AI hỏi để sinh viên tự phát hiện lỗi.
- **Tăng scaffolding có điều kiện:** nếu fail nhiều lần hoặc frustration cao, AI có thể đưa ví dụ tương tự nhưng vẫn không giải trực tiếp.
- **Minh bạch với giảng viên:** các phân tích quan trọng phải có dữ liệu nguồn và mức tin cậy.
- **Giảng viên kiểm duyệt bài tập AI:** AI chỉ tạo draft, không tự publish.
- **Tách quyền dữ liệu:** sinh viên chỉ xem dữ liệu của mình; giảng viên chỉ xem lớp mình phụ trách.

---

## 8. Chỉ số thành công

| Nhóm | KPI | Ý nghĩa |
| :--- | :--- | :--- |
| Học tập | Independence Rate | Tỉ lệ pass với ít hơn hoặc bằng 2 hint. |
| Học tập | Time-to-Fix | Thời gian từ fail đầu tiên đến pass. |
| Học tập | Concept Recovery | Kỹ năng từng yếu có cải thiện qua các bài sau không. |
| Trải nghiệm | Frustration Drop-off | Tỉ lệ bỏ bài sau nhiều lần fail. |
| Giảng viên | Intervention Precision | Đề xuất can thiệp của chatbot có được giảng viên dùng không. |
| Nội dung | Exercise Approval Rate | Tỉ lệ bài tập AI draft được approve sau chỉnh sửa. |
| An toàn | Code Leakage Rate | Tỉ lệ phản hồi AI vi phạm chính sách không lộ lời giải. |

---

## 9. Trạng thái hoàn thiện tính năng

Theo tài liệu hiện có trước bản 1.1.0, dự án **chưa hoàn thiện về mặt yêu cầu sản phẩm**. Các phần đã có gồm ý tưởng AI Mentor, memory, dashboard cơ bản, database ban đầu và fine-tune. Các phần còn thiếu đã được bổ sung trong bộ docs mới:

- Chatbot web cho giảng viên.
- Chatbot web cho sinh viên.
- AI tạo bài tập nháp và luồng approve.
- Reverse Teaching Exercise.
- User stories chi tiết.
- API contract.
- Roadmap triển khai.
- Đánh giá mức độ chi tiết và danh sách tài liệu còn thiếu.
- Thiết kế LangGraph đơn giản hơn, tránh multi-agent quá phức tạp cho MVP.

---

## 10. Bản đồ tài liệu

| File | Vai trò |
| :--- | :--- |
| `README.md` | PRD tổng quan và phạm vi sản phẩm. |
| `docs_audit.md` | Đánh giá mức độ chi tiết, thiếu sót và quyết định bổ sung tài liệu. |
| `user_stories.md` | User stories, acceptance criteria và priority. |
| `technical_architecture.md` | Kiến trúc kỹ thuật, LangGraph mới, tích hợp hệ thống. |
| `chatbot.md` | Chi tiết AI Mentor, chatbot web, Reverse Teaching và prompt policy. |
| `database.md` | Thiết kế cơ sở dữ liệu cập nhật. |
| `api_contracts.md` | API contract cho extension, web, chatbot và analytics. |
| `finetune_gemma.md` | Chiến lược fine-tune/evaluation và cách đưa model vào hệ thống. |
| `roadmap.md` | Lộ trình MVP, V1 và các rủi ro triển khai. |
