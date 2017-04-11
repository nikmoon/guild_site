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
                messages.forEach(function(item, i, arr) {
                    p = document.createElement('p');
                    p.innerHTML = item.created + ' ' + item.author + ': ' + item.text;
                    divMessages.appendChild(p);
                });
                divMessages.scrollTop = divMessages.scrollHeight;
                lastID = messages[messages.length - 1].id;
            }
            get_new_message();
        }

        var endURL = messageURL + '?lastid=' + lastID;
        xhr.open('GET', messageURL + '?lastid=' + lastID, true);
        xhr.send();

    }

    get_new_message();
});


