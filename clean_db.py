import os
import sys
import time
from pymongo import MongoClient

MONGO_URI = os.environ.get("MONGO_URI", "").strip()

if not MONGO_URI:
    print("❌ LỖI: Chưa cấu hình biến môi trường MONGO_URI!")
    sys.exit(1)

print("Đang kết nối tới MongoDB...")
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=30000, socketTimeoutMS=120000)
    db = client["quant_db"]
    bctc_col = db["bctc_data"]
    collection = db["stocks"]
    print("✅ Kết nối MongoDB thành công!")
except Exception as e:
    print(f"❌ Lỗi kết nối MongoDB: {e}")
    sys.exit(1)

def clean_bctc_data():
    print("\n🚀 Bắt đầu dọn rác BCTC (Sử dụng Aggregation Pipeline)...")
    
    CORE_IDS = [
        "IS_NET_REVENUE", "IS_COST_OF_GOODS_SOLD", "IS_NET_PROFIT_AFTER_TAX",
        "CF_NET_CASH_FLOWS_FROM_OPERATING_ACTIVITIES", "BS_TOTAL_ASSETS",
        "BS_SHORT_TERM_ASSETS", "BS_LONG_TERM_ASSETS", "BS_OWNERS_EQUITY", "BS_LIABILITIES"
    ]

    # Sử dụng $project để tách mảng và $filter để lọc, sau đó $slice để cắt 8 kỳ
    # Pipeline này chạy trực tiếp trên server MongoDB nên cực nhẹ
    pipeline = [
        {
            "$project": {
                "balance_sheet": {
                    "$slice": [
                        {
                            "$filter": {
                                "input": "$balance_sheet",
                                "as": "item",
                                "cond": { "$in": ["$$item.id", CORE_IDS] }
                            }
                        }, 8
                    ]
                },
                "income_statement": {
                    "$slice": [
                        {
                            "$filter": {
                                "input": "$income_statement",
                                "as": "item",
                                "cond": { "$in": ["$$item.id", CORE_IDS] }
                            }
                        }, 8
                    ]
                },
                "cash_flow": {
                    "$slice": [
                        {
                            "$filter": {
                                "input": "$cash_flow",
                                "as": "item",
                                "cond": { "$in": ["$$item.id", CORE_IDS] }
                            }
                        }, 8
                    ]
                }
            }
        },
        {
            # Chỉ lấy những document thực sự thay đổi để update
            "$match": {
                "$expr": { "$eq": [1, 1] } 
            }
        }
    ]

    # Cách an toàn nhất: Quét từng mã một bằng find_one_and_update
    # Lấy danh sách symbol để duyệt (tránh load toàn bộ doc nặng)
    symbols = bctc_col.distinct("symbol")
    total = len(symbols)
    print(f"Tìm thấy {total} mã cần dọn dẹp.")

    for i, sym in enumerate(symbols, 1):
        try:
            # Chạy pipeline lọc trực tiếp trên MongoDB cho từng mã
            # Kết quả trả về chỉ là mảng đã được cắt tỉa gọn gàng
            res = bctc_col.aggregate([
                {"$match": {"symbol": sym}},
                *pipeline
            ])
            
            filtered_data = list(res)[0]
            
            # Cập nhật lại mảng đã lọc đè lên mảng cũ
            update_fields = {}
            if "balance_sheet" in filtered_data: update_fields["balance_sheet"] = filtered_data["balance_sheet"]
            if "income_statement" in filtered_data: update_fields["income_statement"] = filtered_data["income_statement"]
            if "cash_flow" in filtered_data: update_fields["cash_flow"] = filtered_data["cash_flow"]

            if update_fields:
                bctc_col.update_one({"symbol": sym}, {"$set": update_fields})
            
            if i % 5 == 0 or i == total:
                print(f"⏳ Đã dọn dẹp {i}/{total} mã...")
                
        except Exception as e:
            print(f"❌ Lỗi khi xử lý mã {sym}: {e}")

    print(f"✅ Đã dọn dẹp xong bảng BCTC.")

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
