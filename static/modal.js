// =========================================================
// 通用模态框：openModal(配置对象)
// =========================================================
function openModal({ title, fields, values = {}, onSubmit }) {
    // 遮罩 + 容器
    const mask = document.createElement("div");
    mask.className = "modal-mask";
    mask.innerHTML = `
        <div class="modal">
            <div class="modal-header">
                <h2>${title}</h2>
                <button class="modal-close" type="button">×</button>
            </div>
            <form class="modal-body" id="modal-form">
                ${fields.map(f => `
                    <label class="form-row">
                        <span class="form-label">${f.label}</span>
                        <input class="form-input"
                               name="${f.name}"
                               type="${f.type || "text"}"
                               value="${values[f.name] ?? ""}"
                               ${f.required ? "required" : ""}
                               placeholder="${f.placeholder || ""}">
                    </label>
                `).join("")}
            </form>
            <div class="modal-footer">
                <button class="btn" type="button" data-role="cancel">取消</button>
                <button class="btn btn-primary" type="button" data-role="submit">保存</button>
            </div>
        </div>
    `;
    document.body.appendChild(mask);

    const close = () => mask.remove();

    mask.querySelector(".modal-close").onclick = close;
    mask.querySelector('[data-role="cancel"]').onclick = close;
    mask.onclick = e => { if (e.target === mask) close(); };

    mask.querySelector('[data-role="submit"]').onclick = async () => {
        const form = mask.querySelector("#modal-form");
        const data = {};
        for (const f of fields) {
            data[f.name] = form.elements[f.name].value.trim();
        }
        try {
            await onSubmit(data);
            close();
        } catch (err) {
            alert("保存失败：" + err.message);
        }
    };
}