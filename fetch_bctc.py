import os
import requests
import json
import time
import subprocess
import datetime

# Thư mục lưu dữ liệu BCTC chi tiết cho từng mã
OUTPUT_DIR = "bctc_data"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Danh sách mã chuẩn đồng bộ chính xác với script chính
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
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    reports = {}
    
    try:
        # 1. Kết quả kinh doanh (Income Statement)
        url_income = f"https://apipubaws.tcbs.com.vn/tcs/v2/finance/{symbol}/income-statement?yearly=0&isAll=true"
        r = requests.get(url_income, headers=headers, timeout=8)
        if r.status_code == 200:
            reports['income_statement'] = r.json()

        # 2. Cân đối kế toán (Balance Sheet)
        url_balance = f"https://apipubaws.tcbs.com.vn/tcs/v2/finance/{symbol}/balance-sheet?yearly=0&isAll=true"
        r = requests.get(url_balance, headers=headers, timeout=8)
        if r.status_code == 200:
            reports['balance_sheet'] = r.json()

        # 3. Lưu chuyển tiền tệ (Cash Flow)
        url_cash = f"https://apipubaws.tcbs.com.vn/tcs/v2/finance/{symbol}/cash-flow?yearly=0&isAll=true"
        r = requests.get(url_cash, headers=headers, timeout=8)
        if r.status_code == 200:
            reports['cash_flow'] = r.json()

        # Lưu file riêng cho từng mã vào bctc_data/
        file_path = os.path.join(OUTPUT_DIR, f"{symbol}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(reports, f, ensure_ascii=False, indent=4)
        
        return True
    except Exception as e:
        print(f"⚠️ Lỗi cào BCTC mã {symbol}: {e}")
        return False

def auto_git_push_bctc():
    """Đồng bộ thư mục bctc_data lên GitHub Pages"""
    try:
        print("\n📤 Đang tiến hành đồng bộ thư mục 'bctc_data' lên GitHub...")
        subprocess.run(["git", "add", OUTPUT_DIR], check=True)
        commit_msg = f"Auto update BCTC raw data - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push"], check=True)
        print("🚀 Đẩy dữ liệu BCTC lên GitHub thành công!")
    except subprocess.CalledProcessError:
        print("ℹ️ Git: Không có thay đổi mới để push hoặc đã được cập nhật.")
    except Exception as e:
        print(f"⚠️ Lỗi Git push: {e}")

def main():
    total = len(VN100_SYMBOLS)
    print(f"🚀 Bắt đầu cào dữ liệu BCTC cho {total} mã cổ phiếu...")
    
    success_count = 0
    for i, symbol in enumerate(VN100_SYMBOLS):
        print(f"[{i+1}/{total}] Đang tải BCTC: {symbol}...")
        if fetch_financial_reports(symbol):
            success_count += 1
        
        # Nghỉ ngắn giữa các request để tránh bị API giới hạn
        time.sleep(0.4)
        
    print(f"\n✅ Hoàn tất! Đã lưu thành công {success_count}/{total} file BCTC vào thư mục '{OUTPUT_DIR}'.")
    
    # Đẩy lên GitHub
    auto_git_push_bctc()

if __name__ == "__main__":
    main()
