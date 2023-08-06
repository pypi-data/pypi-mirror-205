import logging
import random
import time

from optimizely import event_dispatcher as optimizely_event_dispatcher
from optimizely import logger
from optimizely import optimizely
from optimizely.decision.optimizely_decide_option import OptimizelyDecideOption as DecideOption
from optimizely.event import event_processor
from optimizely.event_dispatcher import EventDispatcher as event_dispatcher


# TODO IDEAS:
#  - reproduce by running experiment and seeing if I get 304 errors/timeouts, measure response time, make sure it's not our server-cdn issue - set up loop
#  - invalid config - if download failed, then the cached datafile should be used -- check --> ic caching on line 344, 345 in config_manager.py?
#     - invalid config should only happen when download fails AND cached datafile is not used
#     - Chanhelog in release 3.4.0: "* Added caching for `get_optimizely_config()` - `OptimizelyConfig` object will be cached and reused for the lifetime of the datafile."
#     - in README: "Initial datafile, typically sourced from a local cached source"
#  - what if they increase timeout from 10s to longer?
#  - AKAMAI - cdn downtime?


def random_user_id():
    """Return random integer as string."""
    return 'user' + str(random.randrange(0, 1000001, 2))


user_id = random_user_id()

event_dispatcher_ = optimizely_event_dispatcher.EventDispatcher

batch_processor = event_processor.BatchEventProcessor(
    event_dispatcher,
    batch_size=10,
    flush_interval=1000,
    logger=logger.SimpleLogger(logging.DEBUG),
    start_on_init=True
)

optimizely_client = optimizely.Optimizely(sdk_key='VKpgMkyxhcDYEeFy7gekH',
                                          event_processor=batch_processor,
                                          logger=logger.SimpleLogger(logging.DEBUG))

for _ in range(500):
    user = optimizely_client.create_user_context(user_id, {'attribute1': 'hello9'})
    decision = user.decide('flag1', [DecideOption.INCLUDE_REASONS])
    print('DECISION ', decision.as_json())
    print('\n=======================\n')
    time.sleep(300)     # wait 5 min between generating each event, that's same as default polling interval, then watch logs. computer should not go to sleep though...