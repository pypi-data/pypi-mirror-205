import logging
import random

from optimizely import logger
from optimizely import optimizely
from optimizely.helpers import enums
from optimizely.decision.optimizely_decide_option import OptimizelyDecideOption as DecideOption


# TODO NOTE: Reasons don't display
# TODO NOTE: Default decide options don't seem to work. They don't have an effect

# example how UPS is used in Py SDK - for the sample?
# https://github.com/optimizely/python-sdk/commit/f3e3854327df163214ffde65c34583343d290c7e#diff-3f4dc3a19906104fb55fe8d94268caa8abb9d2f49df5ba32570d617682c4edf7R294

# datafile is from the project "decide_api_bash_legacy" at app.optimizely.com
# on matjaz's optimizely's account
def random_user_id():
    """Return random integer as string."""
    return 'user' + str(random.randrange(0, 1000001, 2))


class CustomConfigManager:
    def get_config(self):
        pass

user_id = random_user_id()
optimizely_client = optimizely.Optimizely(sdk_key='QoaqTFiC4fgU4j9dZtadP',
                                          logger=logger.SimpleLogger(logging.DEBUG),
                                          config_manager=CustomConfigManager()
                                          # default_decide_options=[DecideOption.INCLUDE_REASONS,
                                          #                         DecideOption.DISABLE_DECISION_EVENT,
                                          #                         DecideOption.ENABLED_FLAGS_ONLY,
                                          #                         DecideOption.EXCLUDE_VARIABLES,
                                          #                         DecideOption.IGNORE_USER_PROFILE_SERVICE]
                                          )

# notification listener with LOG EVENTS
def on_log_event(logEvent):
    print('\n >>> LOG EVENT: ', logEvent)

optimizely_client.notification_center.add_notification_listener(enums.NotificationTypes.LOG_EVENT, on_log_event)


# notification listener with DECISION EVENTS

#   =========================================================
#   DECIDE
#   =========================================================
print("\n======  DECIDE  ======\n")

attributes = {"attribute1": "decide_bash"}
options = [DecideOption.INCLUDE_REASONS]
user = optimizely_client.create_user_context(user_id, attributes)
decision = user.decide('flag1', options)
print(' >>> DECISION ', decision.as_json())

print('DEC VARS ---- ', decision.variables, type(decision.variables))

print(' >>> VARIATION KEY ', decision.variation_key)
print(' >>> ENABLED ', decision.enabled)
print(' >>> VARIABLES ', decision.variables)
print(' >>> RULE KEY ', decision.rule_key)
print(' >>> FLAG KEY ', decision.flag_key)
print(' >>> REASONS ', decision.reasons)
print(' >>> USER CONTEXT USER ID ', decision.user_context.user_id)
print(' >>> USER CONTEXT ATTRIBUTES ', decision.user_context.get_user_attributes())
print(' >>> USER AS JSON ', user.as_json())


# # Track event
# user.track_event('myevent')
#
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
