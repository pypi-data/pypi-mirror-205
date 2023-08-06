import logging
import random
import json

from optimizely import logger
from optimizely import optimizely
from optimizely.helpers import enums
from optimizely.decision.optimizely_decide_option import OptimizelyDecideOption as DecideOption
from optimizely.config_manager import PollingConfigManager
from optimizely import notification_center
from optimizely.optimizely_user_context import OptimizelyUserContext


def random_user_id():
    """Return random integer as string."""
    return 'user' + str(random.randrange(0, 1000001, 2))


# with open('similar_rule_keys_audience.json') as json_file:
#     datafile = json_file.read()

# with open('flags_with_rollouts.json') as json_file:
#     datafile = json_file.read()

# datafile is from the Flags project "matjaz_optimizely_config_v2" at app.optimizely.com on matjaz's optimizely's account
user_id = random_user_id()

notif_center = notification_center.NotificationCenter()

# polling_config_manager = PollingConfigManager(
#     # sdk_key='FCnSegiEkRry9rhVMroit4',
#     sdk_key='Hy2EzGGCPaSwc4JoQuDkY',    # "matjaz_optimizely_config_v2"
#     # sdk_key='TyCyNiv9RwJfDoajQuDiH',    # multiple flags
#     blocking_timeout=1,
#     notification_center=notif_center,
#     logger=logger.SimpleLogger(logging.INFO)
# )
#
# optimizely_client = optimizely.Optimizely(config_manager=polling_config_manager,
#                                           logger=logger.SimpleLogger(logging.INFO),
#                                           notification_center=notif_center)

# optimizely_client = optimizely.Optimizely(datafile='datafile', logger=logger.SimpleLogger(min_level=logging.DEBUG))
# optimizely_client = optimizely.Optimizely(datafile='not valid')


optimizely_client = optimizely.Optimizely(sdk_key='X9mZd2WDywaUL9hZXyh9A',
                                          logger=logger.SimpleLogger(logging.ERROR))


project_config = optimizely_client.config_manager.get_config()

# notification listener with LOG EVENTS
def on_log_event(logEvent):
    pass
    # print('\n >>> LOG EVENT: ', logEvent)

optimizely_client.notification_center.add_notification_listener(enums.NotificationTypes.LOG_EVENT, on_log_event)


# notification listener with DECISION EVENTS
# listener needs to be before decide is instantiated
def on_config_update_listener(*args):
    config = optimizely_client.get_optimizely_config()
    # print("LISTENER [OptimizelyConfig] revision = ", config.revision)


optimizely_client.notification_center.add_notification_listener(
    enums.NotificationTypes.OPTIMIZELY_CONFIG_UPDATE, on_config_update_listener)

#   =========================================================
#   DECIDE
#   =========================================================
# print("\n======  DECIDE  ======\n")


# attributes = {"attribute1": "helloa", "attribute2": "hellob", "attribute3": "helloc", "attribute_typed": 18}

options = [DecideOption.INCLUDE_REASONS, DecideOption.IGNORE_USER_PROFILE_SERVICE]

# user = optimizely_client.create_user_context(user_id) # for flags only
# user = optimizely_client.create_user_context('test_user_1') # for flags only

attributes = {"attribute1": "helloa", "attribute2": "hellob"}       # for AB experiments
user = optimizely_client.create_user_context(user_id, attributes)   # for AB experiments

# attributes_for_delivery = {"attr_for_delivery_1": "attr for delivery 1"}    # for targeted deliveries 1
# user = optimizely_client.create_user_context(user_id, attributes_for_delivery)   # for targeted deliveries


# print('\n============================')
# print('  FORCED DECISIONS   ')
# print('============================')
"""
Jae:
CHECKS FOR FORCED DECISIONS ARE MADE IN SEQUENCE - 3 CHECKS:

1. we check if flags (no rule_key) have forced decisions. We look in optimizely.py/_decide()
  - in _decide() function ---> checks if flags have forced decision (no rule_key)

2. We check if any forced decisions in ab experiments
  - in get_variation_from_experiment_rule()

3. Third we check for targeted deliveries (rollouts)
  - in get_variation_from_delivery_rule()
        
Experiments can obstruct targeted deliveries!!! Pause experiment or apply specific audience to targted deliveries.
"""
# TODO In find_validated_forced_decision I don't think I use "options" parameters from function signatures in reasons. I initialise reasons as [], but don't add reasons from options - options is empty but still need to add to reasons? I don't know

