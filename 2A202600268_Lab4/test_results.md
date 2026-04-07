# BÁO CÁO KẾT QUẢ KIỂM THỬ AI AGENT - LAB 4

### Test 1: Direct Answer (Không cần tool)
**Người dùng:** `Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.`

#### 🛠 Luồng suy luận (Execution Trace):

**✅ TravelBuddy phản hồi:**
> Chào bạn! Tuyệt vời quá, đi du lịch luôn là một quyết định hay. Bạn có ý định đến đâu hay có sở thích nào đặc biệt không? Nếu bạn cần một số gợi ý, mình có thể giới thiệu đến các điểm đến nổi tiếng như Hà Nội, Hồ Chí Minh, Đà Nẵng, hay Phú Quốc. Bạn có ngân sách cụ thể nào cho chuyến đi này không?

---

### Test 2: Single Tool Call (Tra cứu chuyến bay)
**Người dùng:** `Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng`

#### 🛠 Luồng suy luận (Execution Trace):
- 🔧 **Gọi công cụ**: `search_flights`
  - Tham số: `{'origin': 'Hà Nội', 'destination': 'Đà Nẵng'}`
  - 📥 **Kết quả Tool**: 
  ```text
  Các chuyến bay từ Hà Nội đến Đà Nẵng:
- Vietnam Airlines (06:00): 1,450,000 VNĐ (economy)
- Vietnam Airlines (14:00): 2,800,000 VNĐ (business)
- VietJet Air (08:30): 890,000 VNĐ (economy)
- Bamboo Airways (11:00): 1,200,000 VNĐ (economy)

  ```

**✅ TravelBuddy phản hồi:**
> Tôi đã tìm thấy một số chuyến bay từ Hà Nội đến Đà Nẵng cho bạn:

1. Vietnam Airlines (06:00): 1,450,000 VNĐ (hạng phổ thông)
2. VietJet Air (08:30): 890,000 VNĐ (hạng phổ thông)
3. Bamboo Airways (11:00): 1,200,000 VNĐ (hạng phổ thông)
4. Vietnam Airlines (14:00): 2,800,000 VNĐ (hạng thương gia)

Nếu bạn cần thêm thông tin về các chuyến bay hoặc muốn đặt vé, hãy cho tôi biết nhé!

---

### Test 3: Multi-Step Tool Chaining (Hành trình phức tạp)
**Người dùng:** `Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!`

#### 🛠 Luồng suy luận (Execution Trace):

**✅ TravelBuddy phản hồi:**
> Rất vui được hỗ trợ bạn! Để lên kế hoạch cho chuyến đi của bạn, mình sẽ tìm chuyến bay từ Hà Nội đến Phú Quốc và tìm khách sạn phù hợp với ngân sách của bạn.

Mình sẽ kiểm tra các chuyến bay trước nhé!

---

### Test 4: Missing Info (Hỏi lại thông tin)
**Người dùng:** `Tôi muốn đặt khách sạn`

#### 🛠 Luồng suy luận (Execution Trace):

**✅ TravelBuddy phản hồi:**
> Chắc chắn rồi! Bạn có thể cho mình biết địa điểm mà bạn muốn đặt khách sạn và ngân sách của bạn là bao nhiêu không?

---

### Test 5: Guardrail (Từ chối ngoài phạm vi)
**Người dùng:** `Giải giúp tôi bài tập lập trình Python về linked list`

#### 🛠 Luồng suy luận (Execution Trace):

**✅ TravelBuddy phản hồi:**
> Xin lỗi, nhưng mình không thể giúp bạn với bài tập lập trình. Tuy nhiên, nếu bạn có câu hỏi về du lịch hoặc cần hỗ trợ đặt vé máy bay, khách sạn, mình luôn sẵn sàng giúp bạn!

---

### Test 6: Reverse Flight Lookup
**Người dùng:** `Tôi đang ở Phú Quốc và muốn về lại Hà Nội, tìm giúp tôi chuyến bay rẻ nhất.`

#### 🛠 Luồng suy luận (Execution Trace):

**✅ TravelBuddy phản hồi:**
> Hiện tại hệ thống chưa hỗ trợ tìm kiếm chuyến bay từ Phú Quốc. Tuy nhiên, tôi có thể giúp bạn tìm chuyến bay từ Hà Nội đến các điểm đến khác như Hà Nội, Hồ Chí Minh, Đà Nẵng và Phú Quốc. Bạn có muốn tìm chuyến bay đến một trong những điểm đến này không?

---

### Test 7: Extreme Low Budget
**Người dùng:** `Tôi muốn đi Đà Nẵng từ HCM, tổng ngân sách chỉ có 800k cho cả vé máy bay và khách sạn 1 đêm.`

#### 🛠 Luồng suy luận (Execution Trace):
- 🔧 **Gọi công cụ**: `search_flights`
  - Tham số: `{'origin': 'Hồ Chí Minh', 'destination': 'Đà Nẵng'}`
- 🔧 **Gọi công cụ**: `search_hotels`
  - Tham số: `{'city': 'Đà Nẵng', 'max_price_per_night': 800000}`
  - 📥 **Kết quả Tool**: 
  ```text
  Các chuyến bay từ Hồ Chí Minh đến Đà Nẵng:
- Vietnam Airlines (09:00): 1,300,000 VNĐ (economy)
- VietJet Air (13:00): 780,000 VNĐ (economy)

  ```
  - 📥 **Kết quả Tool**: 
  ```text
  Khách sạn tại Đà Nẵng (ưu tiên đánh giá cao):
- Christina's Homestay (2 sao): 350,000 VNĐ/đêm - Đánh giá: 4.7
- Memory Hostel (2 sao): 250,000 VNĐ/đêm - Đánh giá: 4.6
- Fivitel Danang (3 sao): 650,000 VNĐ/đêm - Đánh giá: 4.1

  ```
