# -*- coding: utf-8 -*-
"""giaodien_admin.py — Nội dung tab Công cụ Admin."""

def build_admin_tools_tab_html(price_api_url):
    """Trả về nội dung tab Admin, không gồm html/head/body."""
    return f"""
    <div class="flex flex-col h-full">
      <div class="mb-4">
        <h3 class="text-base font-black text-rose-400"><i class="fa-solid fa-gears mr-2"></i>Công cụ Quản trị Hệ thống</h3>
        <p class="text-xs text-slate-400 mt-1">Theo dõi và điều khiển các tác vụ trên Server API.</p>
      </div>

      <div class="bg-slate-950/60 p-3 rounded-lg border border-slate-700 mb-4">
        <div class="flex justify-between items-center mb-2">
          <span class="text-xs font-bold text-blue-400"><i class="fa-solid fa-server mr-1"></i>Trạng thái Server API</span>
          <button onclick="checkAdminStatus()" class="text-[10px] px-2 py-1 bg-slate-800 text-white rounded border border-slate-600"><i class="fa-solid fa-rotate mr-1"></i>Làm mới</button>
        </div>
        <div class="text-[11px] space-y-1">
          <div class="flex justify-between"><span class="text-slate-400">URL:</span><span class="font-mono text-emerald-300 text-[10px]">{price_api_url}</span></div>
          <div class="flex justify-between"><span class="text-slate-400">Server:</span><span id="admin-crawl-status" class="font-bold text-slate-300">Đang kiểm tra...</span></div>
          <div class="flex justify-between"><span class="text-slate-400">Tác vụ lịch sử:</span><span id="admin-history-state" class="font-bold text-cyan-300">Chưa có</span></div>
          <div class="w-full bg-slate-800 rounded h-2 mt-2 overflow-hidden"><div id="admin-history-progress" class="bg-cyan-500 h-2" style="width:0%"></div></div>
          <div id="admin-history-detail" class="text-[10px] text-slate-400 mt-1">Chưa có tác vụ lịch sử.</div>
        </div>
      </div>

      <div class="bg-slate-950/60 p-3 rounded-lg border border-slate-700 mb-4">
        <h4 class="text-xs font-bold text-purple-400 mb-2"><i class="fa-solid fa-download mr-1"></i>Cào Dữ liệu Hàng loạt</h4>
        <div class="grid grid-cols-2 gap-2">
          <button onclick="callAdminApi('/api/force-history','Cào nến 30 ngày')" class="admin-action-btn p-2 bg-slate-800 border border-slate-600 rounded text-[10px] font-bold"><i class="fa-solid fa-chart-line text-emerald-400 text-base"></i> Nến 30 Ngày</button>
          <button onclick="callAdminApi('/api/crawl-full-history','Cào full 10 năm')" class="admin-action-btn p-2 bg-slate-800 border border-slate-600 rounded text-[10px] font-bold"><i class="fa-solid fa-clock-rotate-left text-emerald-400 text-base"></i> Full 10 Năm</button>
          <button onclick="callAdminApi('/api/force-bctc?limit=15','Cào BCTC nhóm 15')" class="admin-action-btn p-2 bg-slate-800 border border-slate-600 rounded text-[10px] font-bold"><i class="fa-solid fa-file-invoice-dollar text-amber-400 text-base"></i> BCTC (15 mã)</button>
          <button onclick="callAdminApi('/api/crawl-full-bctc','Cào full BCTC')" class="admin-action-btn p-2 bg-slate-800 border border-slate-600 rounded text-[10px] font-bold"><i class="fa-solid fa-database text-amber-400 text-base"></i> Full BCTC</button>
          <button onclick="callAdminApi('/api/crawl-ratios','Cào chỉ số P/E, ROE')" class="admin-action-btn p-2 bg-slate-800 border border-slate-600 rounded text-[10px] font-bold col-span-2"><i class="fa-solid fa-percent text-cyan-400"></i> Cào Chỉ số (P/E, ROE)</button>
        </div>
        <p class="text-[10px] text-slate-500 mt-2">Hai tác vụ lịch sử được xếp hàng tuần tự; có thể gửi yêu cầu 10 năm khi tác vụ 30 ngày đang chạy.</p>
      </div>

      <div class="bg-slate-950/60 p-3 rounded-lg border border-slate-700 mb-4">
        <h4 class="text-xs font-bold text-rose-400 mb-2"><i class="fa-solid fa-brain mr-1"></i>Chấm điểm & Phân tích AI</h4>
        <div class="grid grid-cols-1 gap-2">
          <button onclick="callAdminApi('/api/force-screener','Chấm điểm lại toàn bộ',true)" class="admin-action-btn p-2 bg-indigo-600 rounded text-xs font-bold">Chấm điểm lại toàn bộ</button>
          <button onclick="runAdminFullAI()" class="admin-action-btn p-2 bg-fuchsia-600 rounded text-xs font-bold">Chạy AI Toàn bộ 100 mã</button>
          <div class="flex gap-1">
            <input type="text" id="admin-ai-symbol-input" placeholder="Mã test AI..." class="flex-1 bg-slate-900 border border-slate-600 rounded px-2 py-1.5 text-xs uppercase">
            <button onclick="runAdminSingleAI()" class="admin-action-btn px-3 py-1.5 bg-purple-600 rounded text-xs font-bold">Test AI</button>
          </div>
        </div>
      </div>

      <div class="bg-slate-950/60 p-3 rounded-lg border border-slate-700 mb-4">
        <h4 class="text-xs font-bold text-amber-400 mb-2"><i class="fa-solid fa-power-off mr-1"></i>Điều khiển Cào Tự động</h4>
        <div class="grid grid-cols-2 gap-2">
          <button onclick="callAdminApi('/api/pause-crawl','Tạm dừng cào',true)" class="admin-action-btn p-2 bg-red-900 border border-red-600 rounded text-[10px] font-bold">Tạm dừng</button>
          <button onclick="callAdminApi('/api/resume-crawl','Tiếp tục cào',true)" class="admin-action-btn p-2 bg-green-900 border border-green-600 rounded text-[10px] font-bold">Tiếp tục</button>
        </div>
      </div>

      <div class="mt-2 bg-black rounded-lg border border-slate-700 p-2 h-36 overflow-y-auto font-mono text-[10px]" id="admin-tools-log">
        <div class="text-slate-500">// Log kết quả sẽ hiển thị ở đây...</div>
      </div>
    </div>

    <script>
    (function() {{
      const ADMIN_API_URL = "{price_api_url}".replace(/\/$/, "");
      let statusTimer = null;

      function log(msg, type) {{
        const el = document.getElementById('admin-tools-log');
        if (!el) return;
        const line = document.createElement('div');
        line.className = type === 'error' ? 'text-rose-400' : type === 'success' ? 'text-emerald-400' : type === 'warning' ? 'text-amber-400' : 'text-slate-300';
        line.innerText = '[' + new Date().toLocaleTimeString('vi-VN') + '] ' + msg;
        el.appendChild(line); el.scrollTop = el.scrollHeight;
        while (el.children.length > 200) el.removeChild(el.firstChild);
      }}

      async function getJson(url) {{
        const res = await fetch(url, {{ cache: 'no-store' }});
        let data = {{}};
        try {{ data = await res.json(); }} catch (_) {{}}
        if (!res.ok && !data.message) data.message = 'HTTP ' + res.status;
        return {{res, data}};
      }}

      window.checkAdminStatus = async function() {{
        try {{
          const [server, history] = await Promise.all([
            getJson(ADMIN_API_URL + '/api/status'),
            getJson(ADMIN_API_URL + '/api/history-crawl-status')
          ]);
          const serverEl = document.getElementById('admin-crawl-status');
          if (serverEl) serverEl.innerText = server.data.is_crawling ? 'REALTIME ĐANG CHẠY' : (server.data.is_paused ? 'TẠM DỪNG' : 'SẴN SÀNG');
          const job = history.data.job || {{}};
          const stateEl = document.getElementById('admin-history-state');
          const detailEl = document.getElementById('admin-history-detail');
          const bar = document.getElementById('admin-history-progress');
          const pct = job.total ? Math.round((job.completed || 0) * 100 / job.total) : 0;
          if (stateEl) stateEl.innerText = job.status === 'running' ? 'ĐANG CÀO' : (job.status || 'idle').toUpperCase();
          if (detailEl) detailEl.innerText = (job.message || 'Chưa có tác vụ') + ' | ' + (job.completed || 0) + '/' + (job.total || 0) + ' mã | Thành công: ' + (job.success || 0) + ' | Lỗi: ' + (job.failed || 0) + ' | Chờ: ' + (job.queued || 0);
          if (bar) bar.style.width = pct + '%';
          if (job.status === 'running' && !statusTimer) statusTimer = setInterval(window.checkAdminStatus, 5000);
          if (job.status !== 'running' && statusTimer) {{ clearInterval(statusTimer); statusTimer = null; }}
        }} catch (e) {{ log('Không lấy được trạng thái: ' + e.message, 'error'); }}
      }};

      window.callAdminApi = async function(endpoint, actionName, requireKey) {{
        let url = ADMIN_API_URL + endpoint;
        if (requireKey) {{
          const key = prompt('Nhập ADMIN_API_KEY đã cấu hình trên server:');
          if (!key) return;
          url += (url.includes('?') ? '&' : '?') + 'key=' + encodeURIComponent(key);
        }}
        log('Đang gửi yêu cầu: ' + actionName + '...', 'warning');
        try {{
          const {{res, data}} = await getJson(url);
          if (data.status === 'success') {{
            log('Đã nhận yêu cầu ' + actionName + ': ' + (data.message || 'OK'), 'success');
            if (data.job) log('Trạng thái hàng đợi: ' + JSON.stringify(data.job), 'info');
            window.checkAdminStatus();
          }} else log(actionName + ' lỗi: ' + (data.message || ('HTTP ' + res.status)), 'error');
        }} catch (e) {{ log('Lỗi kết nối: ' + e.message, 'error'); }}
      }};

      window.runAdminFullAI = async function() {{
        if (!confirm('Chạy AI cho toàn bộ mã?')) return;
        await window.callAdminApi('/api/admin/force-ai', 'Chạy AI toàn bộ', true);
      }};
      window.runAdminSingleAI = async function() {{
        const symbol = (document.getElementById('admin-ai-symbol-input')?.value || '').trim().toUpperCase();
        if (!/^[A-Z0-9]{{2,10}}$/.test(symbol)) return alert('Mã cổ phiếu không hợp lệ');
        await window.callAdminApi('/api/admin/force-ai-single?symbol=' + encodeURIComponent(symbol), 'Test AI ' + symbol, true);
      }};

      window.checkAdminStatus();
      if (statusTimer) clearInterval(statusTimer);
      statusTimer = setInterval(window.checkAdminStatus, 15000);
    }})();
    </script>
    """
