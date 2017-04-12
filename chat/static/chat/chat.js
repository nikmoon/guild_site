/*
 * chat.js
 * Copyright (C) 2017 nikbird <nikbird@server>
 *
 * Distributed under terms of the MIT license.
 */


document.addEventListener("DOMContentLoaded", function(event) {
    "user strict"

    var urlGetMsg = document.getElementById('urlGetMsg').value;
    var urlPostMsg = document.getElementById('urlPostMsg').value;
    var postMsgButton = document.getElementById('postMessage');
    var msgTextArea = document.getElementById('messageText');
    var divMessages = document.getElementById('messages');
    var lastID;


    // прокрутка списка сообщений вверх
    divMessages.scrollTop = divMessages.scrollHeight;

    // очищаем поле для ввода сообщения при обновлении страницы
    msgTextArea.value = "";


    //
    //  отправка сообщения на сервер при нажатии на кнопку отправки
    //
    postMsgButton.addEventListener('click', function(event) {
        event.preventDefault();

        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
        }
        xhr.open('POST', urlPostMsg, true);
        xhr.send(msgTextArea.value);
        msgTextArea.value = "";
    })


    //
    //  Добавление стилизованного сообщения в окно сообщений чата
    //
    function add_chat_messages(messages) {
        messages.forEach(function(msg, i, arr) {
            var divMain = document.createElement('div');
            var p = document.createElement('p');
            var text = document.createTextNode("[" + msg.created + "] " + msg.author + " говорит:");
            p.innerHTML = '<span style="background-color: lightgray;">' + msg.text + "</span>";
            p.style.marginLeft = '20px';
            divMain.appendChild(text);
            divMain.appendChild(p);
            divMessages.appendChild(divMain);
        });
        divMessages.scrollTop = divMessages.scrollHeight;
        lastID = messages[messages.length - 1].id;
    }

    //
    //  Получаем с сервера последние 20 сообщений и показываем
    //
    function show_last_messages() {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (this.readyState == xhr.DONE && this.status == 200) {
                var messages = JSON.parse(this.responseText)['messages'];
                add_chat_messages(messages);
                get_new_message();
            }
        }
        xhr.open('GET', urlGetMsg, true);
        xhr.send();
    }

    //
    //  Ждем новые сообщения
    //
    function get_new_message() {
        var xhr = new XMLHttpRequest();
        
        xhr.onreadystatechange = function() {
            var timeOut = 20;
            if (this.readyState != xhr.DONE)
                return;

            if (this.status == 200) {
                var messages = JSON.parse(this.responseText)['messages'];
                add_chat_messages(messages);
            }
            else if (this.status != 504){       // 504 - Gateway time-out
                timeOut = 5000;
            }
            setTimeout(get_new_message, timeOut);
        }
        xhr.open('GET', urlGetMsg + '?lastid=' + lastID, true);
        xhr.send();
    }
    show_last_messages();
});


