function outputUpdate(radius) {
    document.querySelector('#selected_radius').value = radius + " km";
}

document.addEventListener("DOMContentLoaded", () => {
    const rows = document.querySelectorAll("tr[data-href]");
    rows.forEach(row => {
        row.addEventListener("click", () => {
            window.location.href = row.dataset.href;
        });
    });
});