const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const scaling = 10;

let conversions = {
    'Digit0': 0,
    'Digit1': 1,
    'Digit2': 2,
    'Digit3': 3,
    'Digit4': 4,
    'Digit5': 5,
    'Digit6': 6,
    'Digit7': 7,
    'Digit8': 8,
    'Digit9': 9,
    'KeyA': 10,
    'KeyB': 11,
    'KeyC': 12,
    'KeyD': 13,
    'KeyE': 14,
    'KeyF': 15,
}
let pressed = [];

document.addEventListener('DOMContentLoaded', (event) => {
    eel.get_status()(function (status) {
        document.getElementById('status').innerHTML = status;
    })
})

document.addEventListener('keydown', (event) => {
    let code = conversions[event.code];
    if (code) {
        if (!pressed.includes(code)) {
            pressed.push(code);
        }
    }
    console.log(pressed);
})

document.addEventListener('keyup', (event) => {
    let code = conversions[event.code];
    if (code) {
        index = pressed.indexOf(code);
        if (index >= 0) {
            pressed.splice(index, 1);
        }
    }
    console.log(pressed);
})

function render() {
    eel.update_status(pressed)((display) => {
        for (let y = 0; y < display.length; y++) {
            const row = display[y]
            for (let x = 0; x < row.length; x++) {
                const value = row[x];
                if (value == 1) {
                    ctx.fillStyle = 'black'
                } else {
                    ctx.fillStyle = 'white'
                }
                ctx.fillRect(x * scaling, y * scaling, scaling, scaling);
            }
        }
    })
    requestAnimationFrame(render)
}

function start() {
    requestAnimationFrame(render)
}