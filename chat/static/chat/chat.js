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
    //  Создание стилизованного сообщения
    //
    function create_chat_message(msg) {
        var divMain = document.createElement('div');
        var p = document.createElement('p');
        var text = document.createTextNode("[" + msg.created + "] " + msg.author + " говорит:");
        p.innerHTML = '<span style="background-color: lightgray;">' + msg.text + "</span>";
        p.style.marginLeft = '20px';
        divMain.appendChild(text);
        divMain.appendChild(p);
        return divMain;
    }

    //
    //  Добавление стилизованного сообщения в окно сообщений чата
    //
    function add_chat_messages(messages) {
        if (messages.length == 0) {
            return;
        }
        var index = 0;
        var timerID = setInterval(function() {
            if (index >= messages.length) {
                clearInterval(timerID);
                get_new_messages();
            }
            else {
                chatMsg = create_chat_message(messages[index]);
                chatMsg.style.display = 'none';
                divMessages.appendChild(chatMsg);
                $(chatMsg).fadeIn(1200);
                divMessages.scrollTop = divMessages.scrollHeight;
                index += 1;
            }
        }, 20);
    }


    //
    //  Получаем с сервера последние 20 сообщений и показываем
    //
    function show_last_messages() {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (this.readyState == xhr.DONE) {
                if ( this.status != 200 ) {
                    setTimeout(show_last_messages, 5000);
                }
                else {
                    var messages = JSON.parse(this.responseText)['messages'];
                    lastID = messages[messages.length - 1].id;
                    add_chat_messages(messages);
                }
            }
        }
        xhr.open('GET', urlGetMsg, true);
        xhr.send();
    }


    //
    //  Ждем новые сообщения
    //
    function get_new_messages() {
        var xhr = new XMLHttpRequest();
        var minTimeout = 5000;
        var startReq, timeoutDelta;
        
        xhr.onreadystatechange = function() {
            if (this.readyState != xhr.DONE)
                return;

            if (this.status == 200) {
                var messages = JSON.parse(this.responseText)['messages'];
                lastID = messages[messages.length - 1].id;
                add_chat_messages(messages);
            }
            else {
                timeoutDelta = minTimeout - (Date.now() - startReq);
                if (timeoutDelta > 300) {
                    setTimeout(get_new_messages, timeoutDelta);
                }
                else {
                    get_new_messages();
                }
            }
        }

        xhr.open('GET', urlGetMsg + '?lastid=' + lastID, true);
        xhr.send();
        startReq = Date.now();
    }

    show_last_messages();
});


