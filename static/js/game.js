let score = 0;
let attempts = 0;
let currentItem = null;

async function getNewItem() {
    const response = await fetch('/get-item');
    const item = await response.json();
    return item;
}

async function displayNewItem() {
    const item = await getNewItem();
    if (item.name === null) {
        endGame();
        return;
    }
    
    currentItem = item;
    document.getElementById('currentItem').textContent = item.name;
}

function updateScore() {
    document.getElementById('score').textContent = score;
}

function showMessage(msg) {
    document.getElementById('message').textContent = msg;
}

function endGame() {
    const message = score >= 10 
        ? "당신은 분리수거 고수!😎 앞으로도 환경을 위해 열심히 분리수거 해주세요😊"
        : "당신은 분리수거 허수ㅡㅡ 올바른 분리수거 방법을 배워보세요😎";
    showMessage(message);
    
    document.querySelectorAll('.bin').forEach(bin => {
        bin.style.pointerEvents = 'none';
    });
}

document.querySelectorAll('.bin').forEach(bin => {
    bin.addEventListener('click', async () => {
        if (!currentItem) return;
        
        attempts++;
        const selectedType = bin.dataset.type;
        
        if (selectedType === currentItem.type) {
            score++;
            updateScore();
            showMessage(`정확히 분리수거되었습니다! '${currentItem.name}'가 ${currentItem.type}로 분리되었습니다.`);
        } else {
            showMessage(`잘못된 분리수거! '${currentItem.name}'는 ${currentItem.type}입니다.`);
        }
        
        if (attempts >= 15) {
            endGame();
        } else {
            await displayNewItem();
        }
    });
});

// 게임 시작
displayNewItem(); 