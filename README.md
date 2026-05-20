# BTL

## Chạy ứng dụng

Ứng dụng sử dụng `streamlit` để hiển thị bảng điều khiển phân tích doanh thu và rủi ro tồn kho.

### Cài đặt phụ thuộc

```bash
python3 -m pip install streamlit pandas matplotlib statsmodels
```

### Chạy ứng dụng

```bash
streamlit run app.py
```

Sau khi chạy, bạn sẽ thấy trong terminal thông báo kiểu:

```bash
Local URL: http://localhost:8501
Network URL: http://127.0.0.1:8501
```

Mở trình duyệt theo đường dẫn được in ra trong terminal (thường là `http://localhost:8501`).

### Giao diện web sẽ gồm

- Tiêu đề chính: `🚀 Hệ Thống Quản Trị: Doanh Thu & Rủi Ro Tồn Kho`
- Widget tải file CSV/ZIP lên
- 2 tab:
  - `📈 Dự Báo Doanh Thu (Sales Forecast)`
  - `⚠️ Rủi Ro Tồn Kho (Inventory Risk)`
- Tab dự báo chứa:
  - chọn chi nhánh
  - biểu đồ doanh thu quá khứ và dự báo 6 tháng
  - bảng chi tiết dự báo
- Tab rủi ro tồn kho chứa:
  - bảng top 10 mặt hàng bán chậm nhất
  - bảng top 10 mặt hàng bán nhanh nhất

### Cách dùng

- Tải file `bookstore_inventory.csv` lên qua giao diện.
- Chọn chi nhánh để xem dự báo doanh thu và cảnh báo tồn kho.

## Tự động tạo kết quả README

Để `README.md` luôn hiển thị kết quả đã chạy sẵn khi chia sẻ link, cần tạo kết quả tĩnh trước khi đẩy repo lên GitHub.

1. Cài phụ thuộc:

```bash
python3 -m pip install -r requirements.txt
```

2. Chạy script tạo kết quả:

```bash
python3 generate_readme.py
```

3. Kiểm tra nội dung `README.md`, rồi commit và push:

```bash
git add README.md
git commit -m "Update README with generated app results"
git push
```

> Khi người khác mở link GitHub, họ sẽ thấy `README.md` đã chứa kết quả chạy sẵn.

## Kết quả mẫu từ dataset hiện tại

<!-- RESULTS_START -->

### Dự báo doanh thu 6 tháng tiếp theo

- `YYC-DT`
  - 2025-01-01: 52,272.35
  - 2025-02-01: 52,409.95
  - 2025-03-01: 52,547.54
  - 2025-04-01: 52,685.14
  - 2025-05-01: 52,822.73
  - 2025-06-01: 52,960.33

- `YYC-NW`
  - 2025-01-01: 35,316.84
  - 2025-02-01: 35,424.41
  - 2025-03-01: 35,531.99
  - 2025-04-01: 35,639.56
  - 2025-05-01: 35,747.14
  - 2025-06-01: 35,854.71

- `YYC-SE`
  - 2025-01-01: 28,762.50
  - 2025-02-01: 28,833.83
  - 2025-03-01: 28,905.17
  - 2025-04-01: 28,976.51
  - 2025-05-01: 29,047.85
  - 2025-06-01: 29,119.18

### Cảnh báo rủi ro tồn kho

- Top 5 sản phẩm bán chậm nhất (rủi ro đọng vốn):
  1. `BK1029` - 2699 đơn vị - 38,325.80 $
  2. `BK1042` - 2746 đơn vị - 38,169.40 $
  3. `BK1046` - 2750 đơn vị - 44,110.00 $
  4. `BK1094` - 2752 đơn vị - 20,805.12 $
  5. `BK1047` - 2760 đơn vị - 39,661.20 $

- Top 5 sản phẩm bán nhanh nhất (rủi ro cháy hàng):
  1. `BK1066` - 3168 đơn vị - 56,295.36 $
  2. `BK1036` - 3114 đơn vị - 31,669.38 $
  3. `BK1017` - 3100 đơn vị - 50,685.00 $
  4. `BK1032` - 3091 đơn vị - 36,906.54 $
  5. `BK1057` - 3084 đơn vị - 30,901.68 $

<!-- RESULTS_END -->