- 🔧 **Gọi công cụ**: `calculate_budget`
  - Tham số: `{'total_budget': 800000, 'expenses': 'vé máy bay: 780000, khách sạn: 350000'}`
  - 📥 **Kết quả Tool**: 
  ```text
  Bảng chi phí chi tiết:
- vé máy bay: 780,000 VNĐ
- khách sạn: 350,000 VNĐ
--------------------------
Tổng chi: 1,130,000 VNĐ
Ngân sách ban đầu: 800,000 VNĐ
VÀNH ĐAI ĐỎ: Vượt ngân sách 330,000 VNĐ! Cần điều chỉnh.
  ```

**✅ TravelBuddy phản hồi:**
> Chào bạn! Mình đã tìm hiểu thông tin cho chuyến đi từ Hồ Chí Minh đến Đà Nẵng như sau:

- **Chuyến bay**: 
  - VietJet Air (13:00): 780,000 VNĐ (economy)

- **Khách sạn**:
  - Christina's Homestay (2 sao): 350,000 VNĐ/đêm - Đánh giá: 4.7
  - Memory Hostel (2 sao): 250,000 VNĐ/đêm - Đánh giá: 4.6

Tuy nhiên, tổng chi phí cho chuyến đi sẽ là 1,130,000 VNĐ (vé máy bay: 780,000 VNĐ + khách sạn: 350,000 VNĐ), vượt quá ngân sách của bạn là 800,000 VNĐ.

Để điều chỉnh ngân sách, bạn có thể lựa chọn:
1. Chọn khách sạn giá rẻ hơn như Memory Hostel với giá 250,000 VNĐ/đêm.
2. Hoặc tìm chuyến bay với giá thấp hơn nếu có (mình sẽ thử xem thêm nếu cần).

Để mình giúp bạn tìm cách tối ưu hơn nhé!

---

### Test 8: Quality Priority (Rating)
**Người dùng:** `Tìm cho tôi khách sạn tốt nhất ở Quận 1, Hồ Chí Minh. Tôi không quan tâm về giá, chỉ cần rating cao nhất.`

#### 🛠 Luồng suy luận (Execution Trace):
- 🔧 **Gọi công cụ**: `search_hotels`
  - Tham số: `{'city': 'Hồ Chí Minh', 'max_price_per_night': 99999999}`
  - 📥 **Kết quả Tool**: 
  ```text
  Khách sạn tại Hồ Chí Minh (ưu tiên đánh giá cao):
- The Common Room (2 sao): 180,000 VNĐ/đêm - Đánh giá: 4.6
- Cochin Zen Hotel (3 sao): 550,000 VNĐ/đêm - Đánh giá: 4.4
- Rex Hotel (5 sao): 2,800,000 VNĐ/đêm - Đánh giá: 4.3
- Liberty Central (4 sao): 1,400,000 VNĐ/đêm - Đánh giá: 4.1

  ```

**✅ TravelBuddy phản hồi:**
> Dưới đây là gợi ý cho khách sạn tốt nhất tại Quận 1, Hồ Chí Minh mà không quan tâm đến giá:

- **Khách sạn**: The Common Room
- **Giá**: 180,000 VNĐ/đêm
- **Đánh giá**: 4.6/5

Nếu bạn cần thêm thông tin hoặc có nhu cầu khác, cứ cho mình biết nhé!

---

### Test 9: Missing Destination
**Người dùng:** `Tôi muốn đi du lịch Nha Trang, tư vấn giúp tôi vé máy bay và khách sạn.`

#### 🛠 Luồng suy luận (Execution Trace):

**✅ TravelBuddy phản hồi:**
> Hiện tại, hệ thống chưa hỗ trợ địa điểm Nha Trang. Nhưng không sao, mình có thể gợi ý cho bạn những điểm đến khác ở Việt Nam như Hà Nội, Hồ Chí Minh, Đà Nẵng hoặc Phú Quốc. Bạn có muốn đi tới một trong những địa điểm này không?

---

### Test 10: Complex Expenses
**Người dùng:** `Tính giúp tôi xem còn dư bao nhiêu: Tổng ngân sách 10 triệu, đã chi: vé máy bay 2tr2, khách sạn 1tr5, ăn uống 2tr, tiền taxi 500k.`

#### 🛠 Luồng suy luận (Execution Trace):
- 🔧 **Gọi công cụ**: `calculate_budget`
  - Tham số: `{'total_budget': 10000000, 'expenses': 'vé máy bay: 2200000, khách sạn: 1500000, ăn uống: 2000000, tiền taxi: 500000'}`
  - 📥 **Kết quả Tool**: 
  ```text
  Bảng chi phí chi tiết:
- vé máy bay: 2,200,000 VNĐ
- khách sạn: 1,500,000 VNĐ
- ăn uống: 2,000,000 VNĐ
- tiền taxi: 500,000 VNĐ
--------------------------
Tổng chi: 6,200,000 VNĐ
Ngân sách ban đầu: 10,000,000 VNĐ
Ngân sách còn lại: 3,800,000 VNĐ
  ```

**✅ TravelBuddy phản hồi:**
> Ngân sách của bạn còn lại là 3.800.000 VNĐ sau khi đã chi cho các khoản như sau:

- Vé máy bay: 2.200.000 VNĐ
- Khách sạn: 1.500.000 VNĐ
- Ăn uống: 2.000.000 VNĐ
- Tiền taxi: 500.000 VNĐ

Tổng chi phí đã tiêu là 6.200.000 VNĐ. Nếu cần thêm thông tin gì khác, bạn cứ hỏi nhé!

---

