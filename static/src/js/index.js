odoo.define('linhafala_odoo.call_popup', function (require) {
    "use strict";

    const io = require('./socketio-socket.io/client-dist/socket.io.min.js');

    const socket = io();

    socket.connect('http://localhost:3001')

    socket.on('connection', (socket) => {
        console.log('Connectado ao servidor ');

        socket.on('disconnect', () => {
            console.log('Disconectado');
        })
    })


});
