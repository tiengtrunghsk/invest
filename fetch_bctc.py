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
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    reports = {}
    
    try:
        # Sử dụng API finfo của VNDirect để lấy dữ liệu tài chính (Báo cáo kết quả kinh doanh / Cân đối kế toán)
        url = "https://api-finfo.vndirect.com.vn/v4/financialStatements"
        
        # Lấy Kết quả kinh doanh (INCOME_STATEMENT) và Cân đối kế toán (BALANCE_SHEET) theo Quý
        for report_type in ["INCOME_STATEMENT", "BALANCE_SHEET"]:
            params = {
                "q": f"code:{symbol}~reportType:{report_type}~periodType:QUARTER",
                "size": 8,  # Lấy 8 quý gần nhất
                "sort": "yearReport:desc,lengthReport:desc"
            }
            r = requests.get(url, params=params, headers=headers, timeout=8)
            if r.status_code == 200:
                data = r.json().get("data", [])
                if report_type == "INCOME_STATEMENT":
                    reports['income_statement'] = data
                else:
                    reports['balance_sheet'] = data

        if not reports.get('income_statement') and not reports.get('balance_sheet'):
            print(f"⚠️ Không lấy được dữ liệu BCTC cho mã: {symbol}")
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
        commit_msg = f"Auto update BCTC raw data - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push"], check=True)
        print("🚀 Đẩy dữ liệu BCTC lên GitHub thành công!")
    except Exception as e:
        print(f"ℹ️ Git push info: {e}")

def main():
    total = len(VN100_SYMBOLS)
    print(f"🚀 Bắt đầu cào dữ liệu BCTC cho {total} mã cổ phiếu...")
    
    success = 0
    for i, symbol in enumerate(VN100_SYMBOLS):
        print(f"[{i+1}/{total}] Xử lý: {symbol}...")
        if fetch_financial_reports(symbol):
            success += 1
        time.sleep(0.3)
        
    print(f"\n🎉 Hoàn tất! Đã lưu thành công {success}/{total} file BCTC.")
    auto_git_push_bctc()

if __name__ == "__main__":
    main()
