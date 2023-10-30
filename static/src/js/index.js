odoo.define('linhafala_odoo.call_popup', function (require) {
    "use strict";

    const socket = io('http://localhost:3001');
    let isDisplayed = false;
    let dialogInstance = null;
    let extensionAnswered = false;

    socket.addEventListener('message', message => {
        const events = message;

        if (!extensionAnswered) {
            if (events.Event === 'Varset' || events.ChannelStateDesc === 'Ring') {
                display();
                isDisplayed = true;
            }
    
            if (events.Event === 'Hangup') {
                dialogInstance.close();
            }
    
            if (events.Event === 'Bridge' && events.BridgeState === 'Link') {
                extensionAnswered = true;
            }
        }
    });

    var Dialog = require('web.Dialog');
    const title = "Recebendo chamada...";
    const connectedLineNum = "000";
    const callerIDNum ="123";
    const time = "2013-";

    setTimeout(() => {
        try {
            dialogInstance = Dialog.confirm(
            this,
                `Time: ${time}\nCaller: ${callerIDNum}\nConnected: ${connectedLineNum}`,
            {
                title: title,

                onForceClose: function () {
                    console.log("Click Close");
                },
                confirm_callback: function () {
                    const connectedLineNumParam = encodeURIComponent(connectedLineNum);
                    const url = `/web#cids=1&menu_id=110&action=155&model=linhafala.chamada&view_type=form&contact=${connectedLineNumParam}`;
                
                    window.location.href = url;

                    $(".some_class").text(this.connectedLineNumParam);
                },
                           
                cancel_callback: function () {
                    console.log("Click Cancel");
                },
                
            }
        );
        } catch (error) {
            console.error("An error occurred:", error);
        }
    }, 5000);

});
