// Плавная прокрутка к началу страницы при смене пагинации
document.addEventListener('DOMContentLoaded', function() {
    // Функция для навешивания обработчиков на пагинационные ссылки
    function attachPaginationLinks() {
        // Находим все ссылки пагинации
        const paginationLinks = document.querySelectorAll('.pagination a.page-link');

        paginationLinks.forEach(function(link) {
            link.addEventListener('click', function(event) {
                // Предотвращаем стандартное поведение ссылки
                event.preventDefault();
                const url = this.getAttribute('href');
                if (url !== '#') {
                    // Обновляем URL без перезагрузки страницы
                    window.history.pushState(null, '', url);
                    // Выполняем AJAX-запрос для получения новой страницы
                    fetch(url, {
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                    })
                    .then(response => response.text())
                    .then(data => {
                        // Парсим полученные данные и заменяем содержимое <main>
                        const parser = new DOMParser();
                        const doc = parser.parseFromString(data, 'text/html');
                        const newMain = doc.querySelector('main').innerHTML;
                        // Обновляем содержимое главного контейнера
                        document.querySelector('main').innerHTML = newMain;

                        // Плавная прокрутка вверх страницы
                        window.scrollTo({
                            top: 0,
                            behavior: 'smooth'
                        });

                        // Повторно навешиваем обработчики на новые пагинационные ссылки
                        attachPaginationLinks();
                    })
                    .catch(error => console.error('Ошибка при загрузке страницы:', error));
                }
            });
        });
    }

    // Инициализируем обработчики при первой загрузке страницы
    attachPaginationLinks();
});