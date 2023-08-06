import logging
import random, time

from optimizely import logger
from optimizely import optimizely
from optimizely.decision.optimizely_decide_option import OptimizelyDecideOption as DecideOption
from optimizely import event_dispatcher as optimizely_event_dispatcher
from optimizely.event import event_processor
from optimizely.event_dispatcher import EventDispatcher as event_dispatcher

from optimizely.optimizely_user_context import OptimizelyUserContext


def random_user():
    return 'user' + str(random.randrange(0, 1000001, 2))     # user_id MUST BE RANDOMIZED!!


event_dispatcher_ = optimizely_event_dispatcher.EventDispatcher

batch_processor = event_processor.BatchEventProcessor(
    event_dispatcher,
    batch_size=10,
    flush_interval=1000,
    logger=logger.SimpleLogger(logging.DEBUG),
    start_on_init=True
)

optimizely_client = optimizely.Optimizely(sdk_key='X9mZd2WDywaUL9hZXyh9A',
                                          event_processor=batch_processor)

# regular impression events
# for _ in range(100):
for _ in range(100):
    user = optimizely_client.create_user_context(random_user(), {"age": 20})
    decision = user.decide('flag1', [DecideOption.INCLUDE_REASONS])
    time.sleep(0.2)     # Please use some small time spacing, otherwise there can be anomalies in event results

# impression events for forced decisions
# for _ in range(100):
#     user = optimizely_client.create_user_context(random_user(), {"age": 20})
#     context = OptimizelyUserContext.OptimizelyDecisionContext(flag_key='flag1', rule_key='flag1_experiment')
#     decision = OptimizelyUserContext.OptimizelyForcedDecision(variation_key='variation_a')
#     user.set_forced_decision(context, decision)
#     decide_decision = user.decide('flag1', [DecideOption.INCLUDE_REASONS])
#     time.sleep(0.2)     # Please use some small time spacing, otherwise there can be anomalies in event results

batch_processor.stop()
