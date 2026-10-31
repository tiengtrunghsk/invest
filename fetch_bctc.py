import os
import requests
import json
import time
import subprocess
import datetime

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
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://tcinvest.tcbs.com.vn/"
    }
    reports = {}
    
    try:
        # Thử gọi API tài chính gốc của TCBS
        url_income = f"https://apipubaws.tcbs.com.vn/tcs/v2/finance/{symbol}/income-statement?yearly=0&isAll=true"
        r1 = requests.get(url_income, headers=headers, timeout=6)
        
        if r1.status_code == 200:
            data_income = r1.json()
            if data_income:  # Chỉ nhận nếu có dữ liệu thực tế
                reports['income_statement'] = data_income

        url_balance = f"https://apipubaws.tcbs.com.vn/tcs/v2/finance/{symbol}/balance-sheet?yearly=0&isAll=true"
        r2 = requests.get(url_balance, headers=headers, timeout=6)
        
        if r2.status_code == 200:
            data_balance = r2.json()
            if data_balance:
                reports['balance_sheet'] = data_balance

        # Nếu cả 2 đều trống, thử gọi sang nguồn API dự phòng (VNDirect ratios/financials)
        if not reports:
            url_backup = f"https://api-finfo.vndirect.com.vn/v4/financialStatements?q=symbol:{symbol}~periodType:QUARTER&size=4"
            r3 = requests.get(url_backup, headers={"User-Agent": "Mozilla/5.0"}, timeout=6)
            if r3.status_code == 200:
                bk_data = r3.json().get("data", [])
                if bk_data:
                    reports['income_statement'] = bk_data

        # Kiểm tra lần cuối trước khi lưu
        if not reports:
            print(f"⚠️ Không có dữ liệu BCTC cho mã: {symbol}")
            return False

        file_path = os.path.join(OUTPUT_DIR, f"{symbol}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(reports, f, ensure_ascii=False, indent=4)
        
        print(f"✅ Đã cào xong BCTC cho mã: {symbol}")
        return True
    except Exception as e:
        print(f"❌ Lỗi mã {symbol}: {e}")
        return False

def auto_git_push_bctc():
    try:
        print("\n📤 Đang đồng bộ thư mục 'bctc_data' lên GitHub...")
        subprocess.run(["git", "add", OUTPUT_DIR], check=True)
        commit_msg = f"Auto update BCTC raw data - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push"], check=True)
        print("🚀 Đẩy dữ liệu BCTC lên GitHub thành công!")
    except Exception as e:
        print(f"ℹ️ Git push info: {e}")

def main():
    total = len(VN100_SYMBOLS)
    print(f"🚀 Bắt đầu cào dữ liệu BCTC thông minh cho {total} mã...")
    
    success = 0
    for i, symbol in enumerate(VN100_SYMBOLS):
        print(f"[{i+1}/{total}] Xử lý: {symbol}...")
        if fetch_financial_reports(symbol):
            success += 1
        time.sleep(0.4)
        
    print(f"\n🎉 Hoàn tất! Đã lưu thành công {success}/{total} file BCTC có dữ liệu.")
    auto_git_push_bctc()

if __name__ == "__main__":
    main()
