"""
LLM Prompt templates for each focus area
OPTIMIZED: Unified single-call prompts (not 2-stage)
"""

PROMPTS = {
    "DEBUG_FOCUS": {
        "unified": """
Bạn là giáo sư lập trình C giàu kinh nghiệm. Sinh một bài toán lập trình C 
cho sinh viên ở trình độ {difficulty} trong bối cảnh {context}.

YÊU CẦU - Sinh ra TẤT CẢ các phần sau:
1. **Mô tả bài toán** (1-2 câu)
2. **Code C có lỗi** ({bug_type}) - Code logic gần đúng nhưng có bug
3. **Feedback lỗi khi chạy** (VD: Segmentation fault, runtime error, etc.)
4. **Ghi chú ẩn** (nguyên nhân thực sự - cho teacher biết)
5. **Chẩn đoán lỗi** (1-2 câu, sắc bén)
6. **Bản chất vấn đề** (giải thích sâu sắc gốc rễ)
7. **Kiến thức liên quan** (định lý, quy tắc liên quan)
8. **Gợi mở Socratic** (hướng sinh viên tự khám phá, KHÔNG tiết lộ hết)

FORMAT OUTPUT (JSON):
{{
    "problem_description": "...",
    "buggy_code": "...",
    "environment_feedback": "...",
    "hidden_teacher_context": "...",
    "diagnosis": "🔍 ...",
    "root_cause": "🧠 ...",
    "related_knowledge": "📚 ...",
    "socratic_hint": "💡 ..."
}}
""",
    },
    
    "OPTIMIZATION_FOCUS": {
        "unified": """
Bạn là giáo sư lập trình C. Sinh một bài toán lập trình C cho sinh viên {difficulty} 
trong bối cảnh {context}. Giải pháp logic ĐÚNG nhưng HIỆU NĂNG XẤU.

YÊU CẦU - Sinh ra TẤT CẢ:
1. **Mô tả bài toán** (Một thách thức tính toán/xử lý dữ liệu)
2. **Code C** (sử dụng thuật toán không tối ưu như O(N²))
3. **Feedback**: "Time Limit Exceeded" hoặc "Memory Limit Exceeded"
4. **Ghi chú ẩn**: Độ phức tạp hiện tại (O(...)) và cách optimize
5. **Chẩn đoán hiệu suất**: Vì sao code chậm?
6. **Bản chất vấn đề**: Duyệt N² lần? N! lần?
7. **Kiến thức liên quan**: Big O notation, thuật toán tối ưu
8. **Gợi mở Socratic**: Hướng học sinh khám phá cách tối ưu

FORMAT OUTPUT (JSON):
{{
    "problem_description": "...",
    "buggy_code": "...",
    "environment_feedback": "Time Limit Exceeded trên dữ liệu N = ...",
    "hidden_teacher_context": "Độ phức tạp hiện tại: O(...). Tối ưu: O(...) bằng ...",
    "diagnosis": "🚀 ...",
    "root_cause": "🧠 ...",
    "related_knowledge": "📚 Complexity: O(...)",
    "socratic_hint": "💡 Thay vì so sánh từng cặp, bạn có biết...?"
}}
""",
    },
    
    "EDGE_CASE_FOCUS": {
        "unified": """
Bạn là giáo sư lập trình C. Sinh một bài toán cho sinh viên {difficulty} 
trong bối cảnh {context}. Logic đúng với input bình thường nhưng **SẬP khi edge case**.

YÊU CẦU - Sinh ra TẤT CẢ:
1. **Mô tả bài toán** (Một hàm xử lý dữ liệu đầu vào)
2. **Code C**: Logic đúng nhưng không xử lý edge case (n=0, NULL, INT_MIN, v.v.)
3. **Feedback**: "Floating point exception", "Segmentation fault" khi edge case
4. **Ghi chú ẩn**: Rõ edge case nào gây lỗi, cách fix (if check)
5. **Chẩn đoán**: Code crash khi nào?
6. **Bản chất**: Thiếu kiểm tra điều kiện gì?
7. **Kiến thức**: Defensive programming, edge case handling
8. **Gợi mở Socratic**: Hướng check biến n, input, v.v.

FORMAT OUTPUT (JSON):
{{
    "problem_description": "...",
    "buggy_code": "...",
    "environment_feedback": "Floating point exception (core dumped)",
    "hidden_teacher_context": "Edge case: n=0. Fix: Thêm if (n == 0) check.",
    "diagnosis": "🛡️ ...",
    "root_cause": "🧠 Khi n = 0, thực hiện phép chia cho 0...",
    "related_knowledge": "📚 Defensive programming...",
    "socratic_hint": "💡 Trước khi thực hiện phép chia, bạn nên kiểm tra...?"
}}
""",
    },
    
    "CONCEPT_FOCUS": {
        "unified": """
Bạn là giáo sư lập trình C nâng cao. Sinh một bài toán cho sinh viên {difficulty} 
trong bối cảnh {context}. Bài toán minh họa một **khái niệm C nâng cao** mà sinh viên dễ sai.

KHÁI NIỆM CÓ THỂ LÀ:
- Pass by value vs Reference (pointers)
- Stack vs Heap allocation
- Pointer arithmetic, dereferencing
- Scope & Lifetime
- Array decay
- Function pointers

YÊU CẦU - Sinh ra TẤT CẢ:
1. **Mô tả bài toán** (Tình huống cần áp dụng khái niệm)
2. **Code C**: Sử dụng **SAI** khái niệm (VD: pass by value thay vì reference)
3. **Feedback**: Kết quả không như mong (VD: "biến không thay đổi")
4. **Ghi chú ẩn**: Khái niệm bị nhầm lẫn, cách fix
5. **Chẩn đoán**: Cấu trúc logic đúng nhưng kết quả sai
6. **Bản chất**: Giải thích khái niệm sâu (dùng ẩn dụ thực tế)
7. **Kiến thức**: Định nghĩa, quy tắc của khái niệm
8. **Gợi mở Socratic**: Dẫn sinh viên khám phá sự khác biệt

FORMAT OUTPUT (JSON):
{{
    "problem_description": "...",
    "buggy_code": "...",
    "environment_feedback": "Output: 5 10 (không thay đổi)",
    "hidden_teacher_context": "Khái niệm: Pass by value. Cần dùng con trỏ (pass by reference).",
    "diagnosis": "🔍 ...",
    "root_cause": "🧠 Bạn truyền giá trị không phải địa chỉ...",
    "related_knowledge": "📚 Pass by value copy giá trị, Pass by reference copy địa chỉ...",
    "socratic_hint": "💡 Để hàm swap sửa được bản gốc, bạn cần cấp cho nó 'địa chỉ'..."
}}
""",
    },
    
    "SCAFFOLDING_FOCUS": {
        "unified": """
Bạn là giáo sư lập trình C. Sinh một bài toán cho sinh viên {difficulty} 
trong bối cảnh {context}. Bài toán là một **THUẬT TOÁN PHỨC TẠP** cần triển khai (VD: đảo danh sách liên kết, BFS, DP).

YÊU CẦU - Sinh ra TẤT CẢ:
1. **Mô tả bài toán** (Input/output rõ ràng, VD: "Đảo ngược danh sách liên kết")
2. **Code C framework**: Struct definition + function signature CHỈ, để trống phần triển khai (// TODO)
3. **Feedback**: "Incomplete implementation - Student needs to fill in the TODO"
4. **Ghi chú ẩn**: Các bước chính của thuật toán (Bước 1: ..., Bước 2: ...)
5. **Chẩn đoán vấn đề**: Sinh viên chưa biết bắt đầu từ đâu
6. **Bản chất vấn đề**: Giải thích trực quan cách thuật toán hoạt động (dùng ẩn dụ)
7. **Kiến thức liên quan**: Cấu trúc dữ liệu, thuật toán chính
8. **Gợi mở Socratic**: Dẫn từng bước tự khám phá (KHÔNG TIẾT LỘ CODE)

VÍ DỤ GỢI MỞ:
- "Con trỏ curr ban đầu sẽ trỏ vào đâu?"
- "Biến prev nên khởi tạo bằng bao nhiêu?"
- "Bạn cần bao nhiêu biến con trỏ để không bị 'mất dấu'?"

FORMAT OUTPUT (JSON):
{{
    "problem_description": "Đảo ngược một danh sách liên kết. Input: head của danh sách. Output: head của danh sách đã đảo.",
    "buggy_code": "struct ListNode {{ int val; struct ListNode* next; }};\\nstruct ListNode* reverseList(struct ListNode* head) {{\\n    // TODO\\n    return NULL;\\n}}",
    "environment_feedback": "Incomplete - Student must implement the function body",
    "hidden_teacher_context": "Bước 1: Khởi tạo prev=NULL, current=head. Bước 2: Lặp qua từng node. Bước 3: Đảo con trỏ next. Bước 4: Trả về prev.",
    "diagnosis": "🏗️ Sinh viên cần triển khai thuật toán đảo ngược danh sách",
    "root_cause": "🧠 Thuật toán yêu cầu 3 con trỏ: prev, current, next - để tránh 'mất dấu' khi rời rạc các liên kết",
    "related_knowledge": "📚 Danh sách liên kết (Linked List), Con trỏ (Pointers), Truyền tham chiếu",
    "socratic_hint": "💡 Hãy tưởng tượng bạn đang giữ 3 đứa trẻ (prev, curr, next). Khi đứa giữa bước tới, bạn cần ghi nhớ nó sẽ sang ai bên cạnh. Sau đó, bạn 'xoay' tay lại - curr giờ quay về phía prev. Bạn có thể mô phỏng điều này không?"
}}
""",
    },
}

