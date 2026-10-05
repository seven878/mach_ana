// =========================================================
// 配置
// =========================================================
const API_BASE = "";   // 同源，留空即可

// =========================================================
// 各视图的列定义
// =========================================================
const VIEWS = {
    customers: {
        title: "客户",
        url: "/customers",
        columns: [
            { key: "id",         label: "ID" },
            { key: "name",       label: "客户公司名" },
            { key: "contact",    label: "联系方式" },
            { key: "phone",      label: "手机号" },
        ],
        formFields: [
        { name: "name",    label: "客户公司名", required: true },
        { name: "contact", label: "联系方式" },
        { name: "phone",   label: "手机号" },
    ],
    },
    orders: {
        title: "订单",
        url: "/orders",
        columns: [
            { key: "id",           label: "ID" },
            { key: "order_no",     label: "订单编号" },
            { key: "customer_id",  label: "客户ID" },
            { key: "status",       label: "状态", render: renderStatus },
            { key: "due_date",     label: "交期", render: renderDate },
            { key: "total_amount", label: "总金额", render: renderMoney },
            { key: "remark",       label: "备注" },
        ],
    },
    items: {
        title: "订单 Item",
        url: "/orders/0/items",   // 占位，见下方 fetchItems 特殊处理
        columns: [
            { key: "id",          label: "ID" },
            { key: "order_id",    label: "订单ID" },
            { key: "part_name",   label: "零件名" },
            { key: "material",    label: "材料" },
            { key: "quantity",    label: "数量" },
            { key: "unit_price",  label: "单价", render: renderMoney },
            { key: "process_req", label: "工艺要求" },
        ],
    },
};

// =========================================================
// 渲染辅助函数
// =========================================================
function renderMoney(v) {
    if (v === null || v === undefined || v === "") return "-";
    return "¥" + Number(v).toFixed(2);
}

function renderDate(v) {
    if (!v) return "-";
    // ISO 字符串，取日期部分
    return String(v).replace("T", " ").slice(0, 16);
}

function renderStatus(v) {
    const labels = {
        pending:       "待定",
        to_production: "待生产",
        in_production: "生产中",
        finished:      "生产完成",
        shipped:       "已发货",
        cancelled:     "已取消",
    };
    const text = labels[v] || v;
    return `<span class="badge badge-${v}">${text}</span>`;
}

function renderCell(col, row) {
    const raw = row[col.key];
    if (col.render) return col.render(raw, row);
    if (raw === null || raw === undefined || raw === "") return "-";
    return escapeHtml(String(raw));
}

function escapeHtml(s) {
    return s.replace(/[&<>"']/g, c => ({
        "&": "&amp;", "<": "&lt;", ">": "&gt;",
        '"': "&quot;", "'": "&#39;"
    }[c]));
}

// =========================================================
// 状态
// =========================================================
let currentView = "customers";

// =========================================================
// 数据获取
// =========================================================
async function fetchData(view) {
    if (view === "items") {
        return fetchAllItems();
    }
    const res = await fetch(API_BASE + VIEWS[view].url);
    if (!res.ok) throw new Error(`请求失败：${res.status}`);
    return res.json();
}

/**
 * items 没有全局列表接口，需要：
 * 1. 先拉订单列表
 * 2. 再逐个订单拉明细
 * 3. 合并成一个数组
 */
async function fetchAllItems() {
    const ordersRes = await fetch(API_BASE + "/orders");
    if (!ordersRes.ok) throw new Error(`订单请求失败：${ordersRes.status}`);
    const orders = await ordersRes.json();

    const results = [];
    for (const o of orders) {
        const r = await fetch(API_BASE + `/orders/${o.id}/items`);
        if (!r.ok) continue;
        const items = await r.json();
        for (const it of items) results.push(it);
    }
    return results;
}

// =========================================================
// 渲染
// =========================================================
function renderTableHead(view) {
    const cols = VIEWS[view].columns;
    const tr = document.createElement("tr");
    for (const c of cols) {
        const th = document.createElement("th");
        th.textContent = c.label;
        tr.appendChild(th);
    }
    // 操作列
    const thAction = document.createElement("th");
    thAction.textContent = "操作";
    tr.appendChild(thAction);

    const thead = document.getElementById("table-head");
    thead.innerHTML = "";
    thead.appendChild(tr);
}

function renderTableBody(view, rows) {
    const tbody = document.getElementById("table-body");
    tbody.innerHTML = "";

    const cols = VIEWS[view].columns;

    for (const row of rows) {
        const tr = document.createElement("tr");

        for (const c of cols) {
            const td = document.createElement("td");
            td.innerHTML = renderCell(c, row);
            tr.appendChild(td);
        }

        // 操作按钮
        const tdAction = document.createElement("td");
        tdAction.innerHTML = `
            <div class="actions">
                <button class="btn btn-sm btn-edit"
                        data-action="edit" data-id="${row.id}">修改</button>
                <button class="btn btn-sm btn-delete"
                        data-action="delete" data-id="${row.id}">删除</button>
            </div>
        `;
        tr.appendChild(tdAction);

        tbody.appendChild(tr);
    }
}

// =========================================================
// 主流程
// =========================================================
async function loadView(view) {
    currentView = view;

    // 更新标题、侧边栏高亮
    document.getElementById("page-title").textContent = VIEWS[view].title;
    document.querySelectorAll(".menu-item").forEach(el => {
        el.classList.toggle("active", el.dataset.view === view);
    });

    // 渲染表头
    renderTableHead(view);

    // 显示 loading
    const loading = document.getElementById("loading");
    const emptyTip = document.getElementById("empty-tip");
    const table = document.querySelector(".data-table");
    loading.style.display = "block";
    emptyTip.style.display = "none";
    table.style.display = "none";

    try {
        const rows = await fetchData(view);
        loading.style.display = "none";

        if (!rows || rows.length === 0) {
            emptyTip.style.display = "block";
        } else {
            table.style.display = "table";
            renderTableBody(view, rows);
        }
    } catch (err) {
        loading.style.display = "none";
        emptyTip.style.display = "block";
        emptyTip.textContent = "加载失败：" + err.message;
        console.error(err);
    }
}

// =========================================================
// 事件绑定
// =========================================================
function bindEvents() {
    // 侧边栏切换
    document.querySelectorAll(".menu-item").forEach(el => {
        el.addEventListener("click", e => {
            e.preventDefault();
            loadView(el.dataset.view);
        });
    });

    document.getElementById("btn-add").addEventListener("click", () => {
    const viewCfg = VIEWS[currentView];
    console.log(currentView)
//    if (currentView !== "customers") {
//        alert("该视图的新增功能待实现");
//        return;
//    }

    openModal({
        title: "新增客户",
        fields: viewCfg.formFields,
        onSubmit: async (data) => {
            const res = await fetch(API_BASE + viewCfg.url, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data),
            });
            if (!res.ok) {
                const err = await res.json().catch(() => ({}));
                throw new Error(err.detail || res.statusText);
            }
            await loadView(currentView);   // 刷新列表
        },
    });
});
    // 表格内的修改 / 删除（事件委托）
    document.getElementById("table-body").addEventListener("click", e => {
        const btn = e.target.closest("button[data-action]");
        if (!btn) return;
        const action = btn.dataset.action;
        const id = btn.dataset.id;
        alert(`${action === "edit" ? "修改" : "删除"} ${currentView} #${id}（待实现）`);
    });
}

// =========================================================
// 启动
// =========================================================
document.addEventListener("DOMContentLoaded", () => {
    bindEvents();
    loadView("customers");
});