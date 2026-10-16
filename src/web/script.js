const input = document.getElementById('cmd-input');
const output = document.getElementById('output');

document.addEventListener('click', () => input.focus());

window.addEventListener('DOMContentLoaded', async () => {
    const user = await eel.get_user()();
    document.title = "Эмулятор — [" + user + "]";
    document.getElementById('prompt').textContent = user+":~$ ";
    console.log("start_script");
    start_script(user);
});

async function start_script(user){
    const printResult = await eel.run_start_script()();
    if (printResult.length < 2){
        return;
    }
    for (let i = 0; i < printResult.length; i+=2){
        const cmd = printResult[i];
        const response = printResult[i+1];
        console.log(i);
        appendLine(`${user}:~$ ${cmd}`, 'user');
        if (response === '__EXIT__') {
            window.close();
        } else if (response) {
            appendLine(response, 'response');
        }

        output.scrollTop = output.scrollHeight;
    }
}

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