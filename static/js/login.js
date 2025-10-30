async function handleLogin(event) {
    event.preventDefault();
    console.log('Попытка входа...');
    
    const formData = {
        email: document.getElementById('email').value,
        password: document.getElementById('password').value
    };

    const errorMessage = document.getElementById('error-message');

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        console.log('Ответ сервера:', data);

        if (response.ok) {
            localStorage.setItem('userRole', data.user.role);
            localStorage.setItem('userName', data.user.name);
            
            console.log('Роль пользователя:', data.user.role);
            
            if (data.user.role === 'admin') {
                console.log('Перенаправление на панель администратора...');
                window.location.href = '/admin/dashboard';
            } else {
                console.log('Перенаправление на главную страницу...');
                window.location.href = '/';
            }
        } else {
            errorMessage.textContent = data.error || 'Неверный email или пароль';
            errorMessage.style.display = 'block';
        }
    } catch (error) {
        console.error('Ошибка:', error);
        errorMessage.textContent = 'Ошибка сервера';
        errorMessage.style.display = 'block';
    }
}