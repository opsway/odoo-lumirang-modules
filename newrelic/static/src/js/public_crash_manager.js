odoo.define('newrelic.PublicCrashManager', function (require) {
    "use strict";

    const {CrashManager} = require('web.PublicCrashManager');
    const {CrashManagerExtension} = require('newrelic.CrashManager');
    const CrashManagerWithReport = CrashManager.extend(CrashManagerExtension);
    const core = require('web.core');

    core.serviceRegistry.add('crash_manager', CrashManagerWithReport);

    return {
        CrashManager: CrashManagerWithReport,
    };
});
