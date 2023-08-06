import logging
import random
import time

from optimizely import logger
from optimizely import optimizely
from optimizely.notification_center import NotificationCenter
from optimizely.config_manager import PollingConfigManager
from optimizely.helpers import enums
from optimizely.decision.optimizely_decide_option import OptimizelyDecideOption as DecideOption
from optimizely.odp.odp_config import OdpConfig
from optimizely.helpers import sdk_settings


def random_user_id():
    """Return random integer as string."""
    return 'user' + str(random.randrange(0, 1000001, 2))

user_id = random_user_id()


# ============================================
# custom polling config manager
# ============================================
notification_center = NotificationCenter()

conf_manager = PollingConfigManager(
    sdk_key='TbrfRLeKvLyWGusqANoeR',
    update_interval=3,
    logger=logger.SimpleLogger(logging.DEBUG)
)
optimizely_client = optimizely.Optimizely(config_manager=conf_manager, logger=logger.SimpleLogger(logging.DEBUG))

# ============================================
# plain polling config manager (using sdk key)
# ============================================
# optimizely_client = optimizely.Optimizely(sdk_key='TbrfRLeKvLyWGusqANoeR',
#                                           logger=logger.SimpleLogger(logging.DEBUG),
#                                           settings=sdk_settings.OptimizelySdkSettings(odp_event_flush_interval=0,
#                                                                                       odp_disabled=False))
config = optimizely_client.get_optimizely_config()   # opti config needs to come before creating user context and fetching for fetch to work properly !

attributes = {"laptop_os": "mac"}
# user = optimizely_client.create_user_context('matjaz-user-4', attributes)
user = optimizely_client.create_user_context('matjaz-user-5', attributes)

# for _ in range(100):
#     user.fetch_qualified_segments()
#     segments = user.get_qualified_segments()
#     print('  >>> SEGMENTS: ', segments)
#     options = [DecideOption.INCLUDE_REASONS]
#     decision = user.decide('flag1', options)
#     print(' >>> DECISION ', decision.as_json())
#     time.sleep(2)

# for segment in segments:
#     is_qualified = user.is_qualified_for(segment)
#     print(f'IS QUALIFIED for {segment}: ', is_qualified)

# user = optimizely_client.create_user_context('matjaz-user-2', attributes)
# user.fetch_qualified_segments()
# segments = user.get_qualified_segments()
# print('\n  >>> SEGMENTS2: ', segments)
#
# user = optimizely_client.create_user_context('fs-id-12', attributes)
# user.fetch_qualified_segments()
# segments = user.get_qualified_segments()
# print('\n  >>> SEGMENTS3: ', segments)
# time.sleep(2)


user.fetch_qualified_segments()
segments = user.get_qualified_segments()
print('  >>> SEGMENTS: ', segments)

# wait 90 seconds after running this - run only once to bind tester-101 to the email - run it once PER USER
optimizely_client.send_odp_event(type="any", action="", identifiers={ "fs_user_id": "matjaz-user123", "email": "matjaz-user-123@email.com" })
# optimizely_client.send_odp_event(type="any", action="any", identifiers={ "test": "test" })

# options = [DecideOption.INCLUDE_REASONS]
# decision = user.decide('flag1', options)
# print('\n >>> DECISION ', decision.as_json())

# # Track event
# user.track_event('myevent')

optimizely_client.close()


# # =========================================================
# # DECIDE ALL
# # =========================================================
# print("\n======  DECIDE ALL ======\n")
#
# options_all = [DecideOption.INCLUDE_REASONS]
# decisions = user.decide_all(options_all)

#
# print(' >>> DECISIONS: ')
# for d, v in decisions.items():
#     print(' >>> DECISION FOR ', d, v.as_json())
#
# options_all_for_enabled_flags = [DecideOption.ENABLED_FLAGS_ONLY]
# decisions_for_enabled_flags = user.decide_all(options_all_for_enabled_flags)
# all_enabled_flags = sorted(list(decisions_for_enabled_flags.keys()))
# print(' >>> GET ENABLED FLAGS ', all_enabled_flags)
#
# print(' >>> INDIVIDUAL PROPERTIES FOR FEATURE3: ')
# decision_feature3 = decisions['feature3']
# print(' >>> [DECIDE ALL] VARIATION KEY FOR FEATURE 3 ', decision_feature3.variation_key)
# print(' >>> [DECIDE ALL] ENABLED', decision_feature3.enabled)
# print(' >>> [DECIDE ALL] VARIABLES', decision_feature3.variables)
# print(' >>> [DECIDE ALL] RULE KEY', decision_feature3.rule_key)
# print(' >>> [DECIDE ALL] FLAG KEY', decision_feature3.flag_key)
# print(' >>> [DECIDE ALL] REASONS', decision_feature3.reasons)
# print(' >>> [DECIDE ALL] USER CONTEXT for FEATURE 3 ', decision_feature3.user_context.as_json())

# # =========================================================
# # DECIDE FOR KEYS
# # =========================================================
# print("\n======  DECIDE FOR KEYS ======\n")
#
# options_keys = [DecideOption.INCLUDE_REASONS]
# keys = ['feature1', 'feature2', 'feature3']
# decisions_keys = user.decide_for_keys(keys, options_keys)
#
# print(' >>> DECISIONS FOR KEYS: ')
# for d, v in decisions_keys.items():
#     print(' >>> DECISION FOR KEY ', d, v.as_json())
#
# # print and verify individual decision for two individual features (ie feature1 and feature3) just like
# # in decide_all but for two features, making sure they work properly
# print(' >>> [DECIDE FOR KEYS] INDIVIDUAL PROPERTIES FOR FEATURE3: ')
# decision_key_feature1 = decisions['feature1']
# decision_key_feature3 = decisions['feature3']
#
# print(' >>> [DECIDE FOR KEYS] VARIATION KEY FOR FEATURE 1 ', decision_key_feature1.variation_key)
# print(' >>> [DECIDE FOR KEYS] VARIATION KEY FOR FEATURE 3 ', decision_key_feature3.variation_key)
#
# # etc ...
#
# # =========================================================
# # FORCED VARIATION
# # =========================================================
# # 1. decide(feat1) exp1 -> var1
# # 2. setForcedVariation(exp1, var2)
# # 3. decide(feat1) exp1 -> var2
# print("\n ========= FORCED VARIATION ===========\n")
#
# # 1 - done above - confirm that decide shows "variation_1_feature_test"
# opt = [DecideOption.INCLUDE_REASONS]
# dec1 = user.decide("feature1", opt)
# print(" >>> [FORCED VARIATION] DECISION: ", dec1.variation_key)
#
# # 2 - force in "variation_2_feature_test"
# optimizely_client.set_forced_variation('feature1_test', user_id, 'variation_2_feature_test')
# print("\n >>>>> [FORCED VARIATION] New variation forced in.")
#
# dec2 = user.decide('feature1', opt)
#
# # 3 - verify that experiment now shows the forced vartiation - "variation_2_feature_test"
# print(" >>> [FORCED VARIATION] NEW FORCED VARIATION: ", dec2.variation_key)

