# try mocking this very simple class instance of a logger:
# HOW TO MOCK logger that is instantiated? (with mock.path.object()?)

import logging

from optimizely import logger
from optimizely import optimizely
from optimizely.helpers.sdk_settings import OptimizelySdkSettings


sdk_settings = OptimizelySdkSettings(odp_disabled=True)
optimizely_client = optimizely.Optimizely(sdk_key='QoaqTFiC4fgU4j9dZtadP',
                                          logger=logger.SimpleLogger(logging.DEBUG).logger,
                                          settings=sdk_settings)


x = optimizely_client.sdk_settings
print('SETTINGS ', x)

