// Получение CSRF токена из DOM
const getCsrfToken = () => document.querySelector('[name=csrfmiddlewaretoken]').value;

// Конфигурация редактора
const editorConfig = {
    spellChecker: false,
    autosave: {
        enabled: true,
        delay: 1000,
        uniqueId: 'post_editor'
    },
    toolbar: [
        'bold', 'italic', 'heading', '|',
        'quote', 'code', 'unordered-list', 'ordered-list', '|',
        'link', 'image', '|',
        'preview', 'side-by-side', 'fullscreen'
    ]
};

// Асинхронный запрос предпросмотра
async function fetchPreview(text) {
    try {
        // Отправка текста на сервер для преобразования в HTML
        const response = await fetch('/blog/preview/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({text})
        });
        const data = await response.json();
        return data.html;
    } catch (error) {
        console.error('Ошибка предпросмотра:', error);
        // Возврат сообщения об ошибке в случае неудачи
        return "<p class='text-danger'>Ошибка при загрузке предпросмотра</p>";
    }
}

// Создание и отображение toast-уведомления
function showToast(message, type = 'success') {
    // Создание элемента уведомления
    const toastElement = document.createElement('div');
    toastElement.className = `toast align-items-center text-white bg-${type} border-0`;
    toastElement.setAttribute('role', 'alert');
    toastElement.setAttribute('aria-live', 'assertive');
    toastElement.setAttribute('aria-atomic', 'true');

    // Формирование HTML-структуры уведомления
    toastElement.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;

    // Добавление уведомления в контейнер и его отображение
    document.querySelector('.toast-container').appendChild(toastElement);
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
}

// Асинхронная отправка формы
async function submitForm(form) {
    try {
        // Отправка данных формы на сервер
        const response = await fetch(form.action, {
            method: 'POST',
            body: new FormData(form),
            headers: {
                'X-CSRFToken': getCsrfToken()
            }
        });

        if (!response.ok) throw new Error('Ошибка сети');

        const data = await response.json();

        // Обработка успешного ответа
        if (data.success) {
            showToast(data.message);
            // Перенаправление на указанный URL после успешного сохранения через 2 секунды
            if (data.redirect_url) {
                setTimeout(() => window.location.href = data.redirect_url, 2000);
            }
        }
    } catch (error) {
        showToast('Произошла ошибка при сохранении поста', 'danger');
        console.error('Ошибка отправки формы:', error);
    }
}

// Инициализация редактора
function initializeEditor(textArea) {
    return new EasyMDE({
        ...editorConfig,
        element: textArea,
        // Настройка функции предпросмотра с асинхронной загрузкой
        previewRender: async (plainText, preview) => {
            preview.innerHTML = 'Загрузка предпросмотра...';
            const html = await fetchPreview(plainText);
            preview.innerHTML = html;
            // Подсветка синтаксиса в предпросмотре
            hljs.highlightAll();
            return preview.innerHTML;
        }
    });
}

// Основная функция инициализации
document.addEventListener('DOMContentLoaded', function() {
    // Получение текстового поля редактора
    const textArea = document.getElementById('id_text');
    if (!textArea) return;

    const editor = initializeEditor(textArea);

    // Настройка обработчика отправки формы
    const form = document.getElementById('post-form');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            // Обновление значения текстового поля перед отправкой
            textArea.value = editor.value();
            await submitForm(form);
        });
    }
});