# TODO CANT REPRO THE ISSUE: important: refactor get_variation_from_experiment_rule(self, config, flag_key, rule, user, options) function to have feature instead of flag_key as param! (see example in get_variation_for_rollout)

# TODO VERY GOOD QUESTION !!!: do I need to replace "return decision_variation, decide_reasons" with Decision(...) ??? in decision_service? or are tuples ok, do they return same type? (I changed for ..._rollout where None didn't work Needed to be Decision(None, None, ...source))

# TODO NEED TO IMPROVE LOGGING IN USER CONTEXT - TOO VERBOSE !!! --> self.log.logger.error(OptimizelyDecisionMessage.SDK_NOT_READY)
#  - noty critical

# TODO IMPORTANT - TRY FIXING THIS!!! maybe comment in PR: why am I logging two find validated fd logs, but Jae logs only one (for me the first pass without rule key is logged too)
#  related? -> WHY IS IT printing TWO strings of reasons because they should be mutually exclusibe in if statement in function find_validated_forced_decisison(). Example from test test_decide_reasons__hit_user_profile_service
#  then tests have such multiple logs as well

# TODO - make sure to add a test for multiple flags. My test datafile only has a single flag. Because for loop needs to work across all flags.

# TODO !!! MATJAZ IMPORTANT - DISCUSSED by DEVX team and Jae: rule_key in set_forced_decision MUST be set to None, not to empty string! EMpty string gets overwritten with experiment/rule key !!!

# TODO I think I missed few checks for None state. Jae has more if statements to check.

# TODO NEXT:
#   - run local unit tests as a check - DONE
#   - lint and push to branch
#   - add testapp methods
#   - run FSC (custom build)
#   - add unit tests


# context_flag = OptimizelyUserContext.OptimizelyDecisionContext(flag_key='flag1')
# forced_flag = OptimizelyUserContext.OptimizelyForcedDecision(variation_key='variation2')
# success_flag = user.set_forced_decision(context_flag, forced_flag)
# decision_flag = user.decide('flag1', options)
# print('FLAG from DECISION ', decision_flag.flag_key)    # flag1
# print('SUCCESS FLAG ', success_flag)
# print('SET_DECISION_RULE KEY- ', decision_flag.rule_key)    # default-rollout-3944-20512300778
# print('SET_DECISION_FLAG - ', decision_flag.variation_key)  # off
# variation_key_flag = user.get_forced_decision(context_flag)
# print('GET FORCED DECICISION FLAG ', variation_key_flag.variation_key)
# removed1 = user.remove_forced_decision(context_flag)
# print('REMOVED ', removed1)
# removed_all = user.remove_all_forced_decisions()
# print('REMOVED ALL', removed_all)


# DECIDE ALL WITH MULTIPLE FLAGS

# print('Scenario: Set forced decision is called twice with multiple flag keys.')
# import json
#
# context_flag1 = OptimizelyUserContext.OptimizelyDecisionContext(flag_key='flag1', rule_key=None)
# forced_flag1 = OptimizelyUserContext.OptimizelyForcedDecision(variation_key='variation2')
#
# context_flag2 = OptimizelyUserContext.OptimizelyDecisionContext(flag_key='flag2', rule_key=None)
# forced_flag2 = OptimizelyUserContext.OptimizelyForcedDecision(variation_key='on')
#
# user.set_forced_decision(context_flag1, forced_flag1)
# user.set_forced_decision(context_flag2, forced_flag2)
#
# decisions_flags = user.decide_all(options)
#
# flags_json = [decisions_flags[fl].as_json() for fl in decisions_flags]
# print(json.dumps(flags_json))

