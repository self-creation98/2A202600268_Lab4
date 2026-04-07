from langchain_core.tools import tool
import re

# Mock Data (Dữ liệu giả lập từ tài liệu) [cite: 61, 64, 125]
FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy"},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650_000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800_000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 4.6},
    ],
}

@tool
# def search_flights(origin: str, destination: str) -> str:
#     """Tìm kiếm các chuyến bay giữa hai thành phố.""" 
#     key = (origin, destination)
#     flights = FLIGHTS_DB.get(key)
    
#     # Thử tra ngược nếu không thấy [cite: 193]
#     if not flights:
#         flights = FLIGHTS_DB.get((destination, origin))
        
#     if not flights:
#         return f"Không tìm thấy chuyến bay từ {origin} đến {destination}." 
    
#     res = f"Các chuyến bay từ {origin} đến {destination}:\n"
#     for f in flights:
#         res += f"- {f['airline']} ({f['departure']}): {f['price']:,} VNĐ ({f['class']})\n"
#     return res

def search_flights(origin: str, destination: str) -> str:
    """Tìm kiếm các chuyến bay giữa hai thành phố."""
    print(f"[LOG] Đang tra cứu chuyến bay từ {origin} đến {destination}...") # Thêm Logging 
    try:
        key = (origin, destination)
        flights = FLIGHTS_DB.get(key)
        
        if not flights:
            print(f"[LOG] Không tìm thấy lượt đi, đang thử tra cứu ngược lại...")
            flights = FLIGHTS_DB.get((destination, origin)) 
            
        if not flights:
            return f"Không tìm thấy chuyến bay giữa {origin} và {destination}."
        
        res = f"Các chuyến bay từ {origin} đến {destination}:\n"
        for f in flights:
            res += f"- {f['airline']} ({f['departure']}): {f['price']:,} VNĐ ({f['class']})\n" 
        return res
    except Exception as e:
        return f"Lỗi hệ thống khi tìm chuyến bay: {str(e)}"
    
# def search_flights(origin: str, destination: str) -> str:
#     """Tìm kiếm các chuyến bay giữa hai thành phố (Ví dụ: Hà Nội, Đà Nẵng)."""
#     # 1. Chuẩn hóa dữ liệu đầu vào (Xử lý lỗi hoa/thường và khoảng trắng thừa)
#     origin_clean = origin.strip().title()
#     dest_clean = destination.strip().title()
    
#     # 2. Logging an toàn (Dùng tiếng Anh hoặc bỏ dấu để tránh lỗi Windows)
#     print(f"[LOG] Searching: {origin_clean} -> {dest_clean}") 
    
#     try:
#         key = (origin_clean, dest_clean)
#         flights = FLIGHTS_DB.get(key)
        
#         # Thử tra ngược chiều nếu không thấy [cite: 193]
#         if not flights:
#             flights = FLIGHTS_DB.get((dest_clean, origin_clean))
            
#         if not flights:
#             return f"Không tìm thấy chuyến bay từ {origin_clean} đến {dest_clean} trong hệ thống."
        
#         # 3. Trả về kết quả đúng định dạng [cite: 195]
#         res = f"Các chuyến bay từ {origin_clean} đến {dest_clean}:\n"
#         for f in flights:
#             res += f"- {f['airline']} ({f['departure']}): {f['price']:,} VNĐ\n"
#         return res
#     except Exception as e:
#         # Nếu có lỗi, in ra console để Leader debug nhưng không làm sập Agent
#         print(f"Error in search_flights: {e}")
#         return "Hệ thống đang gặp sự cố khi tra cứu chuyến bay. Vui lòng thử lại."

@tool
# # def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
# #     """Tìm kiếm khách sạn tại một thành phố theo giá tối đa.""" 
# #     hotels = HOTELS_DB.get(city, [])
# #     # Lọc theo giá và sắp xếp theo rating giảm dần [cite: 206, 208]
# #     filtered = [h for h in hotels if h['price_per_night'] <= max_price_per_night]
# #     filtered.sort(key=lambda x: x['rating'], reverse=True)
    
# #     if not filtered:
# #         return f"Không tìm thấy khách sạn tại {city} với giá dưới {max_price_per_night:,}/đêm." 
    
# #     res = f"Khách sạn tại {city} (ưu tiên đánh giá cao):\n"
# #     for h in filtered:
# #         res += f"- {h['name']} ({h['stars']} sao): {h['price_per_night']:,} VNĐ/đêm - Đánh giá: {h['rating']}\n"
# #     return res

