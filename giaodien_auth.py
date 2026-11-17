# -*- coding: utf-8 -*-
"""giaodien_auth.py — Module xác thực & quản trị (All-in-One)."""

import json

def build_auth_lite_css():
    return r"""
    <style>
        /* 1. LỚP ĐEN (LAYER 1) - PHỦ KÍN 100% MÀN HÌNH */
        #authOverlay {
            position: fixed !important;
            inset: 0 !important;
            width: 100% !important;
            min-height: 100vh !important;
            min-height: 100dvh !important;
            z-index: 99999999 !important;
            background: #0f172a !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            padding: max(1rem, env(safe-area-inset-top)) max(1rem, env(safe-area-inset-right)) max(1rem, env(safe-area-inset-bottom)) max(1rem, env(safe-area-inset-left)) !important;
            box-sizing: border-box !important;
            opacity: 1;
            visibility: visible;
            pointer-events: auto;
            transition: opacity 0.28s ease, visibility 0s linear 0s;
            overflow-x: hidden !important;
            overflow-y: auto !important;
            overscroll-behavior: contain;
            -webkit-overflow-scrolling: touch;
        }
        #authOverlay.hidden {
            opacity: 0 !important;
            visibility: hidden !important;
            pointer-events: none !important;
            transition: opacity 0.28s ease, visibility 0s linear 0.28s;
        }

        /* Khóa cuộn nền nhưng không cố định body (tránh giật vị trí trên iOS). */
        body.auth-locked {
            overflow: hidden !important;
            overscroll-behavior: none;
            width: 100% !important;
        }

        /* 3. HỘP ĐĂNG NHẬP CĂN GIỮA */
        .auth-box { 
            background: linear-gradient(145deg, #1e293b, #0f172a); 
            border: 1px solid rgba(51, 65, 85, 0.8); 
            border-radius: 20px; 
            width: 100%; 
            max-width: 400px; 
            padding: 2.5rem 2rem; 
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8), 0 0 0 1px rgba(255, 255, 255, 0.05); 
            text-align: center; 
            color: #f1f5f9; 
            box-sizing: border-box;
            margin: auto !important;
            max-height: calc(100vh - 2rem);
            max-height: calc(100dvh - 2rem);
            overflow-y: auto;
            overscroll-behavior: contain;
            -webkit-overflow-scrolling: touch;
            transform: translateY(0) scale(1);
            transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1);
        }
        
        #authOverlay.hidden .auth-box { transform: translateY(8px) scale(0.985); }
        
        .auth-title { font-size: 1.35rem; font-weight: 800; margin-bottom: 0.5rem; color: #fff; letter-spacing: -0.025em; }
        .auth-sub { font-size: 0.85rem; color: #94a3b8; margin-bottom: 1.75rem; line-height: 1.5; }
        
        .btn-google { 
            display: flex; align-items: center; justify-content: center; gap: 0.75rem; 
            width: 100%; padding: 0.85rem; border-radius: 12px; 
            border: 1px solid #475569; background: #0f172a; color: #fff; 
            font-weight: 600; font-size: 0.9rem; cursor: pointer; 
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1); 
            margin-bottom: 1rem; 
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }
        .btn-google:hover { background: #1e293b; border-color: #64748b; transform: translateY(-1px); }
        
        .auth-divider { display: flex; align-items: center; gap: 0.75rem; margin: 1.25rem 0; color: #64748b; font-size: 0.75rem; font-weight: 600; }
        .auth-divider::before, .auth-divider::after { content: ''; flex: 1; height: 1px; background: #334155; }
        
        .auth-input { 
            width: 100%; padding: 0.85rem 1rem; border-radius: 12px; 
            border: 1px solid #334155; background: rgba(15, 23, 42, 0.6); 
            color: #fff; font-size: 0.9rem; outline: none; margin-bottom: 0.85rem; 
            box-sizing: border-box; transition: all 0.2s ease; 
        }
        .auth-input:focus { 
            border-color: #10b981; 
            background: rgba(15, 23, 42, 0.9);
            box-shadow: 0 0 0 3px rgba(16,185,129,0.15); 
        }
        
        .auth-btn { 
            width: 100%; padding: 0.85rem; border-radius: 12px; 
            background: #10b981; color: #fff; font-weight: 700; font-size: 0.9rem; 
            border: none; cursor: pointer; display: flex; align-items: center; 
            justify-content: center; gap: 0.5rem; box-sizing: border-box; 
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
        }
        .auth-btn:hover { background: #059669; transform: translateY(-1px); }
        
        .auth-link { color: #38bdf8; font-size: 0.8rem; cursor: pointer; background: none; border: none; padding: 0; margin-top: 0.75rem; text-decoration: none; }
        .auth-link:hover { color: #7dd3fc; text-decoration: underline; }
        
        .auth-msg { padding: 0.85rem; border-radius: 10px; font-size: 0.8rem; margin-top: 1rem; display: none; text-align: left; }
        .auth-msg.show { display: block; }
        .auth-msg.error { background: rgba(244,63,94,.12); color: #fda4af; border: 1px solid rgba(244,63,94,.25); }
        .auth-msg.success { background: rgba(16,185,129,.12); color: #6ee7b7; border: 1px solid rgba(16,185,129,.25); }

        /* 4. MODAL GIA HẠN (VÁ LỖ HỔNG BẰNG NỀN ĐEN ĐẶC) */
        #renewalModal { 
            position: fixed; inset: 0; z-index: 10000001; 
            background: #0f172a !important; 
            backdrop-filter: blur(12px);
            display: none; align-items: center; justify-content: center; 
            padding: 1rem; font-family: system-ui, -apple-system, sans-serif; 
            overflow-y: auto; 
        }
        #renewalModal.show { display: flex; }
        
        .renewal-box { background: #1e293b; border: 1px solid #334155; border-radius: 20px; width: 100%; max-width: 450px; padding: 2rem; text-align: center; position: relative; box-shadow: 0 20px 40px -10px rgba(0,0,0,0.8); margin: auto; max-height: 95vh; overflow-y: auto; }
        .renewal-icon { width: 64px; height: 64px; border-radius: 50%; background: rgba(244,63,94,0.15); color: #f43f5e; display: flex; align-items: center; justify-content: center; font-size: 1.75rem; margin: 0 auto 1rem; border: 2px solid rgba(244,63,94,0.3); }
        .package-item { border: 1px solid #475569; border-radius: 8px; padding: 12px; margin-bottom: 8px; cursor: pointer; text-align: left; transition: 0.2s; display: flex; justify-content: space-between; align-items: center; background: #0f172a; }
        .package-item:hover { border-color: #64748b; }
        .package-item.active { border-color: #10b981; background: rgba(16,185,129,0.1); }
        .bank-info { background: #0f172a; border: 1px dashed #334155; border-radius: 12px; padding: 1rem; margin: 1rem 0; text-align: left; font-size: 0.85rem; }
        .bank-row { display: flex; justify-content: space-between; margin-bottom: 0.5rem; align-items: center; }
        .bank-row:last-child { margin-bottom: 0; }
        .bank-row span:first-child { color: #94a3b8; }
        .bank-row span:last-child { font-weight: 700; color: #fff; }
        .code-highlight { color: #10b981 !important; font-family: monospace; font-size: 1.1rem; letter-spacing: 1px; background: rgba(16,185,129,0.1); padding: 2px 8px; border-radius: 4px; }
    </style>
    """

