# -*- encoding: UTF-8 -*-
from . import controllers, models
import os

from logging import getLogger

_logger = getLogger(__name__)

try:
    import odoo

    target = odoo.service.server.server

    try:
        instrumented = target._nr_instrumented
    except AttributeError:
        instrumented = target._nr_instrumented = False

    if instrumented:
        _logger.info("NewRelic instrumented already")
    else:
        import odoo.tools.config as config
        import newrelic.agent

        env_value = os.environ.get('ODOO_STAGE', "dev")
        _logger.info("NewRelic environment is {}".format(env_value))
        try:
            dirname = os.path.dirname(__file__)
            newrelic.agent.initialize(os.path.join(dirname, 'newrelic.ini'), env_value)
        except KeyError:
            try:
                newrelic.agent.initialize(config['new_relic_config_file'], env_value)
            except KeyError:
                _logger.info('NewRelic setting up from env variables')
                newrelic.agent.initialize(environment=env_value)

        # Main WSGI Application
        target._nr_instrumented = True
        target.app = newrelic.agent.WSGIApplicationWrapper(target.app)

        # Workers new WSGI Application
        target = odoo.service.wsgi_server
        target.application_unproxied = newrelic.agent.WSGIApplicationWrapper(target.application_unproxied)


        # Error handling
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


        target = odoo.http.WebRequest
        target._handle_exception = _nr_wrapper_handle_exception_(target._handle_exception)
except ImportError:
    _logger.warn('newrelic python module not installed or other missing module')
