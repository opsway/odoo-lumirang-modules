from . import controllers, models, lib

from logging import getLogger

import odoo

_logger = getLogger(__name__)


def should_ignore(exc, value, tb):
    from werkzeug.exceptions import HTTPException

    # Werkzeug HTTPException can be raised internally by Odoo or in
    # user code if they mix Odoo with Werkzeug. Filter based on the
    # HTTP status code.

    if isinstance(value, HTTPException) and newrelic.agent.ignore_status_code(value.code):
        return True


def _nr_wrapper_handle_exception_(wrapped):
    def _handle_exception(*args, **kwargs):
        transaction = newrelic.agent.current_transaction()

        if transaction is None:
            return wrapped(*args, **kwargs)

        transaction.record_exception(ignore_errors=should_ignore)

        name = newrelic.agent.callable_name(args[1])
        with newrelic.agent.FunctionTrace(transaction, name):
            return wrapped(*args, **kwargs)

    return _handle_exception


def _instrument():
    target = odoo.service.server.server

    if getattr(target, '_nr_instrumented', False):
        _logger.info("NewRelic instrumented already")
        return

    # Main WSGI Application
    target._nr_instrumented = True
    target.app = newrelic.agent.WSGIApplicationWrapper(target.app)

    # Workers new WSGI Application
    target = odoo.service.wsgi_server
    target.application_unproxied = newrelic.agent.WSGIApplicationWrapper(target.application_unproxied)

    # Error handling
    target = odoo.http.WebRequest
    target._handle_exception = _nr_wrapper_handle_exception_(target._handle_exception)


try:
    import newrelic.agent

    _instrument()
except ImportError:
    _logger.warn("Newrelic python module not installed")
