import json
import os
import re
from agent import graph # Đảm bảo file agent.py cùng thư mục [cite: 357]

# Tự động lấy đường dẫn tuyệt đối của thư mục chứa file test.py này
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_CASES_PATH = os.path.join(BASE_DIR, "test_cases.json")
RESULT_PATH = os.path.join(BASE_DIR, "test_results.md")

def run_tests():
    # 1. Kiểm tra file test_cases.json
    if not os.path.exists(TEST_CASES_PATH):
        print(f"❌ LỖI: Không tìm thấy file tại: {TEST_CASES_PATH}")
        return

    with open(TEST_CASES_PATH, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    # 2. Khởi tạo file (Xóa nội dung cũ nếu có)
    print(f"🚀 Khởi tạo file kết quả tại: {RESULT_PATH}")
    with open(RESULT_PATH, "w", encoding="utf-8") as f:
        f.write("# BÁO CÁO KẾT QUẢ KIỂM THỬ AI AGENT - LAB 4\n\n")

    print(f"🔄 Đang chạy {len(test_cases)} test cases...")

    for case in test_cases:
        print(f"   - Đang chạy Test {case['id']}: {case['name']}")
        
        try:
            # Gọi Agent thực hiện suy luận
            result = graph.invoke({"messages": [("human", case['input'])]})
            
            # 3. Ghi log chi tiết vào Markdown [cite: 358]
            with open(RESULT_PATH, "a", encoding="utf-8") as f:
                f.write(f"### Test {case['id']}: {case['name']}\n")
                f.write(f"**Người dùng:** `{case['input']}`\n\n")
                f.write("#### 🛠 Luồng suy luận (Execution Trace):\n")

                for msg in result["messages"]:
                    # Log khi AI quyết định gọi Tool
                    if hasattr(msg, "tool_calls") and msg.tool_calls:
                        for tc in msg.tool_calls:
                            f.write(f"- 🔧 **Gọi công cụ**: `{tc['name']}`\n")
                            f.write(f"  - Tham số: `{tc['args']}`\n")
                    
                    # Log kết quả thực tế từ Tool trả về
                    if msg.type == "tool":
                        # Cắt bớt nếu kết quả quá dài để file MD gọn gàng
                        content_preview = str(msg.content)[:300] + "..." if len(str(msg.content)) > 300 else msg.content
                        f.write(f"  - 📥 **Kết quả Tool**: \n  ```text\n  {content_preview}\n  ```\n")

                # Câu trả lời cuối cùng cho User
                final_answer = result["messages"][-1].content
                f.write(f"\n**✅ TravelBuddy phản hồi:**\n> {final_answer}\n\n")
                f.write("---\n\n")
        
        except Exception as e:
            print(f"❌ Lỗi khi chạy Test {case['id']}: {str(e)}")
            with open(RESULT_PATH, "a", encoding="utf-8") as f:
                f.write(f"### Test {case['id']}: {case['name']}\n")
                f.write(f"❌ **LỖI HỆ THỐNG**: `{str(e)}`\n\n---\n\n")

    print(f"\n✨ HOÀN THÀNH! File đã nằm tại: {RESULT_PATH}")

if __name__ == "__main__":
    run_tests()