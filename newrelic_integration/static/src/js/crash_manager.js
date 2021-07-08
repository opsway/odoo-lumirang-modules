odoo.define('newrelic.CrashManager', function (require) {
    "use strict";

    const core = require('web.core');
    const {CrashManager} = require('web.CrashManager');
    const _t = core._t;
    
    const CrashManagerExtension = {
        init() {
            let oldError = window.onerror;
            let self = this;
            this._super.apply(this, arguments);
            window.onerror = function (message, file, line, col, error) {
                if (!file && !line && !col) {
                    if (window.onOriginError) {
                        window.onOriginError();
                        delete window.onOriginError;
                    } else {
                        self.show_error({
                            type: _t("Odoo Client Error"),
                            message: _t("Unknown CORS error"),
                            data: {
                                debug: _t("An unknown CORS error occurred. The error probably originates from a " +
                                    "JavaScript file served from a different origin. (Opening your browser console " +
                                    "might give you a hint on the error.)")
                            },
                            skipNewrelic: true,
                        });
                    }
                } else {
                    if (!error && message === 'ResizeObserver loop limit exceeded') {
                        return;
                    }
                    let traceback = error ? error.stack : '';
                    self.show_error({
                        type: _t("Odoo Client Error"),
                        message: message,
                        data: {debug: file + ':' + line + "\n" + _t('Traceback:') + "\n" + traceback},
                        skipNewrelic: true,
                    });
                }
                oldError.apply(null, arguments);
            };
        },
        show_error(error) {
            if (window.newrelic && !error.skipNewrelic) {
                newrelic.noticeError(new Error(JSON.stringify(error)));
            }
            return this._super.apply(this, arguments);
        },
    };
    const CrashManagerWithReport = CrashManager.extend(CrashManagerExtension);

    return {
        CrashManager: CrashManagerWithReport,
        CrashManagerExtension,
    };
});
