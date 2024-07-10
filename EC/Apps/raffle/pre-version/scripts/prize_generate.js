var startBtn = document.getElementById('startBtn');
var participantCountInput = document.getElementById('participantCount');
var angle = 0;
var rotationInterval;

// 存储奖品及其对应个数的对象
var prizesDict = {
    '卡套00': 8,
    '卡套01': 8,
    '卡套02': 8,
    '卡套03': 8,
    '卡套04': 8,
    '卡套05': 8,
    '卡套06': 8,
    '小说？': 3,
    '卡套07': 8,
    '卡套08': 8,
    '卡套09': 8,

    '钥匙扣00': 8,
    '钥匙扣01': 8,
    '钥匙扣02': 8,
    '钥匙扣03': 8,
    '钥匙扣04': 8,
    '钥匙扣05': 8,
    '钥匙扣06': 8,
    '钥匙扣07': 8,
    '钥匙扣08': 8,
    '钥匙扣09': 8,

    '决策币00': 8,
    '决策币01': 8,
    '决策币02': 8,
    '决策币03': 8,  
    '决策币04': 8,
    '决策币05': 8,
    '决策币06': 8,
    '决策币07': 8,
    '决策币08': 8,
    '决策币09': 8,
};


// 从奖品名称中去除数字部分
function removeDigits(name) {
    return name.replace(/\d/g, '');
}

// 计算总奖品数量
var totalPrizeCount = Object.values(prizesDict).reduce((acc, val) => acc + val, 0);


function raffle(){
    // var participantCount = parseInt(participantCountInput.value);
    var participantCount = 1;

    if (isNaN(participantCount) || participantCount < 1) {
        alert('Please enter a valid participant count.');
        return;
    }

    clearInterval(rotationInterval); // 清除之前的旋转定时器

    rotationInterval = setInterval(function() {
        startBtn.style.transform = "rotate(" + angle + "deg)";
        angle += 1;
        if (angle >= 360) {
            angle = 0;
        }
    }, 10);

    // 停止旋转执行抽奖逻辑
    setTimeout(function() {
        clearInterval(rotationInterval); // 停止旋转

        // 根据参与者数量进行抽奖
        var selectedPrizes = [];
        for (var i = 0; i < participantCount; i++) {
            var randomNumber = Math.random() * totalPrizeCount;
            var cumulativeCount = 0;
            var selectedPrize = null;
            for (var prize in prizesDict) {
                cumulativeCount += prizesDict[prize];
                if (randomNumber <= cumulativeCount) {
                    selectedPrize = removeDigits(prize);
                    break;
                }
            }
            selectedPrizes.push(selectedPrize);
            // 更新选中奖品的数量
            if (selectedPrize) {
                prizesDict[selectedPrize]--;
                totalPrizeCount--;
            }
        }

        console.log('Current state:', prizesDict); // 输出抽奖后的奖品字典状态

        if (selectedPrizes.length > 0) {
            var resultText = 'Congratulations! You won: ' + selectedPrizes.join(', ');
            document.getElementById('result').innerText = resultText;
        } else {
            document.getElementById('result').innerText = 'The raffle has ended. All prizes have been awarded!';
        }

        // 显示文本框，等待用户输入新的参与者数量
        participantCountInput.style.display = 'block';
        participantCountInput.value = '';
    }, 2000); // 旋转2秒后停止并执行抽奖逻辑
};
startBtn.addEventListener('click', raffle); 
document.addEventListener('keydown', function(event) {
    // 如果按下的是空格键，则执行抽奖
    if (event.key === ' ') {
        raffle();
    }
});

