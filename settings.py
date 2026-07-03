from os import environ

SESSION_CONFIGS = [
    dict(
        name='meritocracy_low_iq',
        display_name="Meritocracy (LOW prize, IQ framing)",
        app_sequence=['meritocracy'],
        num_demo_participants=2,
        treatment='low_iq', # Set parameters according to treatment in create_session
        # prize=2,
        # framing='iq',
        belief_bonus=2.00,
        participation_fee=2.00,
    ),
    dict(
        name='meritocracy_low_questionnaire',
        display_name="Meritocracy (LOW prize, questionnaire framing)",
        app_sequence=['meritocracy'],
        num_demo_participants=2,
        treatment='low_quest',
        # prize=2,
        # framing='questionnaire',
        belief_bonus=2.00,
        participation_fee=2.00,
    ),
    dict(
        name='meritocracy_high_iq',
        display_name="Meritocracy (HIGH prize, IQ framing)",
        app_sequence=['meritocracy'],
        num_demo_participants=2,
        treatment='high_iq',
        # prize=12,
        # framing='iq',
        belief_bonus=2.00,
        participation_fee=2.00,
    ),
    dict(
        name='meritocracy_high_questionnaire',
        display_name="Meritocracy (HIGH prize, questionnaire framing)",
        app_sequence=['meritocracy'],
        num_demo_participants=2,
        treatment='high_quest',
        # prize=12,
        # framing='questionnaire',
        belief_bonus=2.00,
        participation_fee=2.00,
    ),
    dict(
        name='meritocracy_random',
        display_name="Meritocracy RANDOM TREATMENT",
        app_sequence=['meritocracy'],
        num_demo_participants=8,
        belief_bonus=2.00,
        participation_fee=2.00,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = ['timed_out']
SESSION_FIELDS = []


POINTS_DECIMAL_PLACES = 2

# On group_by_arrival_time wait pages, oTree prompts participants with
# "Are you still there?" after this many seconds of inactivity (default: 120).
# Set high enough that it should never actually trigger.
GBAT_INACTIVE_SECONDS_UNTIL_PROMPT = 10 * 60

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '4537307298521'
