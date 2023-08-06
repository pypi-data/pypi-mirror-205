#!/usr/bin/python
# example: python basic.py <SDK-Key>
# This basic example shows how to make individual decision requests with decide api

import json
import requests
import sys

# if len(sys.argv) < 2:
#     sys.exit('Requires one argument: <SDK-Key>')
#
# sdk_key = sys.argv[1]

s = requests.Session()
# s.headers.update({'X-Optimizely-SDK-Key': 'Hy2EzGGCPaSwc4JoQuDkY'})
s.headers.update({'X-Optimizely-SDK-Key': 'TbrfRLeKvLyWGusqANoeR'})

# resp = s.get('http://localhost:8080/v1/config')
# env = resp.json()

# ==================================
# DECIDE
# ==================================

# payload = {
#     "userId": "test-user",
#     "decideOptions": [
#         "ENABLED_FLAGS_ONLY",
#         "INCLUDE_REASONS"
#     ],
#     "userAttributes": {
#         "laptop_os": "mac"
#     }
# }
#
# resp = s.post(url = 'https://agent.api.optimizely.com/v1/decide', params={"keys": "flag1"}, json=payload)
# print(json.dumps(resp.json(), indent=4, sort_keys=True))

# ==================================
# FETCH QUALIFIED SEGMENTS - WITH DECIDE
# ==================================

# TODO - here is example of the payload with added a field for odp segments (for fetch endpoint only)
#  - we add "with-odp-segment" field to the decide payload ! cause we're embedding it into decide
#  - BUT ALSO ADD PAYLOAD JUST FOR FETCH WULIFIED SEGMENTS - WE WILL HAVE BOTH !! (inside decide and separate)
# payload_w_fetch_segments_w_decide = {
#     "userId": "test-user",
#     "decideOptions": [
#         "ENABLED_FLAGS_ONLY",
#         "INCLUDE_REASONS"
#     ],
#     "userAttributes": {
#         "laptop_os": "mac"
#     },
#     "withOdpSegment": True
# }
#
# for key in env['featuresMap']:
#     params = {"keys": key}
#     resp = s.post(url = 'http://localhost:8080/v1/decide', params=params, json=payload_w_fetch_segments_w_decide)
#     print("Flag key: {}".format(key))
#     print(json.dumps(resp.json(), indent=4, sort_keys=True))

# ==================================
# FETCH QUALIFIED SEGMENTS
# ==================================
# payload for fetch that is separate form decide

payload = {
    "fetchSegments": True,
    "userId": "matjaz-user-4",
    "userAttributes": {
            "laptop_os": "mac"
        },
    "fetchSegmentsOptions": [
        "IGNORE_CACHE",
        "RESET_CACHE"
    ]
}

resp = s.post(url='http://localhost:8080/v1/decide', json=payload)
print('STATUS ', resp.status_code)
print(json.dumps(resp.json(), indent=4, sort_keys=True))

# ==================================
# SEND ODP EVENT
# ==================================
# payload = {
#     "action": "any",
#     "type": "any",
#     "identifiers": {
#         "fs_user_id": "matjaz_user_12345",
#     },
#     "data": None
# }
#
# resp = s.post(url='http://localhost:8080/v1/send-odp-event', json=payload)
# print(json.dumps(resp.json(), indent=4, sort_keys=True))

"""
----
TEST CASES:
1. The value of the action argument of sendOdpEvent method is nil||null||none.	The sendOdpEvent method is called.	The method calls fails and the following error is logged: ODP action is not valid (cannot be empty).

2. The value of the action argument of sendOdpEvent method is an empty string ("").	The sendOdpEvent method is called.	The method calls fails and the following error is logged: ODP action is not valid (cannot be empty).

3. The value of the type argument of sendOdpEvent method is nil||null||none.	The sendOdpEvent method is called.	The provided argument is converted into the string value of fullstack which is used in the method call.

4. The value of the type argument of sendOdpEvent method is an empty string ("").	The sendOdpEvent method is called.	The provided argument is converted into the string value of fullstack which is used in the method call.

5. The value of the identifiers argument of sendOdpEvent method contains only fs_user_id||fs-user-id||FS-USER-ID||FS_USER_ID.	The sendOdpEvent method is called.	The provided argument is converted into the string value of fs_user_id which is used in the method call.
    Findings:
    - remove email, replace fs_user_id with custom name: Go-sdk gives ODP event send failed (400 Bad Request) error when identifier keys invalid, agent gives "success: true", but event in inspector gets "Error" - should we change success: true to false?
        - be careful what should go-sdk handle versus what should Agent handle
        - go-sdk receives identifier "custom-identifier": "matjaz-user-12345" and recognizes that it's invalid (does go-sdk create a BadRequest error log somewhere?)

----


"""

