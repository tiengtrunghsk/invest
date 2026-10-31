import os
import json
import time
import subprocess
import datetime
from vnstock import Stock

OUTPUT_DIR = "bctc_data"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

VN100_SYMBOLS = [
    "ACB", "BID", "CTG", "TCB", "MBB", "STB", "VPB", "HDB", "VIB", "TPB",
    "SHB", "SSB", "LPB", "MSB", "OCB", "EIB", "SSI", "VCI", "HCM", "VIX",
    "MBS", "FTS", "BSI", "CTS", "ORS", "VHM", "VIC", "VRE", "NVL", "PDR",
    "DIG", "NLG", "KDH", "CEO", "DXG", "TCH", "HDG", "KBC", "IDC", "SZC",
    "BCM", "PHR", "HPG", "HSG", "NKG", "CTD", "VCG", "HHV", "FPT", "MWG",
    "PNJ", "FRT", "VNM", "MSN", "SAB", "GAS", "PVD", "PVS", "BSR", "POW",
    "REE", "PC1", "NT2", "GMD", "HAH", "PVT", "VJC", "HVN", "VHC", "ANV"
]

def fetch_financial_reports(symbol):
    try:
        # Khởi tạo đối tượng Stock từ vnstock (sguồn TCBS hoặc VCI)
        stock = Stock(symbol=symbol, source='TCBS')
        
        reports = {}
        # Lấy báo cáo kết quả kinh doanh, cân đối kế toán, lưu chuyển tiền tệ qua vnstock
        # (Tùy phiên bản vnstock bạn đang dùng, gọi hàm lấy finance tương ứng)
        income_df = stock.finance.income_statement(period='quarter')
        balance_df = stock.finance.balance_sheet(period='quarter')
        cash_df = stock.finance.cash_flow(period='quarter')
        
        reports['income_statement'] = income_df.to_dict(orient='records') if income_df is not None else []
        reports['balance_sheet'] = balance_df.to_dict(orient='records') if balance_df is not None else []
        reports['cash_flow'] = cash_df.to_dict(orient='records') if cash_df is not None else []

        if not reports['income_statement']:
            print(f"⚠️ Không có dữ liệu BCTC cho mã: {symbol}")
            return False

        file_path = os.path.join(OUTPUT_DIR, f"{symbol}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(reports, f, ensure_ascii=False, indent=4)
        
        print(f"✅ Đã cào xong BCTC cho mã: {symbol}")
        return True
    except Exception as e:
        print(f"❌ Lỗi cào BCTC mã {symbol}: {e}")
        return False

def auto_git_push_bctc():
    try:
        print("\n📤 Đang đồng bộ thư mục 'bctc_data' lên GitHub...")
        subprocess.run(["git", "add", OUTPUT_DIR], check=True)
        commit_msg = f"Auto update BCTC data - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push"], check=True)
        print("🚀 Đẩy dữ liệu BCTC lên GitHub thành công!")
    except Exception as e:
        print(f"ℹ️ Git push info: {e}")

def main():
    total = len(VN100_SYMBOLS)
    print(f"🚀 Bắt đầu cào BCTC cho {total} mã...")
    
    success = 0
    for i, symbol in enumerate(VN100_SYMBOLS):
        print(f"[{i+1}/{total}] Xử lý: {symbol}...")
        if fetch_financial_reports(symbol):
            success += 1
        time.sleep(0.5)
        
    print(f"\n🎉 Hoàn tất! Thành công {success}/{total} mã.")
    auto_git_push_bctc()

if __name__ == "__main__":
    main()
