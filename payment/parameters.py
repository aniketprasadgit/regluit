 
PAYMENT_TYPE_NONE = 0
PAYMENT_TYPE_INSTANT = 1
PAYMENT_TYPE_AUTHORIZATION = 2

TARGET_TYPE_NONE = 0
TARGET_TYPE_CAMPAIGN = 1
TARGET_TYPE_LIST = 2

PAYPAL_USERNAME = 'jakace_1309677337_biz_api1.gmail.com'
PAYPAL_PASSWORD =  '1309677386'
PAYPAL_SIGNATURE = 'A543DNCPfye3PpgUquUAuyfN2wNQAt.h8FJqHIro2U3-Z886XQvIdWSy'
PAYPAL_APPID = 'APP-80W284485P519543T'

PAYPAL_ENDPOINT = 'svcs.sandbox.paypal.com' # sandbox
PAYPAL_PAYMENT_HOST = 'http://www.sandbox.paypal.com' # sandbox

BASE_URL = 'http://76.28.117.198/'
COMPLETE_URL = 'paymentcomplete'
CANCEL_URL = 'paymentcancel'

PREAPPROVAL_PERIOD = 365 # days to ask for in a preapproval
PAYPAL_COMMISSION = 0.10

try:
    from local_parameters import *
except ImportError:
    pass