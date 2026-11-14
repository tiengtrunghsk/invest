# -*- coding: utf-8 -*-
"""giaodien_admin.py — Module build nội dung tab "Công cụ Admin"."""

def build_admin_tools_tab_html(price_api_url):
    """Trả về CHỈ nội dung tab Công cụ Admin (không có <html>, <head>, <body>)."""
    return f"""
    <div class="flex flex-col h-full">
        <!-- Tiêu đề -->
        <div class="mb-4">
            <h3 class="text-base font-black text-rose-400"><i class="fa-solid fa-gears mr-2"></i>Công cụ Quản trị Hệ thống</h3>
            <p class="text-xs text-slate-400 mt-1">Chỉ Super Admin mới thấy tab này. Các thao tác dưới đây ảnh hưởng trực tiếp đến Server API.</p>
        </div>

        <!-- Trạng thái Server -->
        <div class="bg-slate-950/60 p-3 rounded-lg border border-slate-700 mb-4">
            <div class="flex justify-between items-center mb-2">
                <span class="text-xs font-bold text-blue-400"><i class="fa-solid fa-server mr-1"></i>Trạng thái Server API</span>
                <button onclick="checkAdminStatus()" class="text-[10px] px-2 py-1 bg-slate-800 hover:bg-slate-700 text-white rounded border border-slate-600 transition">
                    <i class="fa-solid fa-rotate mr-1"></i>Làm mới
                </button>
            </div>
            <div class="text-[11px] space-y-1">
                <div class="flex justify-between"><span class="text-slate-400">URL:</span> <span class="font-mono text-emerald-300 text-[10px]">{price_api_url}</span></div>
                <div class="flex justify-between"><span class="text-slate-400">Trạng thái:</span> <span id="admin-crawl-status" class="font-bold text-slate-300">Đang kiểm tra...</span></div>
            </div>
        </div>

        <!-- Cấu hình FHSC Key -->
        <div class="bg-slate-950/60 p-3 rounded-lg border border-slate-700 mb-4">
            <h4 class="text-xs font-bold text-amber-400 mb-2"><i class="fa-solid fa-key mr-1"></i>FHSC API Key</h4>
            <div class="flex gap-2">
                <input type="password" id="admin-fhsc-key-input" placeholder="Nhập key mới..." class="flex-1 bg-slate-900 border border-slate-600 rounded px-3 py-1.5 text-xs focus:outline-none focus:border-amber-500">
                <button onclick="saveAdminFhscKey()" class="px-3 py-1.5 bg-amber-600 hover:bg-amber-500 text-white rounded text-xs font-bold transition">
                    <i class="fa-solid fa-floppy-disk"></i> Lưu
                </button>
            </div>
            <div id="admin-key-msg" class="mt-1 text-[10px] font-bold hidden"></div>
        </div>

        <!-- Cào dữ liệu -->
        <div class="bg-slate-950/60 p-3 rounded-lg border border-slate-700 mb-4">
            <h4 class="text-xs font-bold text-purple-400 mb-2"><i class="fa-solid fa-download mr-1"></i>Cào Dữ liệu Hàng loạt</h4>
            <div class="grid grid-cols-2 gap-2">
                <button onclick="callAdminApi('/api/force-history', 'Cào nến 30 ngày')" class="admin-action-btn p-2 bg-slate-800 hover:bg-slate-700 border border-slate-600 rounded text-[10px] font-bold transition flex flex-col items-center gap-1">
                    <i class="fa-solid fa-chart-line text-emerald-400 text-base"></i> Nến 30 Ngày
                </button>
                <button onclick="callAdminApi('/api/crawl-full-history', 'Cào full 10 năm nến')" class="admin-action-btn p-2 bg-slate-800 hover:bg-slate-700 border border-slate-600 rounded text-[10px] font-bold transition flex flex-col items-center gap-1">
                    <i class="fa-solid fa-clock-rotate-left text-emerald-400 text-base"></i> Full 10 Năm
                </button>
                <button onclick="callAdminApi('/api/force-bctc?limit=15', 'Cào BCTC nhóm 15')" class="admin-action-btn p-2 bg-slate-800 hover:bg-slate-700 border border-slate-600 rounded text-[10px] font-bold transition flex flex-col items-center gap-1">
                    <i class="fa-solid fa-file-invoice-dollar text-amber-400 text-base"></i> BCTC (15 mã)
                </button>
                <button onclick="callAdminApi('/api/crawl-full-bctc', 'Cào full BCTC')" class="admin-action-btn p-2 bg-slate-800 hover:bg-slate-700 border border-slate-600 rounded text-[10px] font-bold transition flex flex-col items-center gap-1">
                    <i class="fa-solid fa-database text-amber-400 text-base"></i> Full BCTC
                </button>
                <button onclick="callAdminApi('/api/crawl-ratios', 'Cào chỉ số P/E, ROE')" class="admin-action-btn p-2 bg-slate-800 hover:bg-slate-700 border border-slate-600 rounded text-[10px] font-bold transition flex flex-col items-center gap-1 col-span-2">
                    <i class="fa-solid fa-percent text-cyan-400 text-base"></i> Cào Chỉ số (P/E, ROE)
                </button>
            </div>
        </div>

        <!-- Chấm điểm & AI -->
        <div class="bg-slate-950/60 p-3 rounded-lg border border-slate-700 mb-4">
            <h4 class="text-xs font-bold text-rose-400 mb-2"><i class="fa-solid fa-brain mr-1"></i>Chấm điểm & Phân tích AI</h4>
            <div class="grid grid-cols-1 gap-2">
                <button onclick="callAdminApi('/api/force-screener', 'Chấm điểm lại toàn bộ', true)" class="admin-action-btn p-2 bg-indigo-600 hover:bg-indigo-500 rounded text-xs font-bold transition flex items-center justify-center gap-1">
                    <i class="fa-solid fa-calculator"></i> Chấm điểm lại toàn bộ
                </button>
                <button onclick="runAdminFullAI()" class="admin-action-btn p-2 bg-fuchsia-600 hover:bg-fuchsia-500 rounded text-xs font-bold transition flex items-center justify-center gap-1">
                    <i class="fa-solid fa-robot"></i> Chạy AI Toàn bộ 100 mã
                </button>
                <div class="flex gap-1">
                    <input type="text" id="admin-ai-symbol-input" placeholder="Mã test AI..." class="flex-1 bg-slate-900 border border-slate-600 rounded px-2 py-1.5 text-xs focus:outline-none focus:border-fuchsia-500 uppercase">
                    <button onclick="runAdminSingleAI()" class="admin-action-btn px-3 py-1.5 bg-purple-600 hover:bg-purple-500 rounded text-xs font-bold transition whitespace-nowrap">
                        <i class="fa-solid fa-flask mr-1"></i> Test
                    </button>
                </div>
            </div>
        </div>

        <!-- Điều khiển Cào tự động -->
        <div class="bg-slate-950/60 p-3 rounded-lg border border-slate-700">
            <h4 class="text-xs font-bold text-amber-400 mb-2"><i class="fa-solid fa-power-off mr-1"></i>Điều khiển Cào Tự động</h4>
            <div class="grid grid-cols-2 gap-2">
                <button onclick="callAdminApi('/api/pause-crawl', 'Tạm dừng cào', true)" class="admin-action-btn p-2 bg-red-900 hover:bg-red-800 border border-red-600 rounded text-[10px] font-bold transition flex items-center justify-center gap-1">
                    <i class="fa-solid fa-pause text-red-400"></i> Tạm dừng
                </button>
                <button onclick="callAdminApi('/api/resume-crawl', 'Tiếp tục cào', true)" class="admin-action-btn p-2 bg-green-900 hover:bg-green-800 border border-green-600 rounded text-[10px] font-bold transition flex items-center justify-center gap-1">
                    <i class="fa-solid fa-play text-green-400"></i> Tiếp tục
                </button>
            </div>
        </div>

        <!-- Log hiển thị kết quả -->
        <div class="mt-4 bg-black rounded-lg border border-slate-700 p-2 h-32 overflow-y-auto font-mono text-[10px]" id="admin-tools-log">
            <div class="text-slate-500">// Log kết quả sẽ hiển thị ở đây...</div>
        </div>
    </div>
    
    <script>
    // ==================== ADMIN TOOLS SCRIPT ====================
    (function() {{
        const ADMIN_API_URL = "{price_api_url}";
        const ADMIN_SECRET = "959214"; // Key bảo mật của bạn
        let adminIsBusy = false;

        function adminLog(msg, type = 'info') {{
            const el = document.getElementById('admin-tools-log');
            if (!el) return;
            const time = new Date().toLocaleTimeString('vi-VN');
            let color = 'text-slate-300';
            if (type === 'error') color = 'text-rose-400';
            if (type === 'success') color = 'text-emerald-400';
            if (type === 'warning') color = 'text-amber-400';
            
            const line = document.createElement('div');
            line.className = color;
            line.innerText = `[${{time}}] ${{msg}}`;
            el.appendChild(line);
            el.scrollTop = el.scrollHeight;
            if (el.children.length > 200) el.removeChild(el.firstChild);
        }}

        function toggleAdminBtns(enable) {{
            const btns = document.querySelectorAll('.admin-action-btn');
            btns.forEach(b => {{
                if (enable) {{
                    b.classList.remove('opacity-50', 'cursor-not-allowed');
                    b.disabled = false;
                }} else {{
                    b.classList.add('opacity-50', 'cursor-not-allowed');
                    b.disabled = true;
                }}
            }});
        }}

        window.checkAdminStatus = async function() {{
            try {{
                const res = await fetch(`${{ADMIN_API_URL}}/api/status`);
                const data = await res.json();
                const el = document.getElementById('admin-crawl-status');
                if (!el) return;
                
                if (data.is_crawling) {{
                    el.innerText = "ĐANG XỬ LÝ (BẬN)";
                    el.className = "font-bold text-amber-400 animate-pulse";
                    adminIsBusy = true;
                    toggleAdminBtns(false);
                }} else if (data.is_paused) {{
                    el.innerText = "ĐANG TẠM DỪNG";
                    el.className = "font-bold text-rose-400";
                    adminIsBusy = false;
                    toggleAdminBtns(true);
                }} else {{
                    el.innerText = "SẴN SÀNG";
                    el.className = "font-bold text-emerald-400";
                    adminIsBusy = false;
                    toggleAdminBtns(true);
                }}
            }} catch (e) {{
                const el = document.getElementById('admin-crawl-status');
                if (el) {{
                    el.innerText = "MẤT KẾT NỐI";
                    el.className = "font-bold text-rose-500";
                }}
            }}
        }};

        // Hàm callAdminApi nâng cấp: Nhận thêm tham số requireKey để quyết định có gửi key hay không
        window.callAdminApi = async function(endpoint, actionName, requireKey = false) {{
            if (adminIsBusy) {{
                alert("Server đang bận, vui lòng đợi!");
                return;
            }}
            
            adminLog(`Đang gửi yêu cầu: ${{actionName}}...`, "warning");
            toggleAdminBtns(false);
            
            let url = `${{ADMIN_API_URL}}${{endpoint}}`;
            
            // Nếu API yêu cầu key (requireKey = true), tự động nối thêm ?key=
            if (requireKey) {{
                if (url.includes('?')) {{
                    url += `&key=${{ADMIN_SECRET}}`;
                }} else {{
                    url += `?key=${{ADMIN_SECRET}}`;
                }}
            }}

            try {{
                const res = await fetch(url);
                const data = await res.json();
                if (data.status === 'success') {{
                    adminLog(`✅ ${{actionName}}: ${{data.message || 'Thành công'}}`, "success");
                    setTimeout(checkAdminStatus, 2000);
                }} else {{
                    adminLog(`❌ ${{actionName}} lỗi: ${{data.message}}`, "error");
                    toggleAdminBtns(true);
                }}
            }} catch (e) {{
                adminLog(`❌ Lỗi kết nối: ${{e.message}}`, "error");
                toggleAdminBtns(true);
            }}
        }};

        // Chạy AI toàn bộ (Truyền key bảo mật lên Server)
        window.runAdminFullAI = async function() {{
            if (adminIsBusy) return alert("Server đang bận!");
            if (!confirm("Chạy AI cho TOÀN BỘ 100 mã?\\nTiến trình có thể mất 5-10 phút.")) return;
            
            adminLog(`🚀 Kích hoạt chạy AI toàn bộ 100 mã...`, "warning");
            toggleAdminBtns(false);
            
            try {{
                const res = await fetch(`${{ADMIN_API_URL}}/api/admin/force-ai?key=${{ADMIN_SECRET}}`);
                const data = await res.json();
                if (data.status === 'success') {{
                    adminLog(`✅ ${{data.message}}`, "success");
                    adminLog(`👉 Xem log Render để theo dõi tiến trình.`, "info");
                }} else {{
                    adminLog(`❌ Lỗi: ${{data.message}}`, "error");
                    toggleAdminBtns(true);
                }}
            }} catch (e) {{
                adminLog(`❌ Lỗi kết nối: ${{e.message}}`, "error");
                toggleAdminBtns(true);
            }}
        }};

        // Test AI 1 mã (Truyền key bảo mật lên Server)
        window.runAdminSingleAI = async function() {{
            if (adminIsBusy) return alert("Server đang bận!");
            const symbol = document.getElementById('admin-ai-symbol-input').value.trim().toUpperCase();
            if (!symbol) return alert("Vui lòng nhập mã cổ phiếu!");
            
            adminLog(`Đang kích hoạt AI cho mã ${{symbol}}...`, "warning");
            toggleAdminBtns(false);
            
            try {{
                const res = await fetch(`${{ADMIN_API_URL}}/api/admin/force-ai-single?symbol=${{symbol}}&key=${{ADMIN_SECRET}}`);
                const data = await res.json();
                if (data.status === 'success') {{
                    adminLog(`✅ Đã gửi lệnh chạy AI cho ${{symbol}}.`, "success");
                    adminLog(`${{data.message}}`, "info");
                }} else {{
                    adminLog(`❌ AI lỗi: ${{data.message}}`, "error");
                }}
            }} catch (e) {{
                adminLog(`❌ Lỗi kết nối: ${{e.message}}`, "error");
            }} finally {{
                toggleAdminBtns(true);
            }}
        }};

        window.saveAdminFhscKey = async function() {{
            const key = document.getElementById('admin-fhsc-key-input').value.trim();
            if (!key) return alert("Vui lòng nhập Key!");
            
            const msgEl = document.getElementById('admin-key-msg');
            msgEl.classList.remove('hidden');
            msgEl.className = "mt-1 text-[10px] font-bold text-amber-400";
            msgEl.innerText = "Đang lưu...";
            
            try {{
                const res = await fetch(`${{ADMIN_API_URL}}/api/set-fhsc-key`, {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ key: key }})
                }});
                const data = await res.json();
                if (data.status === 'success') {{
                    msgEl.className = "mt-1 text-[10px] font-bold text-emerald-400";
                    msgEl.innerText = "✅ Lưu thành công!";
                    adminLog("Đã cập nhật FHSC API Key.", "success");
                }} else {{
                    msgEl.className = "mt-1 text-[10px] font-bold text-rose-400";
                    msgEl.innerText = "❌ " + data.message;
                }}
            }} catch (e) {{
                msgEl.className = "mt-1 text-[10px] font-bold text-rose-400";
                msgEl.innerText = "❌ Lỗi kết nối Server";
            }}
        }};

        // Khởi động kiểm tra trạng thái khi tab được mở
        setTimeout(checkAdminStatus, 500);
    }})();
    </script>
    """
