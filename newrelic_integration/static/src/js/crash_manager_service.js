odoo.define('newrelic.CrashManagerService', function (require) {
    "use strict";

    const {CrashManager} = require('newrelic.CrashManager');
    const core = require('web.core');

    core.serviceRegistry.add('crash_manager', CrashManager);
});
