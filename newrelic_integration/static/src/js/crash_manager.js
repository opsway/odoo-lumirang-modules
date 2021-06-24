odoo.define('newrelic.CrashManager', function (require) {
    "use strict";

    const core = require('web.core');
    const {CrashManager} = require('web.CrashManager');
    const _t = core._t;

    function isBrowserChrome() {
        return $.browser.chrome && navigator.userAgent.toLocaleLowerCase().indexOf('edge') === -1;
    }

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
            core.bus.on('crash_manager_unhandledrejection', this, function (ev) {
                if (ev.reason && ev.reason instanceof Error) {
                    let traceback;
                    if (isBrowserChrome()) {
                        traceback = ev.reason.stack;
                    } else {
                        traceback = `${_t("Error:")} ${ev.reason.message}\n${ev.reason.stack}`;
                    }
                    self.show_error({
                        type: _t("Odoo Client Error"),
                        message: '',
                        data: {debug: _t('Traceback:') + "\n" + traceback},
                        skipNewrelic: true,
                    });
                    if (window.newrelic) {
                        newrelic.noticeError(ev.reason);
                    }
                } else {
                    // the rejection is not due to an Error, so prevent the browser
                    // from displaying an 'unhandledrejection' error in the console
                    ev.stopPropagation();
                    ev.stopImmediatePropagation();
                    ev.preventDefault();
                }
            });
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
