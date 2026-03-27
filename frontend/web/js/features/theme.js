// Apply the correct theme and sync the icon
function applyTheme(theme) {
    document.documentElement.setAttribute("data-bs-theme", theme)
    localStorage.setItem("theme", theme)

    const sun = document.getElementById("icon-sun")
    const moon = document.getElementById("icon-moon")
    if (!sun || !moon) return

    if (theme === "dark") {
        sun.style.display = "block" 
        moon.style.display = "none"
    } else {
        sun.style.display = "none"
        moon.style.display = "block"
    }
}

// Initialize with the saved theme
const current = localStorage.getItem("theme") || "light"
applyTheme(current)

// get the button
document.getElementById("btn-theme-toggle")?.addEventListener("click", () => {
    const next = document.documentElement.getAttribute("data-bs-theme") === "dark" ? "light" : "dark"
    applyTheme(next)
})

export { applyTheme }