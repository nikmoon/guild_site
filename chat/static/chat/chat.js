/*
 * chat.js
 * Copyright (C) 2017 nikbird <nikbird@server>
 *
 * Distributed under terms of the MIT license.
 */


document.addEventListener("DOMContentLoaded", function(event) {
    "user strict"

    var messageURLPost = document.getElementById('msg_url_post').value;
    var messageURLGet = document.getElementById('msg_url_get').value;
    var postMsgButton = document.getElementById('post_message');
    var msgTextArea = document.getElementById('message_text');
    var divMessages = document.getElementById('messages');
    var lastID = document.getElementById('last_id').value;


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
            //console.log('status: ' + this.status);
            //console.log('state: ' + this.readyState);
        }
        xhr.open('POST', messageURLPost, true);
        xhr.send(msgTextArea.value);
        msgTextArea.value = "";
    })


    function get_new_message() {
        var xhr = new XMLHttpRequest();
        
        xhr.onreadystatechange = function() {
            //console.log('status: ' + this.status);
            //console.log('state: ' + this.readyState);
        }


        //var data = JSON.stringify({ 'lastID': lastID });
        //alert(data);
        var endURL = messageURLGet + '?lastid=' + lastID;
        alert(endURL);
        xhr.open('GET', messageURLGet + '?lastid=' + lastID, true);
        xhr.send();

    }

    get_new_message();
});


