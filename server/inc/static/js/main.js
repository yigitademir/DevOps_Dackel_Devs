function App(config) {
    this.config = config
    this.ws = null;
    this.client_id = null;
    this.username = null;
};
App.prototype.main = function(){
    this.init_websocket();
};
App.prototype.init_websocket = function(){
    this.ws = new WebSocket(this.config.wss);
    this.ws.onopen = this.ws_onopen.bind(this);
    this.ws.onmessage = this.ws_onmessage.bind(this);
}
App.prototype.ws_onopen = function(event) {
    console.log('> connected');
    this.add_log('> connected');
};
App.prototype.ws_send = function(data) {
    this.add_log('< '+data['type']);
    console.log('< '+JSON.stringify(data));
    this.ws.send(JSON.stringify(data))
};
App.prototype.ws_onmessage = function(event) {
    console.log('>', event.data);
    data = JSON.parse(event.data);
    this.add_log('> '+data['type']);
    switch(data['type']) {
        case 'authenticated':
            this.authenticated(data);
            break;
        case 're_authenticated':
            this.re_authenticated(data);
            break;
        case 'message':
            var messages = document.getElementById('messages');
            var message = document.createElement('li');
            var content = document.createTextNode(data['sender']+': '+data['message']);
            message.appendChild(content);
            messages.appendChild(message);  
            break;
    }
};
App.prototype.add_log = function(msg) {
    $('#logs').append($('<p>'+msg+'</p>'));
};
App.prototype.send_message = function(event){
    event.preventDefault()
    var input = document.getElementById("messageText")
    data = {
        'type': 'message',
        'message': input.value,
    }
    input.value = '';
    this.ws_send(data);
}
App.prototype.authenticated = function(data) {
    server_client_id = data.client_id;
    local_client_id = sessionStorage.getItem("client_id");
    if (local_client_id === null) {
        this.client_id = data.client_id;
        this.username = data.username;
        sessionStorage.setItem("client_id", this.client_id);
        $('.right').html(this.username);
    } else {
        data = {
            'type': 're_authenticate',
            'local_client_id': local_client_id,
        }
        this.ws_send(data);
    }
}
App.prototype.re_authenticated = function(data) {
    this.username = data.username;
    $('.right').html(this.username);
}

