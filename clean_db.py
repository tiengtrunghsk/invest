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
    print("\n🚀 Bắt đầu dọn rác BCTC (Xóa ratio, lọc core IDs, cắt 8 kỳ)...")
    
    # 1. Xóa sạch mảng 'ratio' rác (dữ liệu VNDirect cũ 2013-2014) khỏi tất cả document
    result_ratio = bctc_col.update_many({}, {"$unset": {"ratio": ""}})
    print(f"✅ Đã xóa mảng 'ratio' khỏi {result_ratio.modified_count} mã.")

    CORE_IDS = [
        "IS_NET_REVENUE", "IS_COST_OF_GOODS_SOLD", "IS_NET_PROFIT_AFTER_TAX",
        "CF_NET_CASH_FLOWS_FROM_OPERATING_ACTIVITIES", "BS_TOTAL_ASSETS",
        "BS_SHORT_TERM_ASSETS", "BS_LONG_TERM_ASSETS", "BS_OWNERS_EQUITY", "BS_LIABILITIES"
    ]

    # 2. Pipeline dọn dẹp cấu trúc bên trong các mảng balance_sheet, income_statement, cash_flow
    # Lọc đúng ID cốt lõi, chỉ lấy 8 kỳ, và CHỈ GIỮ LẠI 3 TRƯỜNG (id, period, value)
    pipeline = [
        {
            "$project": {
                "balance_sheet": {
                    "$map": {
                        "input": {
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
                        "as": "doc",
                        "in": {
                            "id": "$$doc.id",
                            "period": "$$doc.period",
                            "value": "$$doc.value"
                        }
                    }
                },
                "income_statement": {
                    "$map": {
                        "input": {
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
                        "as": "doc",
                        "in": {
                            "id": "$$doc.id",
                            "period": "$$doc.period",
                            "value": "$$doc.value"
                        }
                    }
                },
                "cash_flow": {
                    "$map": {
                        "input": {
                            "$slice": [
                                {
                                    "$filter": {
                                        "input": "$cash_flow",
                                        "as": "item",
                                        "cond": { "$in": ["$$item.id", CORE_IDS] }
                                    }
                                }, 8
                            ]
                        },
                        "as": "doc",
                        "in": {
                            "id": "$$doc.id",
                            "period": "$$doc.period",
                            "value": "$$doc.value"
                        }
                    }
                }
            }
        }
    ]

    symbols = bctc_col.distinct("symbol")
    total = len(symbols)
    print(f"Tìm thấy {total} mã cần dọn dẹp cấu trúc.")

    for i, sym in enumerate(symbols, 1):
        try:
            res = list(bctc_col.aggregate([
                {"$match": {"symbol": sym}},
                *pipeline
            ]))
            
            if res:
                filtered_data = res[0]
                update_fields = {}
                if "balance_sheet" in filtered_data: update_fields["balance_sheet"] = filtered_data["balance_sheet"]
                if "income_statement" in filtered_data: update_fields["income_statement"] = filtered_data["income_statement"]
                if "cash_flow" in filtered_data: update_fields["cash_flow"] = filtered_data["cash_flow"]

                if update_fields:
                    bctc_col.update_one({"symbol": sym}, {"$set": update_fields})
            
            if i % 10 == 0 or i == total:
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
