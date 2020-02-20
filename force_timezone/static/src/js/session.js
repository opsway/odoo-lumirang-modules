odoo.define("force_timezone.session", function (require) {
    "use strict";

    let Session = require("web.Session");

    return Session.include({
        /**
         * Returns the time zone difference (in minutes) from the current locale
         * (host system settings) to UTC, for a given date. The offset is positive
         * if the local timezone is behind UTC, and negative if it is ahead.
         *
         * @param {string | moment} date a valid string date or moment instance
         * @returns {integer}
         */
        getTZOffset(date) {
            return this.force_timezone_minutes;
        },
    });
});
