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
            if (typeof date === "string") {
                date = moment(date);
            } else {
                date = date.clone();
            }
            date.tz(this.force_timezone);
            return (date.clone().tz("UTC", true) - date) / 60000;
            // utcOffset() gives wrong result:
            // let tz = moment.tz.zone(this.force_timezone);
            // return -tz.utcOffset(date.unix());
        },
    });
});
