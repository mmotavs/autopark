// Симуляция данных пользователя (в будущем — из базы данных)
document.addEventListener("DOMContentLoaded", () => {
    const userName = document.getElementById("userName");
    const userEmail = document.getElementById("userEmail");

    // Пример: данные могут быть сохранены после входа
    const userData = JSON.parse(localStorage.getItem("userData")) || {
        name: "Мария Александровна",
        email: "maria@example.com"
    };

    userName.textContent = userData.name;
    userEmail.textContent = userData.email;

    // Выход из аккаунта
    document.getElementById("logoutBtn").addEventListener("click", () => {
        alert("Вы вышли из аккаунта!");
        localStorage.removeItem("userData");
        window.location.href = "login.html";
    });

    // Удаление аккаунта
    document.getElementById("deleteBtn").addEventListener("click", () => {
        const confirmDelete = confirm("Вы уверены, что хотите удалить аккаунт?");
        if (confirmDelete) {
            alert("Аккаунт удалён.");
            localStorage.removeItem("userData");
            window.location.href = "index.html";
        }
    });
});
