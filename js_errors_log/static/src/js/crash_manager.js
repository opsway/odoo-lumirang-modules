odoo.define('js_errors_log.CrashManager', function (require) {
    "use strict";

    const {CrashManager} = require('web.CrashManager');
    let ajax = require('web.ajax');
    const oldShowError = CrashManager.prototype.show_error;
    CrashManager.prototype.show_error = function (error) {
        let result = oldShowError.apply(this, arguments);
        let name;
        if (error.data != null && error.data.name != null) {
            name = error.data.name;
        } else {
            name = "Unknown error";
        }
        try {
            ajax.jsonRpc("/js_error", 'call', {
                name,
                message: error.message,
                data: JSON.stringify(error.data),
                width: window.screen.width,
                height: window.screen.height,
                client_width: document.documentElement.clientWidth,
                client_height: document.documentElement.clientHeight,
                pixel_ratio: window.devicePixelRatio,
            });
        } catch (e) {
            console.error("Error reporting failed", e);
        }
        return result;
    };
});