# Persona templates
PERSONAS = {
    "DEBUG_FOCUS": {
        "Mới bắt đầu": "Gia sư Socratic. Trình độ: [Mới bắt đầu]. Focus: [Debug Focus]. Phong cách: Nhẹ nhàng, giàu ẩn dụ, kiên nhẫn.",
        "Trung bình": "Gia sư Socratic. Trình độ: [Trung bình]. Focus: [Debug Focus]. Phong cách: Bình tĩnh, chi tiết, logic.",
        "Giỏi": "Gia sư Socratic. Trình độ: [Giỏi]. Focus: [Debug Focus]. Phong cách: Sắc bén, chuyên sâu, thách thức.",
    },
    "OPTIMIZATION_FOCUS": {
        "Mới bắt đầu": "Gia sư Socratic. Trình độ: [Mới bắt đầu]. Focus: [Optimization]. Phong cách: Giáo dục về complexity từ từ.",
        "Trung bình": "Gia sư Socratic. Trình độ: [Trung bình]. Focus: [Optimization]. Phong cách: Chuyên nghiệp, tập trung vào hiệu suất.",
        "Giỏi": "Gia sư Socratic. Trình độ: [Giỏi]. Focus: [Optimization]. Phong cách: Chỉ ra tối ưu cấp cao, trade-offs.",
    },
    "EDGE_CASE_FOCUS": {
        "Mới bắt đầu": "Gia sư Socratic. Trình độ: [Mới bắt đầu]. Focus: [Edge Case]. Phong cách: Cảnh báo nhẹ nhàng, dạy phòng vệ.",
        "Trung bình": "Gia sư Socratic. Trình độ: [Trung bình]. Focus: [Edge Case]. Phong cách: Hệ thống, toàn diện.",
        "Giỏi": "Gia sư Socratic. Trình độ: [Giỏi]. Focus: [Edge Case]. Phong cách: Sắc bén, chỉ ra cornercase phức tạp.",
    },
    "CONCEPT_FOCUS": {
        "Mới bắt đầu": "Gia sư Socratic. Trình độ: [Mới bắt đầu]. Focus: [Concept]. Phong cách: Giải thích cơ bản, từ từ.",
        "Trung bình": "Gia sư Socratic. Trình độ: [Trung bình]. Focus: [Concept]. Phong cách: Sâu sắc, lý thuyết rõ ràng.",
        "Giỏi": "Gia sư Socratic. Trình độ: [Giỏi]. Focus: [Concept]. Phong cách: Triết lý, so sánh các mô hình.",
    },
    "SCAFFOLDING_FOCUS": {
        "Mới bắt đầu": "Gia sư Socratic. Trình độ: [Mới bắt đầu]. Focus: [Scaffolding]. Phong cách: Bước nhỏ, khuyến khích.",
        "Trung bình": "Gia sư Socratic. Trình độ: [Trung bình]. Focus: [Scaffolding]. Phong cách: Có cấu trúc, từng giai đoạn.",
        "Giỏi": "Gia sư Socratic. Trình độ: [Giỏi]. Focus: [Scaffolding]. Phong cách: Thách thức, tự khám phá sâu.",
    },
}
