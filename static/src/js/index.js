odoo.define('linhafala_odoo.call_popup', function (require) {
    "use strict";

    const socket = io('http://localhost:3001');
    let isDisplayed = false;
    let dialogInstance = null;

    socket.addEventListener('message', message => {
        const events = message;

        if ((events.Event === 'Varset' || events.ChannelStateDesc === 'Ring') && !isDisplayed) {
            display();
            isDisplayed = true;

            if (events.Event === 'Hangup'){
                dialogInstance.close()
            }
        }
    });

    const display = () => {
        var Dialog = require('web.Dialog');
        const title = "Recebendo chamada...";
        const time = "12:30 PM";
        const phoneNumber = "+1 123-456-7890";
        const numberId = "12345";

        try {
            dialogInstance = Dialog.confirm(
            this,
                 `Time: ${time}\nPhone Number: ${phoneNumber}\nNumber ID: ${numberId}`,
            {
                title: title,

                onForceClose: function () {
                    console.log("Click Close");
                },
                confirm_callback: function () {
                    console.log("Click Confirm");
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