def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """Tìm kiếm khách sạn tại một thành phố theo giá tối đa."""
    print(f"[LOG] Đang tìm khách sạn tại {city} với ngân sách < {max_price_per_night:,} VNĐ/đêm...")
    try:
        hotels = HOTELS_DB.get(city, [])
        # Lọc theo giá và sắp xếp theo rating giảm dần [cite: 206, 208]
        filtered = [h for h in hotels if h['price_per_night'] <= max_price_per_night]
        filtered.sort(key=lambda x: x['rating'], reverse=True)
        
        if not filtered:
            return f"Không tìm thấy khách sạn tại {city} với giá dưới {max_price_per_night:,}/đêm. Hãy thử tăng ngân sách." 
        
        res = f"Khách sạn tại {city} (ưu tiên đánh giá cao):\n"
        for h in filtered:
            res += f"- {h['name']} ({h['stars']} sao): {h['price_per_night']:,} VNĐ/đêm - Đánh giá: {h['rating']}\n"
        return res
    except Exception as e:
        return f"Lỗi hệ thống khi tìm khách sạn: {str(e)}"

@tool
# def calculate_budget(total_budget: int, expenses: str) -> str:
#     """Tính toán ngân sách còn lại từ chuỗi chi phí.""" 
#     try:
#         total_spent = 0
#         detail = ""
#         # Parse chuỗi: "vé: 100, khách: 200" [cite: 221, 227]
#         items = expenses.split(",")
#         for item in items:
#             name, price = item.split(":")
#             amount = int(re.sub(r'[^\d]', '', price))
#             total_spent += amount
#             detail += f"{name.strip()}: {amount:,} VNĐ\n"
            
#         remaining = total_budget - total_spent
#         status = f"Còn lại: {remaining:,} VNĐ" if remaining >= 0 else f"Vượt ngân sách {abs(remaining):,} VNĐ! Cần điều chỉnh." 
        
#         return f"Bảng chi phí:\n{detail}Tổng chi: {total_spent:,} VNĐ\nNgân sách: {total_budget:,} VNĐ\n{status}" 
#     except Exception:
#         return "Lỗi định dạng expenses. Hãy dùng định dạng 'tên: số tiền, ...'" 
def calculate_budget(total_budget: int, expenses: str) -> str:
    """Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: số nguyên (VD: 5000000)
    - expenses: chuỗi định dạng 'tên: số tiền', cách nhau bằng dấu phẩy.
      LƯU Ý: Số tiền phải là số nguyên viết liền, KHÔNG có dấu phẩy phân cách phần nghìn, KHÔNG kèm đơn vị VNĐ.
      VD ĐÚNG: 'vé máy bay: 1100000, khách sạn: 400000'
      """
    print(f"[LOG] Đang tính toán ngân sách: Tổng {total_budget:,} VNĐ...") # Thêm Logging khởi đầu
    try:
        total_spent = 0
        detail = ""
        # Parse chuỗi expenses thành dict (tên: số tiền) [cite: 227]
        items = expenses.split(",")
        for item in items:
            if ":" not in item:
                continue
            name, price = item.split(":")
            # Sử dụng regex để chỉ lấy chữ số, tránh lỗi khi user nhập "1.200.000đ" [cite: 249, 257]
            amount = int(re.sub(r'[^\d]', '', price))
            total_spent += amount
            detail += f"- {name.strip()}: {amount:,} VNĐ\n"
            print(f"  [LOG] Đã thêm khoản chi: {name.strip()} ({amount:,} VNĐ)") # Log chi tiết từng khoản

        remaining = total_budget - total_spent
        
        # Kiểm tra nếu vượt ngân sách [cite: 225, 250]
        if remaining >= 0:
            status = f"Ngân sách còn lại: {remaining:,} VNĐ"
            print(f"[LOG] Kết quả: Còn dư {remaining:,} VNĐ")
        else:
            status = f"VÀNH ĐAI ĐỎ: Vượt ngân sách {abs(remaining):,} VNĐ! Cần điều chỉnh."
            print(f"[LOG] CẢNH BÁO: Vượt ngân sách {abs(remaining):,} VNĐ")

        # Trả về bảng chi tiết theo yêu cầu format [cite: 233, 239-246]
        return (
            f"Bảng chi phí chi tiết:\n"
            f"{detail}"
            f"--------------------------\n"
            f"Tổng chi: {total_spent:,} VNĐ\n"
            f"Ngân sách ban đầu: {total_budget:,} VNĐ\n"
            f"{status}"
        )
    except Exception as e:
        print(f"[LOG] LỖI: Định dạng expenses không hợp lệ ({str(e)})") # Ghi chú lỗi Tool
        return "Lỗi: Vui lòng nhập chi phí theo định dạng 'tên khoản: số tiền, ...' (Ví dụ: vé máy bay: 1200000, khách sạn: 800000)"