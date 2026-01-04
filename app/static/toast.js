document.addEventListener("DOMContentLoaded", () => {
    const toast = document.getElementById("toast");
    if (!toast) return;

    toast.textContent = toast.dataset.message;
    toast.classList.add("show");

    setTimeout(() => {
        toast.classList.remove("show");
    }, 3000);
})