def build_auth_lite_html(config, admin_tools_html=""):
    bank = config.get("bank_config", {})
    packages = config.get("packages", [])
    packages_html = ""
    for p in packages:
        save_badge = f'<span style="background:#10b981;color:#fff;font-size:10px;padding:2px 6px;border-radius:4px;margin-left:8px;">{p["save"]}</span>' if p.get("save") else ""
        packages_html += f"""
        <div onclick="selectPackage('{p['id']}', {p['amount']}, '{p['label']}', {p.get('days', 30)})" class="package-item" id="pkg_{p['id']}">
            <div><div style="font-weight:bold; color:#fff; font-size:0.9rem;">{p['label']} {save_badge}</div></div>
            <div style="color:#10b981; font-weight:bold;">{p['amount']:,}đ</div>
        </div>
        """
    return f"""
    <!-- Thẻ ẩn lưu hạn dùng -->
    <span id="hiddenExpireDate" style="display:none;">Đang tải...</span>

    <!-- ========================================== -->
    <!-- LAYER 1: MODAL ĐĂNG NHẬP -->
    <!-- ========================================== -->
    <div id="authOverlay">
        <div class="auth-box">
            <!-- LOGO & TIÊU ĐỀ -->
            <div class="flex flex-col items-center justify-center mb-5">
                <div class="bg-emerald-600 text-white p-3 rounded-xl shadow-lg shadow-emerald-500/30 mb-3">
                    <i class="fa-solid fa-scale-balanced text-2xl"></i>
                </div>
                <h1 class="text-xl font-black text-white tracking-wide">PRO QUANT SCREENER</h1>
                <p class="text-[11px] text-emerald-400 font-semibold tracking-widest uppercase mt-1">Hệ thống AI Thị trường Chứng khoán</p>
            </div>

            <!-- ƯU ĐÃI DÙNG THỬ -->
            <div class="bg-emerald-500/10 border border-emerald-500/30 rounded-xl p-3 mb-6 flex flex-col items-center justify-center gap-1">
                <span class="text-xs font-bold text-emerald-300"><i class="fa-solid fa-gift mr-1.5"></i> Tặng 3 ngày dùng thử miễn phí!</span>
                <span class="text-[10px] text-slate-400">Trải nghiệm toàn bộ tính năng khi đăng nhập bằng Google.</span>
            </div>
            
            <button class="btn-google shadow-emerald-500/20 shadow-md" id="btnGoogleLogin">
                <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" width="20" height="20">
                Đăng nhập bằng Google
            </button>
            
            <div class="auth-divider">HOẶC ĐĂNG NHẬP BẰNG EMAIL</div>
            
            <form id="emailLoginForm">
                <input type="text" id="loginEmail" class="auth-input" placeholder="Email (VD: abc@gmail.com)" autocomplete="email">
                <input type="password" id="loginPassword" class="auth-input" placeholder="Mật khẩu" autocomplete="current-password">
                <div id="loginMsg" class="auth-msg"></div>
                <button type="submit" class="auth-btn" id="btnEmailLogin" style="margin-top:1rem;">
                    <i class="fa-solid fa-sign-in-alt"></i> <span>Đăng nhập</span>
                </button>
                <div style="display:flex; justify-content:space-between; margin-top:0.75rem;">
                    <button type="button" class="auth-link" onclick="forgotPassword()">Quên mật khẩu?</button>
                    <button type="button" class="auth-link" onclick="showRegisterForm()">Tạo tài khoản</button>
                </div>
            </form>
        </div>
    </div>
    
    <!-- MODAL TẠO MẬT KHẨU DỰ PHÒNG -->
    <div id="setPwdModal" style="display:none; position:fixed; inset:0; z-index:1000000; background:rgba(15, 23, 42, 0.95); backdrop-filter:blur(8px); align-items:center; justify-content:center; padding:1rem;">
        <div class="auth-box">
            <div class="auth-title">Tạo mật khẩu dự phòng</div>
            <div class="auth-sub">Bạn đang đăng nhập bằng Google. Hãy tạo mật khẩu để lần sau có thể đăng nhập bằng Email.</div>
            <input type="password" id="newPwd1" class="auth-input" placeholder="Mật khẩu mới (tối thiểu 6 ký tự)">
            <input type="password" id="newPwd2" class="auth-input" placeholder="Nhập lại mật khẩu">
            <div id="setPwdMsg" class="auth-msg"></div>
            <button class="auth-btn" id="btnSavePwd" style="margin-top:1rem;">Lưu mật khẩu</button>
            <button class="auth-link" id="btnSkipPwd" style="margin-top:1rem; display:block; width:100%;">Để sau</button>
        </div>
    </div>
    
    <!-- MODAL GIA HẠN / NẠP TIỀN -->
    <div id="renewalModal">
        <div class="renewal-box">
            <button class="auth-close" onclick="closeUserRenewalModal()" title="Đóng" style="position:absolute;top:1rem;right:1rem;background:none;border:none;color:#94a3b8;font-size:1.25rem;cursor:pointer;">✕</button>
            
            <div class="flex flex-col items-center justify-center mb-4">
                <div class="bg-emerald-600 text-white p-3 rounded-xl shadow-lg shadow-emerald-500/30 mb-2">
                    <i class="fa-solid fa-scale-balanced text-2xl"></i>
                </div>
                <h3 class="text-lg font-black text-white tracking-wide">PRO QUANT SCREENER</h3>
                <p class="text-[10px] text-slate-400 uppercase tracking-widest mt-1">Hệ thống Đầu tư Chứng khoán</p>
            </div>

            <!-- THÔNG BÁO TRẠNG THÁI HẾT HẠN -->
            <div id="renewalStatusMsg" class="bg-rose-500/10 border border-rose-500/30 rounded-xl p-3 mb-4 text-center hidden">
                <h4 class="text-sm font-bold text-rose-400"><i class="fa-solid fa-triangle-exclamation mr-1"></i> Tài khoản đã hết hạn!</h4>
                <p class="text-[11px] text-slate-300 mt-1">Vui lòng gia hạn để tiếp tục sử dụng hệ thống.</p>
            </div>

            <!-- THÔNG BÁO CHỜ DUYỆT (Dành cho User) -->
            <div id="pendingRequestBox" class="bg-amber-500/10 border border-amber-500/30 rounded-xl p-3 mb-4 text-center hidden">
                <h4 class="text-sm font-bold text-amber-400"><i class="fa-solid fa-clock mr-1"></i> Yêu cầu đang chờ duyệt!</h4>
                <p class="text-[11px] text-slate-300 mt-1">Bạn đã gửi yêu cầu thanh toán. Vui lòng đợi Admin xác nhận.</p>
                <button onclick="cancelMyRenewal()" class="mt-2 px-3 py-1 bg-rose-500/20 hover:bg-rose-500/30 text-rose-300 border border-rose-500/30 rounded text-xs font-semibold transition">Hủy yêu cầu này</button>
            </div>

            <div id="renewalOptionsBox">
                <div class="renewal-icon mx-auto"><i class="fa-solid fa-clock"></i></div>
                <h2 class="auth-title" style="color:#10b981;">Gia hạn tài khoản</h2>
                <p class="auth-sub">Chọn gói gia hạn để tiếp tục sử dụng các tính năng phân tích và lọc cổ phiếu AI.</p>
                
                <div id="packageTitle" style="text-align:left; margin-bottom:10px; font-weight:bold; color:#94a3b8; font-size:0.8rem;">CHỌN GÓI GIA HẠN:</div>
                <div style="max-height:200px; overflow-y:auto; padding-right:5px;" id="packageList">{packages_html}</div>
                
                <div id="qrCodeWrap" style="display:none; margin-top:1rem;">
                    <img id="qrImage" src="" style="width:200px; height:200px; margin:0 auto 10px; border-radius:12px; border:2px solid #334155; background:#fff; padding: 5px;">
                    <div class="bank-info">
                        <div class="bank-row"><span>Ngân hàng:</span> <span>{bank.get('bank_name', 'MB Bank')}</span></div>
                        <div class="bank-row"><span>Số TK:</span> <span>{bank.get('account_no', '0123456789')}</span></div>
                        <div class="bank-row"><span>Chủ TK:</span> <span>{bank.get('account_name', 'NGUYEN VAN A')}</span></div>
                        <div class="bank-row"><span>Số tiền:</span> <span id="payAmount" class="code-highlight">0 VNĐ</span></div>
                        <div class="bank-row"><span>Nội dung:</span> <span id="payCode" class="code-highlight">---</span></div>
                    </div>
                    <p style="font-size:0.75rem; color:#f59e0b; text-align:left; margin-bottom:10px;"><i class="fa-solid fa-info-circle"></i> Vui lòng chuyển khoản đúng nội dung để hệ thống tự động duyệt.</p>
                </div>
                <div style="display:flex; gap:10px; margin-top:1rem;">
                    <button class="auth-btn" id="btnConfirmPay" style="display:none; background:#10b981;" onclick="confirmPayment()">Tôi đã chuyển khoản</button>
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- MODAL ADMIN & USER PROFILE -->
    <!-- ========================================== -->
    <div id="admin-modal" class="fixed inset-0 z-[9999999] flex items-center justify-center bg-black/80 backdrop-blur-sm hidden p-4">
        <div class="bg-slate-900 border border-slate-700 w-full max-w-4xl rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90dvh]">
            
            <div class="bg-slate-950 px-5 py-4 border-b border-slate-800 flex justify-between items-center">
                <div class="flex items-center space-x-3">
                    <!-- AVATAR ICON -->
                    <div class="relative w-8 h-8 rounded-full border border-emerald-500/50 flex items-center justify-center bg-slate-800 overflow-hidden shrink-0" id="modal-header-avatar">
                        <i class="fa-solid fa-circle-user text-emerald-400 text-lg" id="modal-header-icon"></i>
                        <img id="modal-header-img" src="" class="w-full h-full object-cover hidden absolute inset-0">
                    </div>
                    <h3 class="text-sm font-bold text-white" id="modalTitle">Tài khoản của tôi</h3>
                </div>
                <button type="button" onclick="closeAdminModal()" class="text-slate-400 hover:text-white p-2 rounded-lg bg-slate-800 hover:bg-slate-700 transition">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </div>

            <!-- HEADER TÀI KHOẢN TỐI ƯU DIỆN TÍCH -->
            <div class="p-4 bg-slate-800/40 border-b border-slate-700 flex flex-col gap-3">
                
                <!-- Hàng 1: Email và Hạn sử dụng -->
                <div class="flex justify-between items-start">
                    <div class="min-w-0 pr-2 flex-1">
                        <div class="text-[10px] text-slate-400 mb-0.5 uppercase tracking-wider font-semibold">Email đăng nhập</div>
                        <div class="text-sm font-bold text-white truncate" id="modalUserEmail">---</div>
                    </div>
                    
                    <!-- Khối Hạn sử dụng (Sẽ bị ẩn nếu là Admin) -->
                    <div class="text-right shrink-0" id="expire-container">
                        <div class="text-[10px] text-slate-400 mb-0.5 uppercase tracking-wider font-semibold">Hạn sử dụng</div>
                        <div class="text-xs font-bold text-emerald-400" id="modalExpireDate">Đang tải...</div>
                    </div>
                </div>

                <!-- Hàng 2: Các nút chức năng (Ngang hàng, nhỏ gọn) -->
                <div class="flex flex-wrap items-center gap-2 mt-1">
                    <!-- Nút Hỗ trợ (Mở thẳng Zalo) -->
                    <a href="https://zalo.me/0528484668" target="_blank" rel="noopener noreferrer" class="flex-1 min-w-[90px] py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-[11px] font-bold transition flex items-center justify-center gap-1.5 shadow-md">
                        <i class="fa-solid fa-headset"></i> Hỗ trợ
                    </a>
                    
                    <!-- Lịch sử -->
                    <button onclick="openHistoryModal(window.auth.currentUser.email)" class="flex-1 min-w-[100px] py-2 bg-slate-700 hover:bg-slate-600 text-slate-200 border border-slate-600 rounded-lg text-[11px] font-bold transition flex items-center justify-center gap-1.5">
                        <i class="fa-solid fa-clock-rotate-left"></i> Lịch sử
                    </button>

                    <!-- Gia hạn (Ẩn nếu là Admin) -->
                    <button onclick="openUserRenewalModal()" id="btn-renew-user" class="flex-1 min-w-[100px] py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-[11px] font-bold transition flex items-center justify-center gap-1.5 shadow-md">
                        <i class="fa-solid fa-plus-circle"></i> Gia hạn
                    </button>
                </div>
            </div>

            <div id="adminTabsWrapper" class="flex border-b border-slate-800 bg-slate-950 px-5 gap-4 hidden">
                <button onclick="switchAdminTab('users')" id="tabBtnUsers" class="py-3 text-xs font-bold text-emerald-400 border-b-2 border-emerald-400 transition">Quản lý Người dùng</button>
                <button onclick="switchAdminTab('renewals')" id="tabBtnRenewals" class="py-3 text-xs font-bold text-slate-400 border-b-2 border-transparent transition">Duyệt Gia hạn (<span id="pendingCount">0</span>)</button>
                <button onclick="switchAdminTab('tools')" id="tabBtnTools" class="py-3 text-xs font-bold text-slate-400 border-b-2 border-transparent transition hidden"><i class="fa-solid fa-gears mr-1"></i>Công cụ Admin</button>
            </div>

            <div id="adminTabsContent" class="p-5 overflow-y-auto flex-grow hidden">
                <!-- TAB USERS -->
                <div id="adminTabUsers" class="flex flex-col h-full">
                    <!-- THANH CHUYỂN TAB CON & THỐNG KÊ -->
                    <div class="flex gap-2 mb-3 shrink-0">
                        <button onclick="filterUserRole('user')" id="btn-sub-tab-user" class="flex-1 py-2 bg-emerald-600 text-white rounded-lg border border-emerald-500 text-xs font-bold transition flex flex-col items-center justify-center">
                            <span>Người dùng</span>
                            <span class="text-[14px] font-black" id="admin-stat-user">0</span>
                        </button>
                        <button onclick="filterUserRole('admin')" id="btn-sub-tab-admin" class="flex-1 py-2 bg-slate-800 text-slate-400 hover:text-white rounded-lg border border-slate-700 text-xs font-bold transition flex flex-col items-center justify-center">
                            <span>Admin</span>
                            <span class="text-[14px] font-black" id="admin-stat-admin">0</span>
                        </button>
                    </div>

                    <div class="mb-3 relative shrink-0">
                        <span class="absolute inset-y-0 left-0 flex items-center pl-3 text-slate-400">
                            <i class="fa-solid fa-magnifying-glass text-xs"></i>
                        </span>
                        <input type="text" id="admin-search-input" oninput="renderAdminUsersList()" placeholder="Tìm kiếm Email hoặc Tên..." class="w-full pl-8 pr-3 py-2 bg-slate-950 border border-slate-700 rounded-lg text-xs text-white focus:outline-none focus:border-emerald-500 transition">
                    </div>
                    
                    <!-- DANH SÁCH DẠNG THẺ (CARD) -->
                    <div id="admin-users-list" class="space-y-2 overflow-y-auto pr-1 pb-4">
                        <div class="p-4 text-center text-slate-500 text-xs">Đang tải danh sách...</div>
                    </div>
                </div>

                <!-- TAB RENEWALS -->
                <div id="adminTabRenewals" class="overflow-x-auto hidden">
                    <table class="w-full text-left text-xs">
                        <thead>
                          <tr class="border-b border-slate-800 text-slate-400 bg-slate-950">
                           <th class="p-3">Email</th>
                           <th class="p-3">Gói / Số tiền</th>
                           <th class="p-3">Mã CK</th>
                           <th class="p-3 text-center">Thao tác</th>
                          </tr>
                         </thead>
                        <tbody id="admin-renewals-list" class="divide-y divide-slate-800">
                            <tr><td colspan="4" class="p-4 text-center text-slate-500">Đang tải yêu cầu...</td></tr>
                        </tbody>
                    </table>
                </div>

                <!-- TAB TOOLS -->
                <div id="adminTabTools" class="hidden">
                    {admin_tools_html}
                </div>
            </div>

            <div class="bg-slate-950 px-5 py-3 border-t border-slate-800 flex justify-between items-center mt-auto shrink-0">
                <button type="button" onclick="triggerSignOut()" class="px-3 py-2 bg-rose-500/20 hover:bg-rose-500/30 text-rose-300 border border-rose-500/30 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition">
                    <i class="fa-solid fa-right-from-bracket"></i> Đăng xuất
                </button>
                <button type="button" onclick="closeAdminModal()" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg text-xs font-semibold">Đóng</button>
            </div>
        </div>
    </div>

    <!-- MODAL LỊCH SỬ GIA HẠN -->
    <div id="historyModal" class="fixed inset-0 z-[10000002] flex items-center justify-center bg-black/80 backdrop-blur-sm hidden p-4">
        <div class="bg-slate-900 border border-slate-700 w-full max-w-2xl rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[85dvh]">
            <div class="bg-slate-950 px-5 py-4 border-b border-slate-800 flex justify-between items-center">
                <div>
                    <h3 class="text-sm font-bold text-white"><i class="fa-solid fa-clock-rotate-left text-emerald-400 mr-1.5"></i> Lịch sử giao dịch</h3>
                    <p class="text-[11px] text-slate-400 mt-0.5" id="historyEmailText">---</p>
                </div>
                <button type="button" onclick="closeHistoryModal()" class="text-slate-400 hover:text-white p-2 rounded-lg bg-slate-800 transition">
                    <i class="fa-solid fa-xmark"></i>
                </button>
            </div>
            <div class="p-4 overflow-y-auto flex-grow">
                <table class="w-full text-left text-xs">
                    <thead>
                      <tr class="border-b border-slate-800 text-slate-400 bg-slate-950">
                       <th class="p-2">Ngày tạo</th>
                       <th class="p-2">Gói / Số tiền</th>
                       <th class="p-2">Mã CK</th>
                       <th class="p-2">Trạng thái</th>
                      </tr>
                     </thead>
                    <tbody id="history-list" class="divide-y divide-slate-800">
                        <tr><td colspan="4" class="p-4 text-center text-slate-500">Đang tải dữ liệu...</td></tr>
                    </tbody>
                </table>
            </div>
            <div class="bg-slate-950 px-5 py-3 border-t border-slate-800 text-right">
                <button type="button" onclick="closeHistoryModal()" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg text-xs font-semibold">Đóng</button>
            </div>
        </div>
    </div>

    <!-- MODAL SỬA HẠN DÙNG (ADMIN) -->
    <div id="editExpireModal" class="fixed inset-0 z-[10000000] flex items-center justify-center bg-black/80 backdrop-blur-sm hidden p-4">
        <div class="bg-slate-900 border border-slate-700 w-full max-w-sm rounded-2xl shadow-2xl p-5">
            <h3 class="text-sm font-bold text-white mb-2">Điều chỉnh hạn sử dụng</h3>
            <p class="text-xs text-slate-400 mb-4 truncate" id="edit-expire-email">---</p>
            
            <label class="block text-[11px] font-bold text-slate-400 mb-1">Chọn ngày hết hạn mới:</label>
            <input type="date" id="edit-expire-date" class="w-full p-2 mb-4 bg-slate-950 border border-slate-700 rounded-lg text-sm text-emerald-400 font-bold focus:outline-none focus:border-emerald-500 [color-scheme:dark]">
            
            <div class="flex gap-2 mb-5">
                <button onclick="quickAddDays(30)" class="flex-1 py-1 bg-slate-800 hover:bg-slate-700 text-xs text-white rounded border border-slate-600 transition">+30 Ngày</button>
                <button onclick="quickAddDays(90)" class="flex-1 py-1 bg-slate-800 hover:bg-slate-700 text-xs text-white rounded border border-slate-600 transition">+90 Ngày</button>
                <button onclick="quickAddDays(365)" class="flex-1 py-1 bg-slate-800 hover:bg-slate-700 text-xs text-white rounded border border-slate-600 transition">+1 Năm</button>
            </div>
            
            <div class="flex justify-end gap-2">
                <button onclick="closeEditExpireModal()" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg text-xs font-semibold">Hủy</button>
                <button id="btn-save-expire" onclick="saveNewExpireDate()" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-bold shadow">Lưu thay đổi</button>
            </div>
        </div>
    </div>
    """

