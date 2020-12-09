//function that display value
function dis(val) {
    document.getElementById('id_expression').value += val
}

//function that clear the display
function clr() {
    document.getElementById('id_expression').value = ''
}

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + 'roomName'
    + '/'
);

chatSocket.onmessage = function (e) {
    console.log(e)
    const data = JSON.parse(e.data);
    const data2 = JSON.parse(data.data);

    console.log(data2)
    if (data2) {
        $("#table > tbody").html("");
        var len = data2.length;
        var txt = "";
        if (len > 0) {
            for (var i = 0; i < len; i++) {
                var log = data2[i].fields;
                console.log(log);

                if (log.date && log.expression && log.user) {
                    txt += "<tr><td>" + log.date.substr(0,10) + "</td><td>" + log.user +"</td><td>" + log.expression + "</td></tr>";
                }
            }
            if (txt !== "") {
                $("#table").append(txt).removeClass("hidden");
            }
        }
    }
};

chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

document
    .getElementById('cal-form')
    .addEventListener('submit', function (event) {
        event.preventDefault();
        let expression = document.getElementById('id_expression').value;
        let result = eval(expression);
        let record = expression + ' = ' + result;
        document.getElementById("id_expression").value = result;

        chatSocket.send(JSON.stringify({
            'expression': record
        }));
    });