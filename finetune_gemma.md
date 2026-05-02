# TÀI LIỆU KỸ THUẬT: FINE-TUNING GEMMA-4-E4B-IT CHO TÁC VỤ CODE DEBUGGING

> **Mục tiêu:** Tinh chỉnh (Fine-tune) mô hình `google/gemma-4-E4B-it` bằng phương pháp QLoRA để phục vụ chuyên sâu cho các bài toán phát hiện, phân loại và sửa lỗi mã nguồn (Code Debugging).
> 
> **Benchmark System:** Dựa trên tiêu chuẩn đánh giá của DebugEval (Task 1, 2, 3, 4) và khung luận lý của framework COAST.

---

## 1. TỔNG QUAN HỆ THỐNG & CÁC TÁC VỤ (TASKS)

Hệ thống được thiết kế để đánh giá năng lực "Sư phạm lập trình" và "Gỡ lỗi" của mô hình Gemma thông qua bộ dữ liệu DebugEval. 

### Các tác vụ lõi:

| Task | Tên tác vụ | Loại bài toán | Mục tiêu của Model | Metric |
| :--- | :--- | :--- | :--- | :--- |
| **Task 1** | **BUG Localization** | Multiple-choice | Đọc code lỗi, chỉ ra chính xác dòng/đoạn code gây lỗi (A, B, C, D). | Accuracy |
| **Task 2** | **BUG Identification** | Multiple-choice | Phân loại lỗi (Syntax, Reference, Logical, Multiple). | Accuracy |
| **Task 3** | **Code Repair** | Generation | Viết lại code hoàn chỉnh để sửa lỗi. Đánh giá bằng việc chạy test cases thực tế. | Pass@1 |
| **Task 4** | **Code Recognition** | Binary-choice | Đọc 2 đoạn code (1 đúng, 1 sai), chỉ ra đoạn nào sai. Phải đúng cả chiều xuôi và ngược. | Accuracy (Joint) |

---

## 2. KIẾN TRÚC FINE-TUNING (TRAINING PIPELINE)

Việc fine-tune dòng mô hình Gemma 4 đòi hỏi một số kỹ thuật can thiệp sâu (Monkey Patching) vào cấu trúc mạng nơ-ron để tương thích với thư viện PEFT.

### 2.1. Giải quyết Xung đột Kiến trúc Gemma
Trong file training, chúng ta áp dụng 2 bản vá (patch) cốt lõi trước khi load mô hình:
1. **Patch `set_submodule`:** Khắc phục lỗi thiếu hàm chuẩn trong `torch.nn.Module` khi thư viện PEFT cố gắng tiêm (inject) adapter LoRA vào mô hình.
2. **Bóc vỏ `Gemma4ClippableLinear`:** Chuyển đổi các layer Linear đặc thù của kiến trúc Gemma 4 về dạng `nn.Linear` tiêu chuẩn để LoRA có thể "móc" vào các target modules một cách trơn tru.

### 2.2. Cấu hình QLoRA & Tối ưu Bộ nhớ
Hệ thống sử dụng cấu hình tối ưu nhất cho phần cứng hạn chế VRAM:
* **Quantization 4-bit (BitsAndBytes):** Dùng định dạng `nf4` và tính toán bằng `bfloat16`. Bỏ qua lượng tử hóa ở các module ngoại vi (`vision_tower`, `audio_tower`, `lm_head`).
* **LoRA Target Modules:** Tiêm diện rộng vào toàn bộ các ma trận tuyến tính `["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]` với Rank `r=16` và `alpha=32`.
* **Memory Hacks:** 
  * Bật biến môi trường `PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True"` để chống phân mảnh VRAM.
  * Kích hoạt `gradient_checkpointing=True` để đánh đổi tốc độ tính toán lấy không gian VRAM.

### 2.3. Cấu trúc Dữ liệu Đầu vào (Data Processing)
Gemma là mô hình Instruction-tuned, do đó dữ liệu DebugEval được chuyển đổi qua hàm `apply_chat_template` để giữ đúng format hội thoại chuẩn của mô hình:
* **Input (Instruction):** Đề bài + Mã nguồn chứa lỗi.
* **Label (Output):** Khớp chính xác với đáp án mong đợi, bắt buộc kết thúc bằng special token `<end_of_turn>`.

---

## 3. CHIẾN LƯỢC PROMPT & ĐÁNH GIÁ (EVALUATION PIPELINE)

Để đánh giá chính xác độ hiệu quả của việc fine-tune, hệ thống Inference được thiết kế với tiêu chí **Strict Roleplay (Ép khuôn định dạng)** để chống hiện tượng mô hình "lải nhải" (hallucination/yapping).

### 3.1. Kỹ thuật Prompting
Thay vì dùng cấu trúc Zero-shot thông thường, Prompt được thiết kế cực kỳ gắt gao. Ví dụ với Task 1 & 2:

