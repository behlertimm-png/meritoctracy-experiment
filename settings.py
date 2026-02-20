from os import environ

SESSION_CONFIGS = [
dict(
    name='meritocracy_low',
    display_name="Meritocracy (LOW prize)",
    app_sequence=['meritocracy'],
    num_demo_participants=2,
    prize=5,
    p_intervene=0.25,
    comp_pay_per_correct=0.20,
    belief_bonus=1.00,
    participation_fee=5,
    bonus_cap=10,
),
dict(
    name='meritocracy_high',
    display_name="Meritocracy (HIGH prize)",
    app_sequence=['meritocracy'],
    num_demo_participants=2,
    prize=20,
    p_intervene=0.25,
    comp_pay_per_correct=0.20,
    belief_bonus=1.00,
    participation_fee=5,
    bonus_cap=20,
),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

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
