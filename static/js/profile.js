// Переключение вкладок на странице профиля
document.addEventListener("DOMContentLoaded", () => {
    // Функция переключения вкладок
    const navBtns = document.querySelectorAll(".nav-btn");
    const tabPanes = document.querySelectorAll(".tab-pane");

    navBtns.forEach(btn => {
        btn.addEventListener("click", (e) => {
            // Если это ссылка выхода, не переключаем вкладку
            if (btn.classList.contains("logout-btn")) {
                return;
            }

            e.preventDefault();

            // Получаем ID целевой вкладки из data-target
            const targetId = btn.getAttribute("data-target");
            
            // Если это кнопка без data-target, пропускаем
            if (!targetId) return;

            // Убираем класс active у всех кнопок и вкладок
            navBtns.forEach(b => b.classList.remove("active"));
            tabPanes.forEach(pane => pane.classList.remove("active"));

            // Добавляем класс active к нажатой кнопке
            btn.classList.add("active");

            // Показываем целевую вкладку
            const targetPane = document.getElementById(targetId);
            if (targetPane) {
                targetPane.classList.add("active");
            }
        });
    });

    // Обработчик выхода из аккаунта
    const logoutBtn = document.querySelector(".logout-btn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", (e) => {
            e.preventDefault();
            alert("Вы вышли из аккаунта!");
            localStorage.removeItem("userData");
            window.location.href = "{{ url_for('login') }}";
        });
    }

    // Обработчик удаления аккаунта
    const deleteBtn = document.querySelector(".delete-btn");
    if (deleteBtn) {
        deleteBtn.addEventListener("click", (e) => {
            e.preventDefault();
            const confirmDelete = confirm("Вы уверены, что хотите удалить аккаунт?");
            if (confirmDelete) {
                alert("Аккаунт удалён.");
                localStorage.removeItem("userData");
                window.location.href = "{{ url_for('index') }}";
            }
        });
    }
});
