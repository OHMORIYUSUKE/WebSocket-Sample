var ws = new WebSocket("ws://localhost:8000/ws");

//マウスストーカー用のdivを取得
const stalker = document.getElementById('stalker'); 

ws.onmessage = function(event) {
let loc = event.data.split(':');
stalker.style.transform = 'translate(' + loc[0] + 'px, ' + loc[1] + 'px)';
};

//上記のdivタグをマウスに追従させる処理
document.addEventListener('mousemove', function (e) {
    stalker.style.transform = 'translate(' + e.clientX + 'px, ' + e.clientY + 'px)';
    ws.send(e.clientX + ":" + e.clientY);
    document.getElementById("location").value = e.clientX + ":" + e.clientY;
});