```text
CRITICAL INSTRUCTIONS:
1. DO NOT explain your reasoning.
2. DO NOT output any words, greetings, or analysis.
3. Your entire response MUST consist of exactly ONE tag.
Example of VALID output: <Answer>(A)</Answer>
```
*Lưu ý: Việc bọc đáp án trong thẻ `<Answer>...</Answer>` giúp hàm Post-processing dùng Regex bóc tách kết quả dễ dàng và đạt tỷ lệ chính xác cao nhất về mặt định dạng.*

### 3.2. Tối ưu Hyper-parameters khi Inference
Để tối đa hóa tính ổn định (Determinism) trong các bài toán đánh giá:
* **`temperature = 0.2`:** Hạ cực thấp để triệt tiêu tính sáng tạo vô ý.
* **`max_new_tokens = 50`:** Rất ngắn, vì model chỉ được phép xuất ra thẻ `<Answer>` (áp dụng cho Task 1, 2, 4).
* **Early Stopping:** Bổ sung ID của `<end_of_turn>` vào danh sách `eos_token_id` để mô hình lập tức dừng sinh text ngay khi hoàn thành đáp án.

### 3.3. Phương pháp Tính điểm (Metrics)

| Task | Tiêu chuẩn đánh giá (Điều kiện đúng) |
| :--- | :--- |
| **Task 1 & 2** | Chuỗi đáp án model sinh ra có chứa Option gốc (A, B, C, D) **VÀ** model không in ra nhiều hơn 1 Option (kiểm tra chặt chẽ bằng hàm `is_single_answer`). |
| **Task 3** | Tính điểm **Pass@1**. Mô hình sinh ra code sửa lỗi, code này được đưa vào Sandbox Online Judge (OJ) để chạy các private test cases. Trả về AC (Accept) toàn bộ test case mới được tính là Pass. |
| **Task 4** | Model phải chọn đúng code lỗi trong bài test xuôi (Code-A là lỗi) **VÀ** bài test ngược (Code-B là lỗi). Tính năng chấm 2 chiều này giúp loại bỏ hoàn toàn khả năng mô hình đoán mò theo vị trí (bias). |

---

## 4. KẾT QUẢ ĐÁNH GIÁ (EVALUATION RESULTS)

Sau khi hoàn tất quá trình Fine-tuning, mô hình được đưa vào Inference để đánh giá bộ test và so sánh trực tiếp với kiến trúc gốc chưa qua tinh chỉnh (Baseline). 

Dưới đây là bảng tổng hợp kết quả (Model Comparison Summary):

| Tác vụ (Task) | Baseline (Gemma gốc) | LoRA (Đã Fine-tune) | Độ cải thiện (Gain) | Metric |
| :--- | :--- | :--- | :--- | :--- |
| **Task 1: BUG Localization** | 65.40% | **79.30%** | 🟢 +13.90% | Accuracy |
| **Task 2: BUG Identification** | 46.90% | **61.02%** | 🟢 +14.12% | Accuracy |
| **Task 3: Code Repair** | 30.90% | **55.02%** | 🔥 **+24.12%** | Pass@1 |
| **Task 4: Code Recognition** | 73.04% | **87.54%** | 🟢 +14.50% | Accuracy |

### Phân tích kết quả:
* **Tuân thủ định dạng xuất sắc:** Ở các tác vụ trắc nghiệm (Task 1, 2, 4), mô hình LoRA tăng trung bình ~14% độ chính xác. Điều này chứng minh mô hình đã học được cách định vị lỗi code và tuân thủ chặt chẽ yêu cầu xuất ra định dạng thẻ `<Answer>` mà không bị ảo giác sinh chữ thừa.
* **Sự bứt phá ở Task 3 (Code Repair):** Task khó nhất đòi hỏi mô hình phải thực sự sinh ra code chạy được (Executable Code) đã ghi nhận mức tăng kỷ lục hơn **24%**. Điều này khẳng định chiến lược fine-tune bằng tập dữ liệu gỡ lỗi chất lượng cao có tác động cực kỳ mạnh mẽ đến khả năng tư duy logic và sửa lỗi lập trình của mô hình Gemma-4-E4B.

---

## 5. KẾT LUẬN VÀ BƯỚC TIẾP THEO

Việc tinh chỉnh thành công mô hình Gemma-4-E4B-it bằng phương pháp QLoRA đã mang lại một công cụ Code Debugging mạnh mẽ, tối ưu hóa rất tốt cho môi trường phần cứng hạn chế (VRAM thấp).

**Hướng đi tiếp theo:**
1. Triển khai mô hình LoRA này vào các pipeline thực tế (ví dụ: làm engine cốt lõi cho AI Mentor hoặc Code Review Assistant).
2. Tích hợp sâu hơn cơ chế **Chain-of-Thought (CoT)** vào dữ liệu huấn luyện để phân tích xem liệu có thể đẩy điểm Pass@1 của Task 3 vượt ngưỡng 65% hay không.