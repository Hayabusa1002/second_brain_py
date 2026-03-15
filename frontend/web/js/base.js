import { logout } from "./auth/guard.js";

const logoutBtn = document.getElementById("btn-logout");
if (logoutBtn) {
    logoutBtn.addEventListener("click", logout);
}