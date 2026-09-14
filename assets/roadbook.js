(() => {
  "use strict";

  const dataNode = document.getElementById("roadbook-data");
  if (!dataNode) return;
  const roadbook = JSON.parse(dataNode.textContent);
  const tripId = roadbook.meta?.trip_id || `${roadbook.meta?.destination || "trip"}-${roadbook.meta?.start_date || "undated"}`;
  const storageKey = `travel-roadbook:v1:${tripId}`;
  const status = document.getElementById("roadbook-status");

  function loadState() {
    try { return JSON.parse(localStorage.getItem(storageKey)) || {}; }
    catch (_) { return {}; }
  }

  function saveState(state) {
    try { localStorage.setItem(storageKey, JSON.stringify(state)); }
    catch (_) { /* Offline reading still works when storage is unavailable. */ }
  }

  const state = loadState();
  state.checked ||= {};
  state.budget ||= {};

  function announce(message) {
    if (status) status.textContent = message;
  }

  function bindChecks(selector) {
    document.querySelectorAll(selector).forEach((input) => {
      const key = input.dataset.key;
      input.checked = Boolean(state.checked[key]);
      input.addEventListener("change", () => {
        state.checked[key] = input.checked;
        saveState(state);
        announce(input.checked ? "已标记完成" : "已取消完成");
      });
    });
  }

  function recalculateBudget() {
    let total = 0;
    document.querySelectorAll(".budget-input").forEach((input) => {
      total += Number(input.value) || 0;
    });
    const output = document.getElementById("budget-total");
    if (output) output.textContent = new Intl.NumberFormat().format(total);
    return total;
  }

  document.querySelectorAll(".budget-input").forEach((input) => {
    const key = input.dataset.category;
    if (state.budget[key] !== undefined) input.value = state.budget[key];
    input.addEventListener("input", () => {
      state.budget[key] = Number(input.value) || 0;
      saveState(state);
      recalculateBudget();
      announce("预算已更新");
    });
  });

  function shiftTime(value, delta) {
    const [hour, minute] = value.split(":").map(Number);
    const shifted = (hour * 60 + minute + delta + 1440) % 1440;
    return `${String(Math.floor(shifted / 60)).padStart(2, "0")}:${String(shifted % 60).padStart(2, "0")}`;
  }

  document.addEventListener("click", (event) => {
    const button = event.target.closest("[data-action]");
    if (!button) return;
    if (button.dataset.action === "print") window.print();
    if (button.dataset.action === "toggle-details") {
      const details = button.closest(".timeline-copy")?.querySelector(".item-details");
      if (!details) return;
      details.hidden = !details.hidden;
      button.setAttribute("aria-expanded", String(!details.hidden));
      button.textContent = details.hidden ? "展开详情" : "收起详情";
    }
    if (button.dataset.action === "shift-day") {
      const day = button.closest(".day");
      const delta = Number(day?.querySelector(".shift-control input")?.value) || 0;
      day?.querySelectorAll(".timeline-time").forEach((time) => {
        const values = time.querySelectorAll("span");
        values[0].textContent = shiftTime(time.dataset.start, delta);
        values[1].textContent = shiftTime(time.dataset.end, delta);
      });
      announce(`当天时间已顺延 ${delta} 分钟`);
    }
  });

  bindChecks(".item-check, .packing-check");
  recalculateBudget();
})();
