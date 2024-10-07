function Simulation(config) {
    this.config = config
    this.game = new Game(config.game_config);
    this.ws = null;
    this.main();
};
Simulation.prototype.main = function(){
    this.init_websocket();
};
Simulation.prototype.init_websocket = function(){
    this.ws = new WebSocket(this.config.server_url);
    this.ws.onopen = this.ws_onopen.bind(this);
    this.ws.onmessage = this.ws_onmessage.bind(this);
}
Simulation.prototype.ws_onopen = function(event) {
    this.add_log('> connected');
};

Simulation.prototype.ws_onmessage = function(event) {
    var data = JSON.parse(event.data);
    this.add_log('> '+data.type);
    switch(data['type']) {
        case 'update':
    		this.add_log(data['state']);
    		this.game.set_state(data['state']);
            break;
    }
};
Simulation.prototype.add_log = function(msg) {
    //console.log(msg);
};




