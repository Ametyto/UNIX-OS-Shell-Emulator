const input = document.getElementById('cmd-input');
const output = document.getElementById('output');


/**
 * Установка фокуса на поле ввода при клике в любой точке окна.
 */
document.addEventListener('click', () => input.focus());

/**
 * Заголовок приложения и юзер для строки ввода
 */
window.addEventListener('DOMContentLoaded', async () => {
    const user = await eel.get_user()();
    document.title = "Эмулятор — [" + user + "]";
    document.getElementById('prompt').textContent = user+":~$ ";
});

/**
 * Блокировка ПКМ.
 */
document.addEventListener('contextmenu', event => event.preventDefault());

/**
 * Блокировка F12, Ctrl+Shift+I, Ctrl+R, F5.
 */
document.addEventListener('keydown', function (event) {
    const key = event.key.toLowerCase();
    const isCtrlShift = event.ctrlKey && event.shiftKey;

    const isDev = 
    (isCtrlShift && (key === 'i' || key === 'j')) || key === 'f12';
    const isReload = key === 'f5' || (event.ctrlKey && key === 'r');

    if (isDev || isReload) {
    event.preventDefault();
    }
});

/**
 * Обработка ввода команд по нажатию клавиши Enter.
 */
input.addEventListener('keydown', async (event) => {
    if (event.key === 'Enter') {
        const cmd = input.value.trim();
        const user = await eel.get_user()();
        input.value = '';
        console.log(cmd);

        if (!cmd) return;

        // Повторение введенной команды в консоль
        appendLine(`${user}:~$ ${cmd}`, 'user');

        // Вызов функции из питона
        const response = await eel.process_command(cmd)();

        if (response === '__EXIT__') {
            window.close();
        } else if (response) {
            appendLine(response, 'response');
        }

        // Автоскролл вниз
        output.scrollTop = output.scrollHeight;
    }
});

function appendLine(text, className = '') {
    const div = document.createElement('div');
    div.className = `line ${className}`;
    div.textContent = text;
    output.appendChild(div);
}