import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# 1. Cấu hình giao diện Web rộng rãi toàn màn hình
st.set_page_config(page_title="Dashboard Phân Tích Doanh Thu & Tồn Kho", layout="wide")
st.title('🚀 Hệ Thống Quản Trị: Doanh Thu & Rủi Ro Tồn Kho')
st.markdown("---")

# Nút upload file trực tiếp trên giao diện web
uploaded_file = st.file_uploader("Kéo thả file data (CSV/ZIP) vào đây để phân tích", type=['csv', 'zip'])

if uploaded_file is not None:
    # Đọc dữ liệu từ file được tải lên
   # 1. Đọc và làm sạch data (Thêm bộ dịch latin1 để trị dứt điểm lỗi font chữ/ký tự lạ)
   # Đọc data, giải mã ký tự lạ (latin1) và tự động BỎ QUA các dòng bị lỗi cột (on_bad_lines)
    df = pd.read_csv(uploaded_file, encoding='latin1', on_bad_lines='skip')
    
    # Tự động dọn dẹp khoảng trắng thừa ở tên các cột nếu có
    df.columns = df.columns.str.strip()
    
    # Ép kiểu dữ liệu cột tháng về dạng ngày tháng chuẩn cho AI học
    # Ép kiểu thời gian, nếu gặp dòng rác (chữ) thì chuyển thành lỗi vô danh (NaT)
    df['month'] = pd.to_datetime(df['month'], errors='coerce')
    
    # Xóa sạch những dòng rác không phải là ngày tháng để data sạch tinh tươm
    df = df.dropna(subset=['month'])
    
    # Phân chia giao diện thành 2 thẻ rõ ràng
    tab1, tab2 = st.tabs(["📈 Dự Báo Doanh Thu (Sales Forecast)", "⚠️ Rủi Ro Tồn Kho (Inventory Risk)"])
    
    # ==========================================
    # TAB 1: DỰ BÁO DOANH THU BẰNG MÔ HÌNH AI
    # ==========================================
    with tab1:
        st.header("Thuật toán dự báo: Exponential Smoothing (San bằng mũ)")
        
        # Lấy danh sách các chi nhánh thực tế từ file dữ liệu
        branches = df['to'].dropna().unique()
        branch = st.selectbox('Chọn chi nhánh để dự báo:', branches)
        
        # Lọc và tính tổng doanh thu theo từng tháng cho chi nhánh được chọn
        df_branch = df[df['to'] == branch]
        revenue = df_branch.groupby('month')['extended_retail'].sum().reset_index()
        revenue.set_index('month', inplace=True)
        
        # Đảm bảo các mốc thời gian liên tục đều đặn theo từng đầu tháng (Month Start)
        revenue = revenue.resample('MS').sum().fillna(0)
        data_length = len(revenue)
        
        # Điều kiện tối thiểu để mô hình toán học chạy ổn định
        if data_length >= 3:
            try:
                # Sử dụng cấu hình Holt's Linear Trend cực kỳ vững chắc, không lo lỗi thiếu chu kỳ mùa vụ
                model = ExponentialSmoothing(revenue['extended_retail'], trend='add', seasonal=None).fit()
                
                # Cho mô hình dự đoán số liệu 6 tháng tiếp theo trong tương lai
                forecast = model.forecast(6)
                
                # Tiến hành vẽ biểu đồ trực quan
                fig, ax = plt.subplots(figsize=(12, 5))
                ax.plot(revenue.index, revenue['extended_retail'], label='Thực tế quá khứ', marker='o', color='#8A2BE2', linewidth=2)
                ax.plot(forecast.index, forecast, label='AI Dự báo (6 tháng tới)', marker='x', color='#FF4500', linestyle='--', linewidth=2)
                
                ax.set_title(f'Biểu Đồ Biến Động và Dự Báo Doanh Thu - Chi nhánh {branch}', fontsize=14, fontweight='bold')
                st.write(f"Hệ thống ghi nhận: **{data_length} tháng** dữ liệu lịch sử.")
                ax.set_ylabel('Doanh thu (USD)')
                ax.set_xlabel('Thời gian')
                ax.grid(True, linestyle=':')
                ax.legend()
                st.pyplot(fig)
                
                # Xuất thêm bảng thống kê con số cụ thể cho dân kế toán dễ xem số
                st.subheader("📋 Chi tiết con số AI dự báo trong 6 tháng tới:")
                forecast_df = pd.DataFrame({
                    'Tháng tương lai': forecast.index.strftime('%Y-%m'), 
                    'Doanh thu dự báo ($)': forecast.values
                })
                st.dataframe(forecast_df.set_index('Tháng tương lai'), use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Có lỗi phát sinh khi xử lý mô hình AI: {e}")
        else:
            st.warning(f"⚠️ Chi nhánh {branch} chỉ có {data_length} tháng dữ liệu, quá ngắn để học xu hướng (Cần ít nhất 3 tháng dữ liệu).")

    # ==========================================
    # TAB 2: CẢNH BÁO KIỂM SOÁT RỦI RO TỒN KHO
    # ==========================================
    with tab2:
        st.header("Kiểm soát rủi ro luân chuyển hàng hóa")
        st.write("*(Dựa trên phân tích tổng khối lượng hàng đã bán và dòng vốn tồn kho)*")
        
        # Gom nhóm dữ liệu theo từng mã sản phẩm (SKU)
        sku_stats = df.groupby('sku').agg({
            'qty': 'sum',
            'extended_cost': 'sum'
        }).reset_index()
        
        # Chia đôi màn hình web thành 2 cột cân xứng
        col1, col2 = st.columns(2)
        
        with col1:
            st.error("🔴 RỦI RO ĐỌNG VỐN (Top 10 sản phẩm bán chậm nhất)")
            st.write("Những mặt hàng có lượng xuất kho thấp nhất hệ thống. Đề xuất kiểm tra chiến lược xả kho để giải phóng dòng tiền.")
            dong_von = sku_stats.sort_values('qty', ascending=True).head(10)
            dong_von.columns = ['Mã Sản Phẩm (SKU)', 'Tổng Lượng Đã Bán', 'Giá Vốn Đang Kẹt ($)']
            st.dataframe(dong_von, use_container_width=True)
            
        with col2:
            st.success("🔥 RỦI RO CHÁY HÀNG (Top 10 sản phẩm bán nhanh nhất)")
            st.write("Những mặt hàng đang tiêu thụ mạnh nhất. Cần chủ động lên kế hoạch nhập hàng gấp để tránh đứt gãy chuỗi cung ứng.")
            chay_hang = sku_stats.sort_values('qty', ascending=False).head(10)
            chay_hang.columns = ['Mã Sản Phẩm (SKU)', 'Tổng Lượng Đã Bán', 'Tổng Chi Phí Nhập ($)']
            st.dataframe(chay_hang, use_container_width=True)