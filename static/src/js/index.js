odoo.define('linhafala_odoo.call_popup', function (require) {
    "use strict";

    const socket = io('http://localhost:3001');
    let isDisplayed = false;
    let dialogInstance = null;

    socket.addEventListener('message', message => {
        const events = message;

        if ((events.Event === 'Varset' || events.ChannelStateDesc === 'Ring') && !isDisplayed) {
            display( events.$time, events.CallerIDNum, events.ConnectedLineNum);
            isDisplayed = true;

            if (events.Event === 'Hangup'){
                dialogInstance.close()
            }
        }
    });

    const display = (time, callerIDNum, connectedLineNum) => {
        var Dialog = require('web.Dialog');
        const title = "Recebendo chamada...";

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
                    window.location.href = '/web#cids=1&menu_id=110&action=155&model=linhafala.chamada&view_type=form';
                },
                cancel_callback: function () {
                    console.log("Click Cancel");
                }
            }
        );
        } catch (error) {
            console.error("An error occurred:", error);
        }
    }
});
