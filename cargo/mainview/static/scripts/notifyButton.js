document.addEventListener("DOMContentLoaded", function() {
    const btn = document.getElementById("notif-btn");
    const dropdown = document.getElementById("notification-dropdown");

    btn.addEventListener("click", (e) => {
        e.stopPropagation();
        dropdown.classList.toggle("hidden");
    });

    document.addEventListener("click", (e) => {
        if (!dropdown.contains(e.target) && !btn.contains(e.target)) {
            dropdown.classList.add("hidden");
        }
    });
});