# TODO - Remove Forced Decisions called before calling decide_all.
# print('\nScenario: Remove Forced Decisions called before calling decide_all.')
#
# context_flag1 = OptimizelyUserContext.OptimizelyDecisionContext(flag_key='flag_3')
# forced_flag1 = OptimizelyUserContext.OptimizelyForcedDecision(variation_key='variation_1')
#
# context_flag2 = OptimizelyUserContext.OptimizelyDecisionContext(flag_key='flag_2')
# forced_flag2 = OptimizelyUserContext.OptimizelyForcedDecision(variation_key='variation_2')
#
# user.set_forced_decision(context_flag1, forced_flag1)
# user.set_forced_decision(context_flag2, forced_flag2)
#
# removed1 = user.remove_forced_decision(context_flag1)
#
# decisions_flags = user.decide_all(options)
#
# # decision = user.decide("flag_3", options)
# # print(json.dumps(decision.as_json(), indent=2))
#
# flags_json = [decisions_flags[fl].as_json() for fl in decisions_flags]
# print(json.dumps(flags_json, indent=2))

# flags_json = [decisions_flags[fl].as_json() for fl in decisions_flags if decisions_flags[fl].as_json()["flag_key"] == "flag_2"]
# print(json.dumps(flags_json, indent=2))




context_ab = OptimizelyUserContext.OptimizelyDecisionContext(flag_key='flag1', rule_key='flag1_experiment')
forced_ab = OptimizelyUserContext.OptimizelyForcedDecision(variation_key='variation2')

success_ab = user.set_forced_decision(context_ab, forced_ab)

decision_ab = user.decide('flag1', options)
# print('\n   >>> user.decide ENABLED: ', success_ab)
# print('   >>> user.decide DECISION VAR: ', decision_ab.variation_key)
# forced_decision_ab = user.get_forced_decision(context_ab)
# print('   >>> GET FORCED DECISION AB ', forced_decision_ab.variation_key)
# print(decision_ab.reasons)
#
# #decision should be false, because we have forced decision instead
# enabled = decision_ab.enabled
# print('ENABLED AFTER FD SET ', enabled)

# removed2 = user.remove_forced_decision(context_ab)
# print('REMOVED ', removed2)
# variation_key_ab = user.get_forced_decision(context_ab)
# print('   >>> GET FORCED DECISION AB ', variation_key_ab)
# assert variation_key_ab == None

# decision should be true, because we removed the forced decision
# decision_ab = user.decide('flag1', options)
# print('ENABLED AFTER REMOVAL OF FD ', decision_ab.enabled)



# # removed_all = user.remove_all_forced_decisions()
# # print('REMOVED ALL', removed_all)





# print('>>> TARGETED DELIVERY')
# context_targ = OptimizelyUserContext.OptimizelyDecisionContext(flag_key='flag1', rule_key='flag1_targeted_delivery')
# context_targ = OptimizelyUserContext.OptimizelyDecisionContext(flag_key='flag1', rule_key='default-rollout-6550-20512300778')
# forced_targ = OptimizelyUserContext.OptimizelyForcedDecision(variation_key='invalid')
# forced_targ = OptimizelyUserContext.OptimizelyForcedDecision(variation_key='invalid')
#
# success_targ = user.set_forced_decision(context_targ, forced_targ)
# decision_targ = user.decide('flag1', options)
# print('\n   >>> SUCCESS TARG ', success_targ)
# print('   >>> SET DECISION TARGETED ', decision_targ.variation_key)
# forced_decision_targeted_d = user.get_forced_decision(context_targ)
# print('   >>> GET FORCED DECISION TARG ', forced_decision_targeted_d.variation_key)
# print(decision_targ.reasons)

# removed3 = user.remove_forced_decision(context_targ)
#
# print('REMOVED ', removed3)

# decision_targ = user.decide('flag1', options)
# print(decision_targ.enabled)
# print(decision_targ.reasons)
# print('\n')
# print(decision_targ.as_json())


# print('REMOVED ', removed3)
# removed_all = user.remove_all_forced_decisions()
# print('REMOVED ALL', removed_all)



