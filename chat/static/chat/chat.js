/*
 * chat.js
 * Copyright (C) 2017 nikbird <nikbird@server>
 *
 * Distributed under terms of the MIT license.
 */


document.addEventListener("DOMContentLoaded", function(event) {
    "user strict"

    var messageURL = document.getElementById('msgURL').value;
    var postMsgButton = document.getElementById('postMessage');
    var msgTextArea = document.getElementById('messageText');
    var divMessages = document.getElementById('messages');
    var lastID = document.getElementById('lastID').value;


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
        xhr.open('POST', messageURL, true);
        xhr.send(msgTextArea.value);
        msgTextArea.value = "";
    })


    //
    //  Добавление стилизованного сообщения в окно сообщений чата
    //
    function add_chat_message(msg, i, arr) {
        var divMain = document.createElement('div');
        var p = document.createElement('p');
        var text = document.createTextNode("[" + msg.created + "] " + msg.author + " говорит:");
        p.innerHTML = '<span style="background-color: lightgray;">' + msg.text + "</span>";
        p.style.marginLeft = '20px';
        divMain.appendChild(text);
        divMain.appendChild(p);
        divMessages.appendChild(divMain);
    }

    //
    //  Получаем с сервера последние 20 сообщений и показываем
    //
    function show_last_messages() {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (this.readyState == xhr.DONE && this.status == 200) {
                var messages = JSON.parse(this.responseText)['messages'];
                messages.forEach(add_chat_message);
                divMessages.scrollTop = divMessages.scrollHeight;
            }
        }
        xhr.open('GET', messageURL + '?count=20', true);
        xhr.send();
    }


    function get_new_message() {
        var xhr = new XMLHttpRequest();
        
        xhr.onreadystatechange = function() {
            var messages;
            var p;
            if (this.readyState != xhr.DONE)
                return;

            if (this.status == 200) {
                var data = JSON.parse(this.responseText);
                messages = data['messages'];
                messages.forEach(
                    //function(item, i, arr) {
                    add_chat_message);
                    //p = document.createElement('p');
                    //p.innerHTML = item.created + ' ' + item.author + ': ' + item.text;
                    //divMessages.appendChild(p);
                //});
                divMessages.scrollTop = divMessages.scrollHeight;
                lastID = messages[messages.length - 1].id;
                setTimeout(get_new_message, 10);
            }
            else if (this.status == 504) {
                setTimeout(get_new_message, 10)
            }
            else {
                setTimeout(get_new_message, 5000);
            }
        }

        var endURL = messageURL + '?lastid=' + lastID;
        xhr.open('GET', messageURL + '?lastid=' + lastID, true);
        xhr.send();

    }

    show_last_messages();
    get_new_message();
});