def build_auth_lite_js(config):
    trial_days = config.get("trial_days", 7)
    bank_config_js = json.dumps(config.get("bank_config", {}), ensure_ascii=False)
    
    js_template = r"""
    <script>
    (function() {
        'use strict';
        var TRIAL_DAYS = __TRIAL_DAYS__;
        var BANK_CONFIG = __BANK_CONFIG__;
        var selectedPkgId = null;
        var selectedAmount = 0;
        var selectedDays = 30;
        var currentUserRole = "user";
        
        function parseDate(val) {
            if (!val) return null;
            if (typeof val.toDate === 'function') return val.toDate();
            if (typeof val === 'object' && val.seconds !== undefined) {
                return new Date(val.seconds * 1000);
            }
            var d = new Date(val);
            return isNaN(d.getTime()) ? null : d;
        }
        
        function waitAuth(cb) {
            var t = setInterval(function() {
                if (typeof firebase !== 'undefined' && typeof window.auth !== 'undefined' && typeof window.db !== 'undefined') {
                    clearInterval(t); cb();
                }
            }, 200);
        }

        async function sendTelegramMessage(message) {
            if (!TELEGRAM_BOT_TOKEN || !TELEGRAM_CHAT_ID) return; 
            try {
                var url = `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`;
                await fetch(url, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        chat_id: TELEGRAM_CHAT_ID,
                        text: message,
                        parse_mode: 'HTML'
                    })
                });
            } catch (err) {
                console.warn('Lỗi gửi Telegram:', err);
            }
        }

        window.triggerSignOut = async function() {
            window.scrollTo(0, 0);
            var adminModal = document.getElementById('admin-modal');
            if (adminModal) adminModal.classList.add('hidden');
            
            var renewal = document.getElementById('renewalModal');
            if (renewal) renewal.classList.remove('show');

            try {
                if (window.auth) await window.auth.signOut();
            } catch(e) { console.warn('SignOut error:', e); }
        };

        waitAuth(function() {
            var auth = window.auth;
            var db = window.db;

            var btnEmailLogin = document.getElementById('btnEmailLogin');
            if (btnEmailLogin) {
                var btnSpan = btnEmailLogin.querySelector('span');
                btnEmailLogin.disabled = false;
                if(btnSpan) btnSpan.innerHTML = 'Đăng nhập';
            }

            auth.onAuthStateChanged(async function(user) {
                var authOverlay = document.getElementById('authOverlay');
                var adminModal = document.getElementById('admin-modal');
                var renewalModal = document.getElementById('renewalModal');
                var statusMsg = document.getElementById('renewalStatusMsg');
                
                if (btnEmailLogin) {
                    btnEmailLogin.disabled = false;
                    if(btnSpan) btnSpan.innerHTML = 'Đăng nhập';
                }

                // ==========================================
                // CẬP NHẬT AVATAR LÊN HEADER VÀ MODAL
                // ==========================================
                var iconEl = document.getElementById('header-user-icon');
                var imgEl = document.getElementById('header-user-avatar');
                
                var modalIcon = document.getElementById('modal-header-icon');
                var modalImg = document.getElementById('modal-header-img');

                if (user) {
                    // Header Avatar
                    if (imgEl && iconEl) {
                        if (user.photoURL) {
                            imgEl.src = user.photoURL;
                            imgEl.classList.remove('hidden');
                            iconEl.classList.add('hidden');
                        } else {
                            imgEl.classList.add('hidden');
                            iconEl.classList.remove('hidden');
                        }
                    }
                    // Modal Avatar
                    if (modalImg && modalIcon) {
                        if (user.photoURL) {
                            modalImg.src = user.photoURL;
                            modalImg.classList.remove('hidden');
                            modalIcon.classList.add('hidden');
                        } else {
                            modalImg.classList.add('hidden');
                            modalIcon.classList.remove('hidden');
                        }
                    }
                } else {
                    // Chưa đăng nhập -> Trả lại icon mặc định
                    if (imgEl && iconEl) {
                        imgEl.classList.add('hidden');
                        iconEl.classList.remove('hidden');
                    }
                    if (modalImg && modalIcon) {
                        modalImg.classList.add('hidden');
                        modalIcon.classList.remove('hidden');
                    }
                }
                // ==========================================

                if (user) {
                    var isExpired = await checkUserPermission(user);
                    
                    if (isExpired) {
                        if (authOverlay) {
                            authOverlay.classList.remove('hidden');
                        }
                        document.body.classList.add('auth-locked');
                        if (renewalModal) renewalModal.classList.add('show');
                        if (adminModal) adminModal.classList.add('hidden');
                        
                        if (statusMsg) statusMsg.classList.remove('hidden');
                        checkMyPendingRequest();
                    } else {
                        document.body.classList.remove('auth-locked'); 
                        if (authOverlay) {
                            authOverlay.classList.add('hidden');
                        }
                        if (adminModal) {
                            adminModal.classList.add('hidden');
                            adminModal.style.display = 'none';
                        }
                        if (statusMsg) statusMsg.classList.add('hidden');
                        
                        if (typeof window.onAuthReady === 'function') {
                            try { await window.onAuthReady(user); } catch(e) { console.warn(e); }
                        }
                    }
                } else {
                    currentUserRole = "user";
                    document.body.classList.add('auth-locked');
                    if (authOverlay) {
                        authOverlay.classList.remove('hidden');
                    }
                    if (adminModal) {
                        adminModal.classList.add('hidden');
                        adminModal.style.display = 'none';
                    }
                    if (renewalModal) renewalModal.classList.remove('show');
                    if (statusMsg) statusMsg.classList.add('hidden');
                    
                    var adminList = document.getElementById('admin-users-list');
                    if (adminList) adminList.innerHTML = `<div class="p-4 text-center text-slate-500 text-xs">Chưa đăng nhập...</div>`;
                    selectedPkgId = null;
                }
            });

            document.getElementById('btnGoogleLogin').addEventListener('click', async function() {
                var provider = new firebase.auth.GoogleAuthProvider();
                try {
                    var res = await auth.signInWithPopup(provider);
                    if (res.user) checkAskPassword(res.user);
                } catch(e) { showMsg('loginMsg', 'Lỗi Google: ' + e.message, 'error'); }
            });

            var loginForm = document.getElementById('emailLoginForm');
            var emailInput = document.getElementById('loginEmail');
            
            emailInput.addEventListener('blur', function() {
                var v = this.value.trim().toLowerCase();
                if (v && v.indexOf('@') === -1) this.value = v + '@gmail.com';
            });

            loginForm.addEventListener('submit', async function(e) {
                e.preventDefault();
                var email = emailInput.value.trim();
                var pwd = document.getElementById('loginPassword').value;
                var btn = document.getElementById('btnEmailLogin');
                var btnSpan = btn.querySelector('span');
                var msgBox = document.getElementById('loginMsg');
                
                msgBox.className = 'auth-msg';
                msgBox.innerHTML = '';

                if (!email || !pwd) return showMsg('loginMsg', 'Vui lòng nhập đủ email và mật khẩu.', 'error');
                
                btn.disabled = true; 
                btnSpan.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Đang kết nối...';
                
                try {
                    await auth.signInWithEmailAndPassword(email, pwd);
                } catch(e) {
                    var errMsg = e.message;
                    if (e.code === 'auth/user-not-found') errMsg = 'Tài khoản chưa tồn tại. Vui lòng đăng nhập bằng Google hoặc bấm "Tạo tài khoản".';
                    if (e.code === 'auth/wrong-password') errMsg = 'Sai mật khẩu. Vui lòng kiểm tra lại.';
                    
                    showMsg('loginMsg', 'Lỗi: ' + errMsg, 'error');
                    btn.disabled = false; 
                    btnSpan.innerHTML = 'Đăng nhập';
                }
            });

            function checkAskPassword(user) {
                if (!user || !user.email) return;
                var hasPwd = user.providerData.some(function(p) { return p.providerId === 'password'; });
                if (hasPwd || sessionStorage.getItem('asked_pwd_' + user.email)) return;
                sessionStorage.setItem('asked_pwd_' + user.email, '1'); 
                document.getElementById('setPwdModal').style.display = 'flex';
            }

            document.getElementById('btnSkipPwd').addEventListener('click', function() {
                document.getElementById('setPwdModal').style.display = 'none';
            });

            document.getElementById('btnSavePwd').addEventListener('click', async function() {
                var p1 = document.getElementById('newPwd1').value;
                var p2 = document.getElementById('newPwd2').value;
                if (p1.length < 6) return showMsg('setPwdMsg', 'Mật khẩu phải từ 6 ký tự.', 'error');
                if (p1 !== p2) return showMsg('setPwdMsg', 'Mật khẩu nhập lại không khớp.', 'error');
                
                var btn = this; btn.disabled = true; btn.innerText = 'Đang lưu...';
                try {
                    var user = auth.currentUser;
                    var cred = firebase.auth.EmailAuthProvider.credential(user.email, p1);
                    await user.linkWithCredential(cred);
                    showMsg('setPwdMsg', '✅ Tạo mật khẩu thành công!', 'success');
                    setTimeout(function() { document.getElementById('setPwdModal').style.display = 'none'; }, 1500);
                } catch(e) {
                    showMsg('setPwdMsg', 'Lỗi: ' + e.message, 'error');
                    btn.disabled = false; btn.innerText = 'Lưu mật khẩu';
                }
            });

            async function checkUserPermission(user) {
                var email = user.email.toLowerCase();
                try {
                    var doc = await db.collection('allowed_users').doc(email).get();
                    
                    var isSuperAdmin = typeof SUPER_ADMINS !== 'undefined' && SUPER_ADMINS.includes(email);

                    if (!doc.exists) {
                        var expireDate = new Date();
                        expireDate.setDate(expireDate.getDate() + TRIAL_DAYS);
                        await db.collection('allowed_users').doc(email).set({
                            email: email, 
                            role: isSuperAdmin ? 'super_admin' : 'user', 
                            expiresAt: expireDate.toISOString()
                        });
                        updateExpireUI(expireDate);
                        currentUserRole = isSuperAdmin ? 'super_admin' : 'user';
                        return false; 
                    } else {
                        var data = doc.data();
                        var currentRole = data.role || "user";
                        
                        if (isSuperAdmin && currentRole !== 'super_admin') {
                            await db.collection('allowed_users').doc(email).update({ role: 'super_admin' });
                            currentRole = 'super_admin';
                        } else if (!isSuperAdmin && currentRole === 'super_admin') {
                            await db.collection('allowed_users').doc(email).update({ role: 'admin' });
                            currentRole = 'admin';
                        }
                        
                        currentUserRole = currentRole;
                        
                        if (currentRole === 'admin' || currentRole === 'super_admin') {
                            var btnChat = document.getElementById('btn-admin-chat-header');
                            if (btnChat) {
                                btnChat.classList.remove('hidden');
                                btnChat.classList.add('flex');
                            }
                        }

                        var expDateObj = parseDate(data.expiresAt);
                        
                        if (expDateObj) {
                            updateExpireUI(expDateObj);
                            if (currentRole !== 'admin' && currentRole !== 'super_admin' && new Date() > expDateObj) {
                                return true;
                            }
                        }
                    }
                } catch(e) { console.warn('Lỗi check quyền:', e); }
                return false;
            }

            function updateExpireUI(expDate) {
                var txt = document.getElementById('hiddenExpireDate');
                if (txt) txt.innerText = expDate.toLocaleDateString('vi-VN');
            }

            window.openUserRenewalModal = function() {
                var renewal = document.getElementById('renewalModal');
                var statusMsg = document.getElementById('renewalStatusMsg');
                if (renewal) {
                    renewal.classList.add('show');
                    selectedPkgId = null;
                    document.querySelectorAll('.package-item').forEach(function(el) { el.classList.remove('active'); });
                    var qrWrap = document.getElementById('qrCodeWrap');
                    if (qrWrap) qrWrap.style.display = 'none';
                    var btnPay = document.getElementById('btnConfirmPay');
                    if (btnPay) btnPay.style.display = 'none';
                    
                    if (statusMsg) statusMsg.classList.add('hidden');
                    checkMyPendingRequest();
                }
            };

            window.closeUserRenewalModal = function() {
                var renewal = document.getElementById('renewalModal');
                if (renewal) renewal.classList.remove('show');
            };

            window.selectPackage = function(id, amount, label, days) {
                selectedPkgId = id;
                selectedAmount = amount;
                selectedDays = days || 30;
                
                document.querySelectorAll('.package-item').forEach(function(el) { el.classList.remove('active'); });
                var el = document.getElementById('pkg_' + id);
                if (el) el.classList.add('active');
                document.getElementById('qrCodeWrap').style.display = 'block';
                document.getElementById('payAmount').innerText = amount.toLocaleString('vi-VN') + ' VNĐ';
                var code = 'NAP' + Math.floor(100000 + Math.random() * 900000);
                document.getElementById('payCode').innerText = code;
                var qrUrl = `https://img.vietqr.io/image/${BANK_CONFIG.bank_id}-${BANK_CONFIG.account_no}-compact2.png?amount=${amount}&addInfo=${code}&accountName=${encodeURIComponent(BANK_CONFIG.account_name)}`;
                document.getElementById('qrImage').src = qrUrl;
                document.getElementById('btnConfirmPay').style.display = 'flex';
            };

            async function checkMyPendingRequest() {
                if (!auth.currentUser) return;
                var pendingBox = document.getElementById('pendingRequestBox');
                var pkgList = document.getElementById('packageList');
                var qrWrap = document.getElementById('qrCodeWrap');
                var btnConfirm = document.getElementById('btnConfirmPay');
                var titleEl = document.getElementById('packageTitle');
                
                try {
                    var snap = await db.collection('renewal_requests')
                        .where('email', '==', auth.currentUser.email)
                        .where('status', '==', 'pending')
                        .get();
                        
                    if (!snap.empty) {
                        var reqData = snap.docs[0].data();
                        window.myPendingReqId = snap.docs[0].id;
                        
                        if (pendingBox) pendingBox.classList.remove('hidden');
                        if (pkgList) pkgList.classList.add('hidden');
                        if (btnConfirm) btnConfirm.style.display = 'none';
                        
                        if (qrWrap) {
                            qrWrap.style.display = 'block';
                            document.getElementById('payAmount').innerText = reqData.amount.toLocaleString('vi-VN') + ' VNĐ';
                            document.getElementById('payCode').innerText = reqData.code;
                            
                            var qrUrl = `https://img.vietqr.io/image/${BANK_CONFIG.bank_id}-${BANK_CONFIG.account_no}-compact2.png?amount=${reqData.amount}&addInfo=${reqData.code}&accountName=${encodeURIComponent(BANK_CONFIG.account_name)}`;
                            document.getElementById('qrImage').src = qrUrl;
                        }
                        
                        if (titleEl) titleEl.innerHTML = `GÓI ĐÃ CHỌN: <span class="text-emerald-400">${reqData.packageId.toUpperCase()}</span>`;

                    } else {
                        if (pendingBox) pendingBox.classList.add('hidden');
                        if (pkgList) pkgList.classList.remove('hidden');
                        if (qrWrap) qrWrap.style.display = 'none';
                        if (btnConfirm) btnConfirm.style.display = 'none';
                        window.myPendingReqId = null;
                        
                        if (titleEl) titleEl.innerHTML = `CHỌN GÓI GIA HẠN:`;
                    }
                } catch(e) { console.warn('Lỗi check pending:', e); }
            }

            window.cancelMyRenewal = async function() {
                if (!window.myPendingReqId) return;
                if (!confirm("Bạn có chắc muốn hủy yêu cầu gia hạn này?")) return;
                try {
                    await db.collection('renewal_requests').doc(window.myPendingReqId).delete();
                    alert('Đã hủy yêu cầu thành công. Bạn có thể tạo lệnh mới.');
                    checkMyPendingRequest();
                } catch(e) {
                    alert('Lỗi hủy yêu cầu: ' + e.message);
                }
            };

            window.confirmPayment = async function() {
                if (!selectedPkgId) return;
                if (!auth.currentUser) return alert('Phiên đăng nhập đã hết hạn, vui lòng đăng nhập lại.');
                
                var btn = document.getElementById('btnConfirmPay');
                btn.disabled = true; btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Đang kiểm tra...';
                
                try {
                    var existingReq = await db.collection('renewal_requests')
                        .where('email', '==', auth.currentUser.email)
                        .where('status', '==', 'pending')
                        .get();
                        
                    if (!existingReq.empty) {
                        alert('Bạn đã có một yêu cầu đang chờ duyệt! Vui lòng đợi Admin xác nhận hoặc Hủy yêu cầu cũ trước khi tạo lệnh mới.');
                        checkMyPendingRequest();
                        return; 
                    }

                    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Đang gửi...';
                    var payCode = document.getElementById('payCode').innerText;
                    
                    await db.collection('renewal_requests').add({
                        email: auth.currentUser.email,
                        packageId: selectedPkgId,
                        amount: selectedAmount,
                        days: selectedDays,
                        code: payCode,
                        status: 'pending',
                        createdAt: firebase.firestore.FieldValue.serverTimestamp()
                    });

                    var msg = `🔔 <b>CÓ YÊU CẦU GIA HẠN MỚI</b>\n\n`
                            + `👤 Email: <code>${auth.currentUser.email}</code>\n`
                            + `📦 Gói: ${selectedPkgId}\n`
                            + `💰 Số tiền: ${selectedAmount.toLocaleString('vi-VN')} VNĐ\n`
                            + `🔑 Mã CK: <code>${payCode}</code>\n\n`
                            + `👉 Vào Web để kiểm tra và duyệt!`;
                    sendTelegramMessage(msg);

                    alert('Đã gửi yêu cầu! Vui lòng đợi Admin xác nhận.');
                    checkMyPendingRequest();
                    
                } catch(e) {
                    alert('Lỗi gửi yêu cầu: ' + e.message);
                    btn.disabled = false; btn.innerText = 'Tôi đã chuyển khoản';
                }
            };

            window.showRegisterForm = function() { alert('Vui lòng đăng nhập bằng Google để tạo tài khoản tự động!'); };
            window.forgotPassword = async function() {
                var email = document.getElementById('loginEmail').value.trim();
                if (!email) return showMsg('loginMsg', 'Nhập email để lấy lại mật khẩu.', 'error');
                try {
                    await auth.sendPasswordResetEmail(email);
                    showMsg('loginMsg', '✅ Đã gửi link khôi phục vào email!', 'success');
                } catch(e) { showMsg('loginMsg', 'Lỗi: ' + e.message, 'error'); }
            };

            window.switchAdminTab = function(tab) {
                var usersTab = document.getElementById('adminTabUsers');
                var renewalsTab = document.getElementById('adminTabRenewals');
                var toolsTab = document.getElementById('adminTabTools');
                var btnUsers = document.getElementById('tabBtnUsers');
                var btnRenewals = document.getElementById('tabBtnRenewals');
                var btnTools = document.getElementById('tabBtnTools');

                // Ẩn nội dung tất cả các tab
                if (usersTab) usersTab.classList.add('hidden');
                if (renewalsTab) renewalsTab.classList.add('hidden');
                if (toolsTab) toolsTab.classList.add('hidden');
                
                // Reset style các nút (KHÔNG thêm class hidden cho btnTools)
                if (btnUsers) btnUsers.className = "py-3 text-xs font-bold text-slate-400 border-b-2 border-transparent transition";
                if (btnRenewals) btnRenewals.className = "py-3 text-xs font-bold text-slate-400 border-b-2 border-transparent transition";
                if (btnTools) btnTools.className = "py-3 text-xs font-bold text-slate-400 border-b-2 border-transparent transition";

                // Hiện tab được chọn
                if (tab === 'users') {
                    if (usersTab) usersTab.classList.remove('hidden');
                    if (btnUsers) btnUsers.className = "py-3 text-xs font-bold text-emerald-400 border-b-2 border-emerald-400 transition";
                    loadAdminUsers();
                } else if (tab === 'renewals') {
                    if (renewalsTab) renewalsTab.classList.remove('hidden');
                    if (btnRenewals) btnRenewals.className = "py-3 text-xs font-bold text-emerald-400 border-b-2 border-emerald-400 transition";
                    loadAdminRenewals();
                } else if (tab === 'tools' && btnTools) {
                    if (toolsTab) toolsTab.classList.remove('hidden');
                    btnTools.className = "py-3 text-xs font-bold text-rose-400 border-b-2 border-rose-400 transition";
                }
            };

            window.openAdminModal = async function() {
                if (!window.auth || !window.auth.currentUser) return;
                try {
                    var modal = document.getElementById('admin-modal');
                    modal.style.display = 'flex';
                    modal.classList.remove('hidden');
                    
                    var email = window.auth.currentUser.email;
                    document.getElementById('modalUserEmail').innerText = email;
                    
                    var renewBtn = document.getElementById('btn-renew-user');
                    var expireContainer = document.getElementById('expire-container');

                    if (!window.db) throw new Error("Firebase DB chưa sẵn sàng");
                    
                    var doc = await window.db.collection('allowed_users').doc(email.toLowerCase()).get();
                    
                    if (doc.exists) {
                        var data = doc.data();
                        var role = data.role || 'user';
                        var isAdmin = (role === 'admin' || role === 'super_admin');
                        
                        var tabsWrapper = document.getElementById('adminTabsWrapper');
                        var tabsContent = document.getElementById('adminTabsContent');
                        
                        if (isAdmin) {
                            tabsWrapper.classList.remove('hidden');
                            tabsContent.classList.remove('hidden');
                            
                            var titleStr = "Quản Trị Hệ Thống";
                            if (role === 'super_admin') titleStr = "Super Admin (Toàn quyền)";
                            else if (role === 'admin') titleStr = "Quản Trị Viên (Admin)";
                            
                            document.getElementById('modalTitle').innerText = titleStr;
                            
                            // Ẩn nút Gia hạn và khối Hạn sử dụng
                            if (renewBtn) renewBtn.style.display = 'none';
                            if (expireContainer) expireContainer.style.display = 'none';
                            
                            // CHỈ SUPER ADMIN MỚI THẤY TAB CÔNG CỤ ADMIN
                            var btnTools = document.getElementById('tabBtnTools');
                            if (btnTools) {
                                if (role === 'super_admin') {
                                    btnTools.classList.remove('hidden');
                                } else {
                                    btnTools.classList.add('hidden');
                                }
                            }
                            
                            switchAdminTab('users');
                        } else {
                            tabsWrapper.classList.add('hidden');
                            tabsContent.classList.add('hidden');
                            document.getElementById('modalTitle').innerText = "Tài khoản của tôi";
                            
                            // Hiện nút Gia hạn và khối Hạn sử dụng
                            if (renewBtn) renewBtn.style.display = 'flex';
                            if (expireContainer) expireContainer.style.display = 'block';
                            
                            var expDateObj = parseDate(data.expiresAt);
                            document.getElementById('modalExpireDate').innerText = expDateObj ? expDateObj.toLocaleDateString('vi-VN') : 'Chưa cập nhật';
                        }
                    }
                } catch (e) {
                    console.warn("Lỗi mở modal (có thể do mạng chập chờn):", e);
                    // Đã bỏ alert và closeAdminModal để không làm gián đoạn người dùng
                }
            };

            window.closeAdminModal = function() {
                var modal = document.getElementById('admin-modal');
                if (modal) {
                    modal.classList.add('hidden');
                    modal.style.display = 'none'; 
                    setTimeout(function() { modal.style.display = ''; }, 300);
                }
            };

            function escapeHTML(str) {
                if (!str) return '';
                return String(str).replace(/[&<>"']/g, function(m) {
                    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m];
                });
            }

            var adminAllUsers = []; 
            var editingUserEmail = ""; 
            var currentSubTabRole = 'user';

            async function loadAdminUsers() {
                var listEl = document.getElementById('admin-users-list');
                listEl.innerHTML = `<div class="p-4 text-center text-slate-500 text-xs"><i class="fa-solid fa-spinner fa-spin mr-2"></i>Đang tải danh sách...</div>`;

                try {
                    var snapshot = await window.db.collection('allowed_users').get();
                    adminAllUsers = [];
                    snapshot.forEach(function(doc) {
                        var data = doc.data();
                        data.id = doc.id;
                        adminAllUsers.push(data);
                    });

                    adminAllUsers.sort(function(a, b) {
                        var dateA = parseDate(a.expiresAt) ? parseDate(a.expiresAt).getTime() : 0;
                        var dateB = parseDate(b.expiresAt) ? parseDate(b.expiresAt).getTime() : 0;
                        return dateB - dateA;
                    });

                    var searchInput = document.getElementById('admin-search-input');
                    if (searchInput) searchInput.value = '';
                    renderAdminUsersList();

                } catch (err) {
                    listEl.innerHTML = `<div class="p-4 text-center text-rose-400 text-xs">Không có quyền truy cập.</div>`;
                }
            }

            window.filterUserRole = function(role) {
                currentSubTabRole = role;
                
                var btnUser = document.getElementById('btn-sub-tab-user');
                var btnAdmin = document.getElementById('btn-sub-tab-admin');
                
                if (role === 'user') {
                    btnUser.className = "flex-1 py-2 bg-emerald-600 text-white rounded-lg border border-emerald-500 text-xs font-bold transition flex flex-col items-center justify-center";
                    btnAdmin.className = "flex-1 py-2 bg-slate-800 text-slate-400 hover:text-white rounded-lg border border-slate-700 text-xs font-bold transition flex flex-col items-center justify-center";
                } else {
                    btnAdmin.className = "flex-1 py-2 bg-emerald-600 text-white rounded-lg border border-emerald-500 text-xs font-bold transition flex flex-col items-center justify-center";
                    btnUser.className = "flex-1 py-2 bg-slate-800 text-slate-400 hover:text-white rounded-lg border border-slate-700 text-xs font-bold transition flex flex-col items-center justify-center";
                }
                
                renderAdminUsersList();
            };

            window.renderAdminUsersList = function() {
                var listEl = document.getElementById('admin-users-list');
                var keyword = (document.getElementById('admin-search-input').value || '').toLowerCase().trim();
                
                var totalUsers = 0;
                var totalAdmins = 0;
                adminAllUsers.forEach(function(u) {
                    var r = u.role || 'user';
                    if (r === 'user') totalUsers++;
                    else if (r === 'admin' || r === 'super_admin') totalAdmins++;
                });
                
                if(document.getElementById('admin-stat-user')) document.getElementById('admin-stat-user').innerText = totalUsers;
                if(document.getElementById('admin-stat-admin')) document.getElementById('admin-stat-admin').innerText = totalAdmins;

                var filtered = adminAllUsers.filter(function(u) {
                    var role = u.role || 'user';
                    var isAdmin = (role === 'admin' || role === 'super_admin');
                    
                    if (currentSubTabRole === 'user' && isAdmin) return false;
                    if (currentSubTabRole === 'admin' && !isAdmin) return false;

                    var email = (u.email || u.id).toLowerCase();
                    var name = (u.name || u.displayName || '').toLowerCase();
                    return email.includes(keyword) || name.includes(keyword);
                });

                listEl.innerHTML = '';
                if (filtered.length === 0) {
                    listEl.innerHTML = `<div class="p-4 text-center text-slate-400 text-xs">Không tìm thấy người dùng nào.</div>`;
                    return;
                }

                filtered.forEach(function(data, index) {
                    var dateStr = '—';
                    var expDateObj = parseDate(data.expiresAt);
                    if (expDateObj) dateStr = expDateObj.toLocaleDateString('vi-VN');
                    
                    var safeEmail = escapeHTML(data.email || data.id);
                    var role = data.role || 'user';
                    
                    var roleBadge = '';
                    if (role === 'super_admin') roleBadge = '<span class="px-2 py-0.5 rounded text-[9px] font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30">Super</span>';
                    else if (role === 'admin') roleBadge = '<span class="px-2 py-0.5 rounded text-[9px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">Admin</span>';
                    else roleBadge = '<span class="px-2 py-0.5 rounded text-[9px] font-bold bg-slate-800 text-slate-300">User</span>';
                    
                    var actionId = `user-action-${index}`;

                    var div = document.createElement('div');
                    div.className = "bg-slate-800/40 border border-slate-700/60 rounded-xl overflow-hidden transition-all duration-200";
                    
                    div.innerHTML = `
                        <div onclick="toggleUserCard('${actionId}')" class="p-3 flex items-center justify-between cursor-pointer hover:bg-slate-800/80 transition select-none">
                            <div class="flex-1 min-w-0 pr-2">
                                <div class="text-xs font-bold text-white truncate">${safeEmail}</div>
                                <div class="flex items-center gap-2 mt-1 text-[10px] text-slate-400">
                                    <span><i class="fa-regular fa-calendar mr-1"></i>${dateStr}</span>
                                    ${roleBadge}
                                </div>
                            </div>
                            <i class="fa-solid fa-chevron-down text-slate-500 transition-transform duration-200" id="icon-${actionId}"></i>
                        </div>

                        <div id="${actionId}" class="hidden bg-slate-900/60 border-t border-slate-700/50 p-2 grid grid-cols-3 gap-2">
                            
                            <button onclick="openHistoryModal('${safeEmail}'); event.stopPropagation();" class="flex flex-col items-center justify-center py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg border border-slate-600 transition">
                                <i class="fa-solid fa-clock-rotate-left text-sm mb-1"></i>
                                <span class="text-[10px] font-semibold">Lịch sử</span>
                            </button>

                            <button onclick="openEditExpireModal('${safeEmail}', '${data.expiresAt || ''}'); event.stopPropagation();" class="flex flex-col items-center justify-center py-2 bg-indigo-500/10 hover:bg-indigo-500/20 text-indigo-300 rounded-lg border border-indigo-500/30 transition">
                                <i class="fa-solid fa-pen-to-square text-sm mb-1"></i>
                                <span class="text-[10px] font-semibold">Sửa hạn</span>
                            </button>

                            ${currentUserRole === 'super_admin' && safeEmail !== window.auth.currentUser.email ? (
                                role === 'user' 
                                ? `<button onclick="changeRole('${safeEmail}', 'admin'); event.stopPropagation();" class="flex flex-col items-center justify-center py-2 bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 rounded-lg border border-amber-500/30 transition">
                                    <i class="fa-solid fa-arrow-up text-sm mb-1"></i>
                                    <span class="text-[10px] font-semibold">Lên Admin</span>
                                   </button>`
                                : `<button onclick="changeRole('${safeEmail}', 'user'); event.stopPropagation();" class="flex flex-col items-center justify-center py-2 bg-rose-500/10 hover:bg-rose-500/20 text-rose-300 rounded-lg border border-rose-500/30 transition">
                                    <i class="fa-solid fa-arrow-down text-sm mb-1"></i>
                                    <span class="text-[10px] font-semibold">Xuống User</span>
                                   </button>`
                            ) : (
                                `<button disabled class="flex flex-col items-center justify-center py-2 bg-slate-800/50 text-slate-600 rounded-lg border border-slate-700/50 cursor-not-allowed">
                                    <i class="fa-solid fa-lock text-sm mb-1"></i>
                                    <span class="text-[10px] font-semibold">Không quyền</span>
                                 </button>`
                            )}
                        </div>
                    `;
                    listEl.appendChild(div);
                });
            }

            window.toggleUserCard = function(actionId) {
                var actionDiv = document.getElementById(actionId);
                var icon = document.getElementById('icon-' + actionId);
                if (!actionDiv || !icon) return;

                if (actionDiv.classList.contains('hidden')) {
                    actionDiv.classList.remove('hidden');
                    icon.style.transform = 'rotate(180deg)';
                } else {
                    actionDiv.classList.add('hidden');
                    icon.style.transform = 'rotate(0deg)';
                }
            };

            window.changeRole = async function(email, newRole) {
                if (currentUserRole !== 'super_admin') return alert("Bạn không có quyền thực hiện thao tác này!");
                if (!confirm(`Đổi quyền của ${email} thành ${newRole.toUpperCase()}?`)) return;
                try {
                    await window.db.collection('allowed_users').doc(email.toLowerCase()).update({ role: newRole });
                    alert(`✅ Đã đổi quyền thành ${newRole.toUpperCase()}`);
                    loadAdminUsers();
                } catch(e) {
                    alert("Lỗi đổi quyền: " + e.message);
                }
            };

            window.openEditExpireModal = function(email, currentExpireIso) {
                editingUserEmail = email;
                document.getElementById('edit-expire-email').innerText = email;
                
                var dateInput = document.getElementById('edit-expire-date');
                var d = parseDate(currentExpireIso);
                if (d) {
                    var yyyy = d.getFullYear();
                    var mm = String(d.getMonth() + 1).padStart(2, '0');
                    var dd = String(d.getDate()).padStart(2, '0');
                    dateInput.value = `${yyyy}-${mm}-${dd}`;
                } else {
                    dateInput.value = ''; 
                }
                
                document.getElementById('editExpireModal').classList.remove('hidden');
            };

            window.closeEditExpireModal = function() {
                document.getElementById('editExpireModal').classList.add('hidden');
                editingUserEmail = "";
            };

            window.quickAddDays = function(days) {
                var dateInput = document.getElementById('edit-expire-date');
                var d = new Date();
                if (dateInput.value) {
                    var currentVal = new Date(dateInput.value);
                    if (!isNaN(currentVal.getTime())) d = currentVal;
                }
                d.setDate(d.getDate() + days);
                var yyyy = d.getFullYear();
                var mm = String(d.getMonth() + 1).padStart(2, '0');
                var dd = String(d.getDate()).padStart(2, '0');
                dateInput.value = `${yyyy}-${mm}-${dd}`;
            };

            window.saveNewExpireDate = async function() {
                if (!editingUserEmail) return;
                var dateVal = document.getElementById('edit-expire-date').value;
                if (!dateVal) return alert("Vui lòng chọn ngày!");

                var btn = document.getElementById('btn-save-expire');
                btn.disabled = true; btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Đang lưu...';

                try {
                    var newDate = new Date(dateVal + 'T23:59:59');
                    var isoString = newDate.toISOString();

                    await window.db.collection('allowed_users').doc(editingUserEmail.toLowerCase()).update({
                        expiresAt: isoString
                    });

                    alert('✅ Đã cập nhật hạn sử dụng!');
                    closeEditExpireModal();
                    loadAdminUsers();
                } catch (e) {
                    alert('Lỗi lưu ngày: ' + e.message);
                    btn.disabled = false; btn.innerText = 'Lưu thay đổi';
                }
            };

            async function loadAdminRenewals() {
                var listEl = document.getElementById('admin-renewals-list');
                listEl.innerHTML = `<tr><td colspan="4" class="p-4 text-center text-slate-500"><i class="fa-solid fa-spinner fa-spin mr-2"></i>Đang tải yêu cầu...</td></tr>`;

                try {
                    var snapshot = await window.db.collection('renewal_requests').where('status', '==', 'pending').get();
                    document.getElementById('pendingCount').innerText = snapshot.size;
                    listEl.innerHTML = '';
                    if (snapshot.empty) {
                        listEl.innerHTML = `<tr><td colspan="4" class="p-4 text-center text-slate-400">Không có yêu cầu gia hạn nào đang chờ.</td></tr>`;
                        return;
                    }
                    snapshot.forEach(function(doc) {
                        var data = doc.data();
                        var tr = document.createElement('tr');
                        tr.className = "hover:bg-slate-800/50 transition";
                        var safeEmail = escapeHTML(data.email);
                        tr.innerHTML = `
                            <td class="p-3 font-semibold text-white">${safeEmail}</td>
                            <td class="p-3 text-emerald-400 font-bold">${data.packageId} (${data.amount ? data.amount.toLocaleString() : 0}đ)</td>
                            <td class="p-3 font-mono text-amber-300">${data.code}</td>
                            <td class="p-3 text-center">
                                <div class="flex items-center justify-center gap-1">
                                    <button onclick="approveRenewal('${doc.id}', '${data.email}', '${data.packageId}', ${data.days || 30})" class="px-2 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-[11px] font-bold transition" title="Duyệt yêu cầu">Duyệt</button>
                                    <button onclick="deleteRenewal('${doc.id}')" class="px-2 py-1 bg-rose-500/20 hover:bg-rose-500/40 text-rose-400 border border-rose-500/30 rounded text-[11px] font-bold transition" title="Xóa yêu cầu"><i class="fa-solid fa-trash-can"></i></button>
                                </div>
                            </td>
                        `;
                        listEl.appendChild(tr);
                    });
                } catch (err) {
                    listEl.innerHTML = `<tr><td colspan="4" class="p-4 text-center text-rose-400">Lỗi tải danh sách gia hạn.</td></tr>`;
                }
            }

            window.approveRenewal = async function(reqId, email, packageId, daysToAdd) {
                if (!confirm(`Xác nhận duyệt gia hạn cho ${email} (${packageId})?`)) return;
                try {
                    var userRef = window.db.collection('allowed_users').doc(email.toLowerCase());
                    var userDoc = await userRef.get();
                    
                    var newExp = new Date();
                    if (userDoc.exists && userDoc.data().expiresAt) {
                        var currentExp = parseDate(userDoc.data().expiresAt);
                        if (currentExp > newExp) newExp = currentExp;
                    }
                    newExp.setDate(newExp.getDate() + (daysToAdd || 30));

                    await userRef.set({ expiresAt: newExp.toISOString() }, { merge: true });
                    await window.db.collection('renewal_requests').doc(reqId).update({ status: 'approved' });

                    var msg = `✅ <b>ĐÃ DUYỆT GIA HẠN THÀNH CÔNG</b>\n\n`
                            + `👤 Tài khoản: <code>${email}</code>\n`
                            + `📦 Gói: ${packageId}\n`
                            + `📅 Hạn mới: ${newExp.toLocaleDateString('vi-VN')}\n\n`
                            + `Hệ thống đã tự động cập nhật quyền truy cập.`;
                    sendTelegramMessage(msg);

                    alert('✅ Đã duyệt gia hạn thành công!');
                    loadAdminRenewals();
                } catch (e) {
                    alert('Lỗi duyệt: ' + e.message);
                }
            };

            window.deleteRenewal = async function(reqId) {
                if (!confirm("Bạn có chắc chắn muốn xóa yêu cầu này không?")) return;
                try {
                    await window.db.collection('renewal_requests').doc(reqId).delete();
                    alert('✅ Đã xóa yêu cầu thành công!');
                    loadAdminRenewals();
                } catch (e) {
                    alert('Lỗi xóa yêu cầu: ' + e.message);
                }
            };

            window.openHistoryModal = async function(email) {
                document.getElementById('historyEmailText').innerText = "Tài khoản: " + email;
                document.getElementById('historyModal').classList.remove('hidden');
                
                var listEl = document.getElementById('history-list');
                listEl.innerHTML = `<tr><td colspan="4" class="p-4 text-center text-slate-500"><i class="fa-solid fa-spinner fa-spin mr-2"></i>Đang tải lịch sử...</td></tr>`;
                
                try {
                    var snapshot = await window.db.collection('renewal_requests')
                        .where('email', '==', email.toLowerCase())
                        .get();
                        
                    if (snapshot.empty) {
                        listEl.innerHTML = `<tr><td colspan="4" class="p-4 text-center text-slate-400">Chưa có giao dịch nào.</td></tr>`;
                        return;
                    }
                    
                    var history = [];
                    snapshot.forEach(function(doc) {
                        var data = doc.data();
                        data.id = doc.id;
                        history.push(data);
                    });
                    
                    history.sort(function(a, b) {
                        var dateA = a.createdAt ? parseDate(a.createdAt).getTime() : 0;
                        var dateB = b.createdAt ? parseDate(b.createdAt).getTime() : 0;
                        return dateB - dateA;
                    });
                    
                    listEl.innerHTML = '';
                    history.forEach(function(data) {
                        var dateStr = '—';
                        if (data.createdAt) {
                            var d = parseDate(data.createdAt);
                            if (d) {
                                dateStr = d.toLocaleDateString('vi-VN') + ' ' + d.toLocaleTimeString('vi-VN', {hour: '2-digit', minute:'2-digit'});
                            }
                        }
                        
                        var statusStr = '';
                        if (data.status === 'pending') statusStr = '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">Chờ duyệt</span>';
                        else if (data.status === 'approved') statusStr = '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">Thành công</span>';
                        else statusStr = `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-800 text-slate-400 border border-slate-700">${data.status}</span>`;
                        
                        var tr = document.createElement('tr');
                        tr.className = "hover:bg-slate-800/50 transition";
                        tr.innerHTML = `
                            <td class="p-2 text-slate-300">${dateStr}</td>
                            <td class="p-2 text-emerald-400 font-bold">${data.packageId} (${data.amount ? data.amount.toLocaleString() : 0}đ)</td>
                            <td class="p-2 font-mono text-amber-300">${data.code}</td>
                            <td class="p-2">${statusStr}</td>
                        `;
                        listEl.appendChild(tr);
                    });
                    
                } catch(e) {
                    listEl.innerHTML = `<tr><td colspan="4" class="p-4 text-center text-rose-400">Lỗi tải lịch sử: ${e.message}</td></tr>`;
                }
            };

            window.closeHistoryModal = function() {
                document.getElementById('historyModal').classList.add('hidden');
            };

            function showMsg(id, text, type) {
                var el = document.getElementById(id);
                if(!el) return;
                el.className = 'auth-msg show ' + (type || 'error');
                el.innerHTML = text;
            }
        });
    })();
    </script>
    """
    
    js_template = js_template.replace('__TRIAL_DAYS__', str(trial_days))
    js_template = js_template.replace('__BANK_CONFIG__', bank_config_js)
    
    return js_template
