from traceback import format_exc

import os
from logging import getLogger

import tempfile

try:
    import newrelic.agent
    from newrelic.api.exceptions import ConfigurationError
except ImportError:
    pass


def init_agent(license_key: str, config: str):
    logger = getLogger(__name__)

    env_value = os.environ.get('ODOO_STAGE', "dev")
    logger.info("NewRelic environment is {}".format(env_value))
    fd, filepath = tempfile.mkstemp()
    try:
        with os.fdopen(fd, "w") as file:
            parts = config.split("[newrelic]", 1)
            if len(parts) < 2:
                parts[1] = ""
            file.write(parts[0])
            file.write("[newrelic]\nlicense_key = {}\n".format(license_key))
            file.write(parts[1])
        newrelic.agent.initialize(filepath, env_value)
    except (ConfigurationError, OSError):
        logger.info("NewRelic failed to init due to configuration error: {}".format(format_exc()))
    except Exception:
        logger.info("NewRelic failed to init: {}".format(format_exc()))
    finally:
        os.remove(filepath)
    logger.info("NewRelic initialized successfully")
