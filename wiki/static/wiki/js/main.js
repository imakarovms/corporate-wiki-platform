document.addEventListener('DOMContentLoaded', function() {
    // Утилиты для работы с закладками
    document.querySelectorAll('.bookmark-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const form = this.closest('form');
            const url = form.action;
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                if (data.is_bookmarked !== undefined) {
                    // Обновляем состояние кнопки
                    if (data.is_bookmarked) {
                        this.classList.add('active');
                        this.innerHTML = '⭐ Удалить из закладок';
                    } else {
                        this.classList.remove('active');
                        this.innerHTML = '⭐ Добавить в закладки';
                    }
                }
            })
            .catch(error => {
                console.error('Ошибка:', error);
                alert('Не удалось обновить закладку. Попробуйте позже.');
            });
        });
    });
    
    // Получение CSRF-токена
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});