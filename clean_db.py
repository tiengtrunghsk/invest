import os
import sys
import time
from datetime import datetime, timedelta
from pymongo import MongoClient

# ===================== CẤU HÌNH =====================
# Ưu tiên lấy từ biến môi trường (khi chạy trên Github Action)
MONGO_URI = os.environ.get("MONGO_URI", "").strip()

if not MONGO_URI:
    print("❌ LỖI: Chưa cấu hình biến môi trường MONGO_URI!")
    sys.exit(1)

print("Đang kết nối tới MongoDB...")
try:
    # Cấu hình timeout dài để thoải mái xử lý dữ liệu lớn
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=30000, socketTimeoutMS=120000)
    db = client["quant_db"]
    bctc_col = db["bctc_data"]
    collection = db["stocks"]
    print("✅ Kết nối MongoDB thành công!")
except Exception as e:
    print(f"❌ Lỗi kết nối MongoDB: {e}")
    sys.exit(1)

def clean_bctc_data():
    print("\n🚀 Bắt đầu dọn rác BCTC (Xóa VCI_..., cắt tỉa 8 kỳ)...")
    
    CORE_IDS = {
        "IS_NET_REVENUE", "IS_COST_OF_GOODS_SOLD", "IS_NET_PROFIT_AFTER_TAX",
        "CF_NET_CASH_FLOWS_FROM_OPERATING_ACTIVITIES", "BS_TOTAL_ASSETS",
        "BS_SHORT_TERM_ASSETS", "BS_LONG_TERM_ASSETS", "BS_OWNERS_EQUITY", "BS_LIABILITIES"
    }

    updated_count = 0
    processed_count = 0
    last_id = None
    batch_size = 20

    while True:
        query = {}
        if last_id is not None:
            query = {"_id": {"$gt": last_id}}
            
        docs = list(bctc_col.find(query).sort("_id", 1).limit(batch_size))
        
        if not docs:
            break

        for doc in docs:
            last_id = doc["_id"]
            processed_count += 1
            
            update_data = {}
            needs_update = False

            for report_key in ["balance_sheet", "income_statement", "cash_flow"]:
                if report_key in doc and isinstance(doc[report_key], list):
                    original_list = doc[report_key]
                    
                    # 1. Lọc bỏ rác
                    filtered_list = [item for item in original_list if item.get("id") in CORE_IDS]
                    
                    # 2. Cắt tỉa 8 kỳ
                    if filtered_list:
                        unique_periods = sorted(list(set([item["period"] for item in filtered_list])), reverse=True)
                        keep_periods = set(unique_periods[:8])
                        filtered_list = [item for item in filtered_list if item["period"] in keep_periods]
                    
                    if len(filtered_list) != len(original_list):
                        update_data[report_key] = filtered_list
                        needs_update = True

            if needs_update:
                bctc_col.update_one({"_id": doc["_id"]}, {"$set": update_data})
                updated_count += 1
        
        print(f"⏳ Đã quét qua {processed_count} documents (Đã sửa: {updated_count})...")
        time.sleep(0.5)

    print(f"✅ Đã dọn dẹp xong bảng BCTC. Tổng số sửa: {updated_count}/{processed_count}")

def clean_stocks_data():
    print("\n🧹 Đang dọn dẹp các trường rác trong bảng Giá (stocks)...")
    junk_fields = ["is_incomplete", "last_error_at", "chot_so_today", "ratio_updated_at"]
    unset_query = {field: "" for field in junk_fields}
    
    result = collection.update_many({}, {"$unset": unset_query})
    print(f"✅ Đã dọn dẹp {result.modified_count} mã trong bảng Giá (stocks).")

if __name__ == "__main__":
    start_time = time.time()
    clean_bctc_data()
    clean_stocks_data()
    elapsed = time.time() - start_time
    print(f"\n🏁 HOÀN TẤT QUÁ TRÌNH DỌN RÁC! Thời gian chạy: {elapsed:.2f} giây.")
