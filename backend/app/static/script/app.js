var ws = new WebSocket("ws://localhost:8000/ws");

const stalkerMe = document.getElementById('stalkerMe'); 
const stalkerEnemy = document.getElementById('stalkerEnemy'); 

// init
document.getElementById("locationMeX").value = "0";
document.getElementById("locationMeY").value = "0";
document.getElementById("locationEnemyX").value = "0";
document.getElementById("locationEnemyY").value = "0";

// 相手(自分以外)
ws.onmessage = function(event) {
    let loc = event.data.split(':');
    // 自分のポインターのみ移動
    if(loc[2] != document.getElementById("playerId").value){
        document.getElementById("locationEnemyX").value = loc[0];
        document.getElementById("locationEnemyY").value = loc[1];
        stalkerEnemy.style.transform = 'translate(' + loc[0] + 'px, ' + loc[1] + 'px)';
    }
};

// 自分
document.getElementById("field").addEventListener('mousemove', function (e) {
    stalkerMe.style.transform = 'translate(' + e.offsetX + 'px, ' + e.offsetY + 'px)';
    ws.send(e.offsetX + ":" + e.offsetY + ":" + document.getElementById("playerId").value);
    document.getElementById("locationMeX").value = e.offsetX;
    document.getElementById("locationMeY").value = e.offsetY;
});