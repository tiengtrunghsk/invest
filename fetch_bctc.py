import os
import requests
import json
import time

# Thư mục lưu dữ liệu BCTC chi tiết cho từng mã
OUTPUT_DIR = "bctc_data"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Danh sách mã VN100 mẫu (hoặc bạn lấy danh sách từ data.json của bạn)
SECTOR_MAPPING = {
    "NH": ["ACB", "BID", "CTG", "TCB", "MBB", "STB", "VPB", "HDB", "VIB", "TPB", "SHB", "SSB", "LPB", "MSB", "OCB", "EIB"],
    "CK": ["SSI", "VCI", "HCM", "VIX", "MBS", "FTS", "BSI", "CTS", "ORS"],
    "BDS": ["VHM", "VIC", "VRE", "NVL", "PDR", "DIG", "NLG", "KDH", "CEO", "DXG", "TCH", "HDG"],
    "BDS_KCN": ["KBC", "IDC", "SZC", "BCM", "PHR"],
    "THEP": ["HPG", "HSG", "NKG"],
    "XAYDUNG": ["CTD", "VCG", "HHV"],
    "CONGNGHE": ["FPT"],
    "BANLE": ["MWG", "PNJ", "FRT"],
    "THUCPHAM": ["VNM", "MSN", "SAB"],
    "DAUKHI": ["GAS", "PVD", "PVS", "BSR", "POW"],
    "VANTAI": ["GMD", "HAH", "PVT", "VJC", "HVN"],
    "KHAC": ["REE", "PC1", "NT2", "VHC", "ANV"]
}

def fetch_financial_reports(symbol):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    # API TCBS lấy dữ liệu BCTC theo năm/quý
    # type: 1 = Kết quả kinh doanh, 2 = Cân đối kế toán, 3 = Lưu chuyển tiền tệ trực tiếp, 4 = Lưu chuyển tiền tệ gián tiếp
    reports = {}
    
    try:
        # 1. Kết quả kinh doanh (Income Statement)
        url_income = f"https://apipubaws.tcbs.com.vn/tcs/v2/finance/{symbol}/income-statement?yearly=0&isAll=true"
        r = requests.get(url_income, headers=headers, timeout=5)
        if r.status_code == 200:
            reports['income_statement'] = r.json()

        # 2. Cân đối kế toán (Balance Sheet)
        url_balance = f"https://apipubaws.tcbs.com.vn/tcs/v2/finance/{symbol}/balance-sheet?yearly=0&isAll=true"
        r = requests.get(url_balance, headers=headers, timeout=5)
        if r.status_code == 200:
            reports['balance_sheet'] = r.json()

        # 3. Lưu chuyển tiền tệ (Cash Flow)
        url_cash = f"https://apipubaws.tcbs.com.vn/tcs/v2/finance/{symbol}/cash-flow?yearly=0&isAll=true"
        r = requests.get(url_cash, headers=headers, timeout=5)
        if r.status_code == 200:
            reports['cash_flow'] = r.json()

        file_path = os.path.join(OUTPUT_DIR, f"{symbol}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(reports, f, ensure_ascii=False, indent=4)
        
        print(f"✅ Đã cào xong BCTC cho mã: {symbol}")
    except Exception as e:
        print(f"❌ Lỗi cào mã {symbol}: {e}")

if __name__ == "__main__":
    print("🚀 Bắt đầu cào dữ liệu BCTC cho các mã VN100...")
    all_symbols = []
    for symbols in SECTOR_MAPPING.values():
        all_symbols.extend(symbols)
    
    for symbol in all_symbols:
        fetch_financial_reports(symbol)
        time.sleep(0.3) # Nghỉ nhẹ tránh bị chặn request
        
    print("\n🎉 Hoàn tất quá trình cào dữ liệu BCTC! Dữ liệu được lưu trong thư mục 'bctc_data'.")
