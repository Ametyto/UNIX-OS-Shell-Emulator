const input = document.getElementById('cmd-input');
const output = document.getElementById('output');

document.addEventListener('click', () => input.focus());

window.addEventListener('DOMContentLoaded', async () => {
    const user = await eel.get_user()();
    document.title = "Эмулятор — [" + user + "]";
    document.getElementById('prompt').textContent = user+":~$ ";
});

document.addEventListener('contextmenu', event => event.preventDefault());

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

input.addEventListener('keydown', async (event) => {
    if (event.key === 'Enter') {
        const cmd = input.value.trim();
        const user = await eel.get_user()();
        input.value = '';
        console.log(cmd);

        if (!cmd) return;

        appendLine(`${user}:~$ ${cmd}`, 'user');

        const response = await eel.process_command(cmd)();

        if (response === '__EXIT__') {
            window.close();
        } else if (response) {
            appendLine(response, 'response');
        }

        output.scrollTop = output.scrollHeight;
    }
});

function appendLine(text, className = '') {
    const div = document.createElement('div');
    div.className = `line ${className}`;
    div.textContent = text;
    output.appendChild(div);
}