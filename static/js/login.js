document.addEventListener("DOMContentLoaded", () => {
    const loginTab = document.getElementById("login-tab");
    const registerTab = document.getElementById("register-tab");
    const loginForm = document.getElementById("login-form");
    const registerForm = document.getElementById("register-form");

    // Переключение вкладок
    loginTab.addEventListener("click", () => {
        loginTab.classList.add("active");
        registerTab.classList.remove("active");
        loginForm.classList.add("active");
        registerForm.classList.remove("active");
    });

    registerTab.addEventListener("click", () => {
        registerTab.classList.add("active");
        loginTab.classList.remove("active");
        registerForm.classList.add("active");
        loginForm.classList.remove("active");
    });

    // Имитируем отправку форм
    loginForm.addEventListener("submit", (e) => {
        e.preventDefault();
        alert("Добро пожаловать! Вход выполнен успешно ✅");
        loginForm.reset();
    });

    registerForm.addEventListener("submit", (e) => {
        e.preventDefault();
        alert("Регистрация успешно завершена! 🎉");
        registerForm.reset();
    });
});

// Плавная прокрутка при клике на ссылки
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            const navbarHeight = document.querySelector('.navbar').offsetHeight;
            const targetPosition = targetElement.offsetTop - navbarHeight;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// Скрытие/показ шапки при прокрутке
let lastScrollTop = 0;
let scrollThreshold = 100; // Порог прокрутки для начала скрытия
const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', function() {
    let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    // Если в самом верху страницы - показываем шапку
    if (scrollTop <= scrollThreshold) {
        navbar.classList.remove('hidden');
    } 
    // Если прокручиваем вниз - скрываем
    else if (scrollTop > lastScrollTop && scrollTop > scrollThreshold) {
        navbar.classList.add('hidden');
    } 
    // Если прокручиваем вверх - показываем
    else if (scrollTop < lastScrollTop) {
        navbar.classList.remove('hidden');
    }
    
    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
}, false);




