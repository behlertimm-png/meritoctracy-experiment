from otree.api import *
import random
import itertools
import time
import csv
import functools
from pathlib import Path


doc = """
Meritocracy experiment skeleton.
"""

WAIT_PAGE_TIMEOUT = 5 * 60  # 5 minutes


class C(BaseConstants):
    NAME_IN_URL = 'meritocracy'
    PLAYERS_PER_GROUP = 2

    # 36 puzzle rounds (Part 1) + 1 final round (matching/Part 2, no puzzle)
    NUM_ROUNDS = 37

    # One image per round (round 1 uses index 0, etc.)
    # Filenames match your actual files exactly: IQ_1.JPG ... IQ_36.JPG
    PUZZLE_IMAGES = [
        'meritocracy/puzzles/IQ_1.JPG',
        'meritocracy/puzzles/IQ_2.JPG',
        'meritocracy/puzzles/IQ_3.JPG',
        'meritocracy/puzzles/IQ_4.JPG',
        'meritocracy/puzzles/IQ_5.JPG',
        'meritocracy/puzzles/IQ_6.JPG',
        'meritocracy/puzzles/IQ_7.JPG',
        'meritocracy/puzzles/IQ_8.JPG',
        'meritocracy/puzzles/IQ_9.JPG',
        'meritocracy/puzzles/IQ_10.JPG',
        'meritocracy/puzzles/IQ_11.JPG',
        'meritocracy/puzzles/IQ_12.JPG',
        'meritocracy/puzzles/IQ_13.JPG',
        'meritocracy/puzzles/IQ_14.JPG',
        'meritocracy/puzzles/IQ_15.JPG',
        'meritocracy/puzzles/IQ_16.JPG',
        'meritocracy/puzzles/IQ_17.JPG',
        'meritocracy/puzzles/IQ_18.JPG',
        'meritocracy/puzzles/IQ_19.JPG',
        'meritocracy/puzzles/IQ_20.JPG',
        'meritocracy/puzzles/IQ_21.JPG',
        'meritocracy/puzzles/IQ_22.JPG',
        'meritocracy/puzzles/IQ_23.JPG',
        'meritocracy/puzzles/IQ_24.JPG',
        'meritocracy/puzzles/IQ_25.JPG',
        'meritocracy/puzzles/IQ_26.JPG',
        'meritocracy/puzzles/IQ_27.JPG',
        'meritocracy/puzzles/IQ_28.JPG',
        'meritocracy/puzzles/IQ_29.JPG',
        'meritocracy/puzzles/IQ_30.JPG',
        'meritocracy/puzzles/IQ_31.JPG',
        'meritocracy/puzzles/IQ_32.JPG',
        'meritocracy/puzzles/IQ_33.JPG',
        'meritocracy/puzzles/IQ_34.JPG',
        'meritocracy/puzzles/IQ_35.JPG',
        'meritocracy/puzzles/IQ_36.JPG',
    ]

    # Correct option for each puzzle, as an integer 1..8
    CORRECT_ANSWERS = [
        5,  # IQ_1
        1,  # IQ_2
        7,  # IQ_3
        4,  # IQ_4
        3,  # IQ_5
        1,  # IQ_6
        6,  # IQ_7
        1,  # IQ_8
        8,  # IQ_9
        4,  # IQ_10
        5,  # IQ_11
        6,  # IQ_12
        2,  # IQ_13
        1,  # IQ_14
        2,  # IQ_15
        4,  # IQ_16
        6,  # IQ_17
        7,  # IQ_18
        3,  # IQ_19
        8,  # IQ_20
        8,  # IQ_21
        7,  # IQ_22
        6,  # IQ_23
        3,  # IQ_24
        7,  # IQ_25
        2,  # IQ_26
        7,  # IQ_27
        5,  # IQ_28
        6,  # IQ_29
        5,  # IQ_30
        4,  # IQ_31
        8,  # IQ_32
        5,  # IQ_33
        1,  # IQ_34
        3,  # IQ_35
        2,  # IQ_36
    ]

class Subsession(BaseSubsession):
    pass


def creating_session(subsession):
    print("creating_session called, round:", subsession.round_number, flush=True)
    treatment_list = [
        ['low_iq', 'low_iq'],
        ['low_quest', 'low_quest'],
        ['high_iq', 'high_iq'],
        ['high_quest', 'high_quest'],
    ]
    random.shuffle(treatment_list)
    treatment_list = list(itertools.chain.from_iterable(treatment_list))
    treatment_cycle = itertools.cycle(treatment_list)

    if subsession.round_number == 1:
        for player in subsession.get_players():
            player.participant.timed_out = False
            if 'treatment' not in subsession.session.config:
                print("Randomly assigning treatment for player", player.id_in_subsession)
                player.treatment = next(treatment_cycle)
            else:
                player.treatment = subsession.session.config['treatment']
            print("Treatment:", player.treatment)

            if player.treatment == 'low_iq':
                player.prize = 2
                player.framing = 'iq'
            elif player.treatment == 'low_quest':
                player.prize = 2
                player.framing = 'questionnaire'
            elif player.treatment == 'high_iq':
                player.prize = 12
                player.framing = 'iq'
            elif player.treatment == 'high_quest':
                player.prize = 12
                player.framing = 'questionnaire'
    else:
        for player in subsession.get_players():
            p1 = player.in_round(1)
            player.prize = p1.prize
            player.framing = p1.framing
            player.treatment = p1.treatment




def group_by_arrival_time_method(_subsession, waiting_players):
    for p in waiting_players:
        p.participant.vars.setdefault('meritocracy_wait_started_at', time.time())

    low_iq = [p for p in waiting_players if p.treatment == 'low_iq']
    low_quest = [p for p in waiting_players if p.treatment == 'low_quest']
    high_iq = [p for p in waiting_players if p.treatment == 'high_iq']
    high_quest = [p for p in waiting_players if p.treatment == 'high_quest']

    for group in [low_iq, low_quest, high_iq, high_quest]:
        if len(group) >= 2:
            return group[:2]

    # No same-treatment partner available yet. If someone has been waiting
    # too long, place them alone in a singleton group so they can be
    # fallback-matched against a donor from the pilot study instead of
    # waiting indefinitely (see finalize_singleton_outcome).
    now = time.time()
    timed_out = [
        p for p in waiting_players
        if now - p.participant.vars['meritocracy_wait_started_at'] >= WAIT_PAGE_TIMEOUT
    ]
    if timed_out:
        timed_out.sort(key=lambda p: p.participant.vars['meritocracy_wait_started_at'])
        return [timed_out[0]]

    return None


class Group(BaseGroup):
    # Old fields from old part 2 mechanism, kept for now so old code/data references don't break
    selected_player = models.IntegerField()
    intervene = models.BooleanField()


class Player(BasePlayer):
    # --- Treatment variables ---
    prize = models.IntegerField()
    framing = models.StringField()
    treatment = models.StringField()
    # --- Consent Form ---

    consent = models.StringField(
    choices=[
            ['yes', 'I agree and confirm that I live in the US and am 18 years of age or older.'],
            ['no', 'I don’t agree.'],
        ],
    widget=widgets.RadioSelect,
    label="",
    )

    prolific_id = models.StringField()


    # --- Part 1 (puzzles) ---
    answer = models.IntegerField(
    choices=[
        [1, '1'],
        [2, '2'],
        [3, '3'],
        [4, '4'],
        [5, '5'],
        [6, '6'],
        [7, '7'],
        [8, '8'],
    ],
    widget=widgets.RadioSelect,
    blank=True,
    label="Select an answer:",
    )

    is_correct = models.BooleanField(initial=False)
    total_correct = models.IntegerField(initial=0)
    other_player_total_correct = models.IntegerField(initial=0)
    stop_part1 = models.BooleanField(initial=False)
    action = models.StringField(blank=True)

    # --- Part 2 outcome mechanism (moved from Group to Player) ---
    # For a real 2-player match, both players' rows are set to mirrored/
    # coordinated values inside finalize_pair_outcome() so the pair shares
    # exactly one Part 1 winner and one set of Part 2 random draws (never two
    # winners, never zero). For a fallback (donor) match, the lone live
    # player's row is set independently inside finalize_singleton_outcome().
    is_fallback_match = models.BooleanField(initial=False)
    fallback_donor_id = models.StringField(blank=True)

    part1_winner = models.BooleanField(initial=False)
    p_performance = models.IntegerField(initial=0)
    performance_rule_applies = models.BooleanField(initial=False)
    random_winner = models.BooleanField(initial=False)
    part2_winner = models.BooleanField(initial=False)
    paying_part = models.IntegerField(initial=0)
    paying_winner = models.BooleanField(initial=False)


        
        # --- Comprehension questions (Part 2) ---
    cq1 = models.IntegerField(
        choices=[
            [1, 'The computer selects one of the two participants at random, giving each an equal chance.'],
            [2, 'The participant with fewer mistakes wins'],
            [3, 'The winner is randomly selected based on Part 1 scores'],
            [4, 'The participant who solved more puzzles in Part 1 wins'],
        ],
        widget=widgets.RadioSelect,
        label="<strong>Q1. How does the Random rule determine the winner?</strong>",
    )

    cq2 = models.IntegerField(
        choices=[
            [1, 'The winner is randomly selected regardless of Part 1 performance'],
            [2, 'The participant who solved more puzzles in Part 1 wins'],
            [3, 'Both participants win'],
            [4, 'The computer cancels Part 2'],
        ],
        widget=widgets.RadioSelect,
        label="<strong>Q2. If the Performance rule applies with a 100% chance, how is the winner determined?</strong>",
    )

    cq3 = models.IntegerField(
        choices=[
            [1, 'The participant who solved more puzzles in Part 1 wins'],
            [2, 'The faster participant wins'],
            [3, 'The computer selects the winner at random, regardless of Part 1 performance'],
            [4, 'No one wins'],
        ],
        widget=widgets.RadioSelect,
        label="<strong>Q3. If the chance that the Performance rule applies is 0%, how is the winner determined?</strong>",
    )

    cq4 = models.IntegerField(
        choices=[
            [1, '30'],
            [2, '100'],
            [3, '50'],
            [4, '70'],
        ],
        widget=widgets.RadioSelect,
        label="<strong>Q4. Suppose the chance that the Performance rule applies is 30%. Out of 100 similar cases, in how many cases is the winner selected at random, regardless of Part 1 performance?</strong>",
    )

    cq5 = models.IntegerField(
        choices=[
            [1, 'Yes'],
            [2, 'No'],
        ],
        widget=widgets.RadioSelect,
        label="<strong>Q5. If you solved fewer puzzles than your paired participant in Part 1, is it guaranteed that you will lose Part 2?</strong>",
    )

    comp_correct = models.IntegerField(initial=0)
    comp_bonus_amount = models.CurrencyField(initial=0)


    comp_attempts = models.IntegerField(initial=0)
    comp_first_try_recorded = models.BooleanField(initial=False)

    cq1_first_try_correct = models.BooleanField(initial=False)
    cq2_first_try_correct = models.BooleanField(initial=False)
    cq3_first_try_correct = models.BooleanField(initial=False)
    cq5_first_try_correct = models.BooleanField(initial=False)



    cq1_first_answer = models.IntegerField(blank=True)
    cq2_first_answer = models.IntegerField(blank=True)
    cq3_first_answer = models.IntegerField(blank=True)
    cq5_first_answer = models.IntegerField(blank=True)  





    # --- Beliefs ---
    belief_p_performance = models.IntegerField(
        choices=[
            [0, '0%'],
            [10, '10%'],
            [20, '20%'],
            [30, '30%'],
            [40, '40%'],
            [50, '50%'],
            [60, '60%'],
            [70, '70%'],
            [80, '80%'],
            [90, '90%'],
            [100, '100%'],
        ],
        widget=widgets.RadioSelectHorizontal,
        label="Your guess:",
    )


    true_p_performance = models.IntegerField(initial=0)
    belief_bonus_earned = models.BooleanField(initial=False)
    belief_bonus_amount = models.CurrencyField(initial=0)

    final_guess_more_puzzles = models.IntegerField(
        min=0,
        max=100,
        label="Your guess (0–100):",
    )

    # --- Webcam check (Archived/Unused) ---
    webcam_success = models.BooleanField(initial=False)
    webcam_error = models.LongStringField(blank=True)
    webcam_prompted = models.BooleanField(initial=False)



    # --- AI Check ---
    ai_check_answer = models.StringField(blank=True)
    ai_check_correct = models.BooleanField(initial=False)
    ai_check_code = models.StringField(blank=True)


def set_payoffs(player: Player):
    prize = player.prize

    won_competition = player.paying_winner

    competition_payoff = prize if won_competition else 0

    player.payoff = (
        competition_payoff
        + player.belief_bonus_amount
        + player.comp_bonus_amount
    )


DONOR_POOL_CSV_PATH = Path(__file__).resolve().parent.parent / '_static' / 'meritocracy' / 'donor_pool.csv'


@functools.lru_cache(maxsize=1)
def _load_donor_pool():
    """Read donor_pool.csv once per server process, grouped by treatment.
    Data contract: every treatment used in SESSION_CONFIGS must have >=2 rows
    here (donors are drawn with replacement)."""
    pool = {}
    with DONOR_POOL_CSV_PATH.open(newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            pool.setdefault(row['treatment'].strip(), []).append(
                dict(
                    donor_id=row['donor_id'].strip(),
                    total_correct=int(row['total_correct'].strip()),
                )
            )
    return pool


def draw_donor(treatment):
    """Randomly draw (with replacement) one donor row for `treatment`.
    Returns dict(donor_id=..., total_correct=...), or None if no donor rows
    exist for this treatment (should not happen; see data contract above)."""
    candidates = _load_donor_pool().get(treatment, [])
    if not candidates:
        return None
    return random.choice(candidates)


def _compute_total_correct(player):
    total = 0
    for pr in player.in_all_rounds():
        if pr.field_maybe_none('is_correct'):
            total += 1
    player.total_correct = total


def finalize_pair_outcome(p1: Player, p2: Player):
    """Two real live players, paired normally (group_by_arrival_time_method
    matched them by treatment). All Part 2 randomization is drawn ONCE and
    mirrored/complemented onto both rows, so the pair always shares exactly
    one designated Part 1/2 winner and one paying_part -- never two winners,
    never zero, since each draw below calls random.*() exactly once."""
    _compute_total_correct(p1)
    _compute_total_correct(p2)

    p1.other_player_total_correct = p2.total_correct
    p2.other_player_total_correct = p1.total_correct

    # Part 1 winner (ties broken by a single shared coin flip)
    if p1.total_correct > p2.total_correct:
        p1.part1_winner, p2.part1_winner = True, False
    elif p2.total_correct > p1.total_correct:
        p1.part1_winner, p2.part1_winner = False, True
    else:
        p1_wins = random.choice([True, False])
        p1.part1_winner, p2.part1_winner = p1_wins, not p1_wins

    # Part 2 mechanism: each draw happens once, then is copied/complemented
    shared_p_performance = random.choice(list(range(0, 101, 10)))
    shared_applies = random.random() < shared_p_performance / 100
    p1_random_wins = random.choice([True, False])

    for p in (p1, p2):
        p.p_performance = shared_p_performance
        p.performance_rule_applies = shared_applies
    p1.random_winner, p2.random_winner = p1_random_wins, not p1_random_wins

    for p in (p1, p2):
        p.part2_winner = p.part1_winner if p.performance_rule_applies else p.random_winner

    # Paying part: one shared draw, mirrored on both rows
    shared_paying_part = random.choice([1, 2])
    for p in (p1, p2):
        p.paying_part = shared_paying_part
        p.paying_winner = p.part1_winner if p.paying_part == 1 else p.part2_winner


def finalize_singleton_outcome(player: Player):
    """Fallback match: this live player waited too long for a same-treatment
    partner, so we compare them one-directionally against a randomly drawn
    (with replacement) donor score from the same-treatment pilot CSV. Only
    this player's own outcome is computed/stored here -- the donor's own
    (historical) outcome was already finalized in the pilot run and is
    untouched."""
    _compute_total_correct(player)
    player.is_fallback_match = True

    donor = draw_donor(player.treatment)
    if donor is None:
        # Defensive-only fallback. The CSV data contract (>=2 rows per
        # treatment in use) guarantees this doesn't happen in practice; if it
        # ever does, degrade to the existing dead-end/apology flow rather
        # than fabricate an outcome from no data.
        player.participant.timed_out = True
        return

    player.other_player_total_correct = donor['total_correct']
    player.fallback_donor_id = donor['donor_id']

    if player.total_correct > player.other_player_total_correct:
        player.part1_winner = True
    elif player.total_correct < player.other_player_total_correct:
        player.part1_winner = False
    else:
        player.part1_winner = random.choice([True, False])

    player.p_performance = random.choice(list(range(0, 101, 10)))
    player.performance_rule_applies = random.random() < player.p_performance / 100
    player.random_winner = random.choice([True, False])
    player.part2_winner = (
        player.part1_winner if player.performance_rule_applies else player.random_winner
    )

    player.paying_part = random.choice([1, 2])
    player.paying_winner = (
        player.part1_winner if player.paying_part == 1 else player.part2_winner
    )


class Consent(Page):
    form_model = 'player'
    form_fields = ['consent']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['consent_declined'] = (player.consent == 'no')

    @staticmethod
    def vars_for_template(player: Player):

        prize = player.prize
        belief_bonus = player.session.config.get('belief_bonus')

        return dict(
            participation_fee=player.session.config.get('participation_fee'),
            prize=prize,
            belief_bonus=belief_bonus,
            max_bonus=f"{prize + belief_bonus:.2f}",
        )



class ProlificID(Page):
    form_model = 'player'
    form_fields = ['prolific_id']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class ConsentDeclined(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and player.participant.vars.get('consent_declined', False)




class WelcomeToStudy(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1




class AIWarning(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1




class AICheck(Page):
    form_model = 'player'
    form_fields = ['ai_check_answer']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        player.ai_check_code = '4719'
        return dict(
            ai_check_gif='meritocracy/ai_checks/ai_check.gif'
        )

    
    @staticmethod
    def error_message(player: Player, values):
        answer = values.get('ai_check_answer', '').strip()

        if not answer.isdigit() or len(answer) != 4:
            return 'Please enter a four-digit number.'


    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        answer = player.ai_check_answer.strip()
        player.ai_check_correct = (answer == player.ai_check_code)

    
  





class InstructionsPart1(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        prize = player.prize
        return dict(
            prize_formatted=f"{prize:.2f}",
        )


class InstructionsPart1Competition(Page):
    allow_back_button = True

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        prize = player.prize
        return dict(
            prize_formatted=f"{prize:.2f}",
        )


class InstructionsPart1Timing(Page):
    allow_back_button = True

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class InstructionsPart1Start(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1



class Puzzle(Page):
    form_model = 'player'
    form_fields = ['answer', 'action']   # IMPORTANT

    timeout_seconds = 120

    @staticmethod
    def is_displayed(player: Player):
        if player.participant.timed_out:
            return False
        if player.round_number >= C.NUM_ROUNDS:
            return False
        stop_round = player.participant.vars.get('stop_round')
        if stop_round is not None and player.round_number > stop_round:
            return False
        return True

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            puzzle_image=C.PUZZLE_IMAGES[player.round_number - 1],
            round_number=player.round_number,
            num_rounds=C.NUM_ROUNDS,
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # If they clicked "Stop", remember this round
        if player.action == 'stop':
            player.stop_part1 = True
            player.participant.vars['stop_round'] = player.round_number
        else:
            player.stop_part1 = False

        # Grade this round (unanswered/timeout => incorrect)
        ans = player.field_maybe_none('answer')
        correct_answer = C.CORRECT_ANSWERS[player.round_number - 1]
        player.is_correct = (ans == correct_answer)






class InstructionsPart2(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS and not player.participant.timed_out

    @staticmethod
    def vars_for_template(player: Player):
        prize = player.prize
        return dict(
            prize_formatted=f"{prize:.2f}",
        )


class InstructionsPart2Rules(Page):
    allow_back_button = True

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS and not player.participant.timed_out

    @staticmethod
    def vars_for_template(player: Player):
        prize = player.prize
        return dict(
            prize_formatted=f"{prize:.2f}",
        )

class InstructionsPart2Probability(Page):
    allow_back_button = True

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS and not player.participant.timed_out


class InstructionsPart2Examples(Page):
    allow_back_button = True

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS and not player.participant.timed_out



class Comprehension(Page):
    form_model = 'player'
    form_fields = [
        'cq1', 'cq2', 'cq3', 'cq5',
        'cq1_first_answer', 'cq2_first_answer', 'cq3_first_answer', 'cq5_first_answer',
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS and not player.participant.timed_out

    @staticmethod
    def vars_for_template(player: Player):
        task_word = "puzzles" if player.framing == "iq" else "questions"
        return dict(task_word=task_word)

    @staticmethod
    def error_message(player: Player, values):
        errors = {}

        task_word = "puzzles" if player.framing == "iq" else "questions"

        if values['cq1'] != 1:
            errors['cq1'] = 'Incorrect. According to the Random rule, the computer selects one of the two participants at random, giving each an equal chance.'

        if values['cq2'] != 2:
            errors['cq2'] = f'Incorrect. If the Performance rule applies with a 100% chance, the participant who solved more {task_word} in Part 1 wins.'

        if values['cq3'] != 3:
            errors['cq3'] = 'Incorrect. If the Performance rule applies with a 0% chance, the computer selects the winner at random, regardless of Part 1 performance.'

        if values['cq5'] != 2:
            errors['cq5'] = f'Incorrect. If you solved fewer {task_word} than your paired participant in Part 1, you may still win in Part 2 if the Random rule applies and you are selected.'

        if errors:
            return errors

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        correct_count = 0

        player.cq1_first_try_correct = (player.cq1_first_answer == 1)
        player.cq2_first_try_correct = (player.cq2_first_answer == 2)
        player.cq3_first_try_correct = (player.cq3_first_answer == 3)
        player.cq5_first_try_correct = (player.cq5_first_answer == 2)

        correct_count += int(player.cq1_first_try_correct)
        correct_count += int(player.cq2_first_try_correct)
        correct_count += int(player.cq3_first_try_correct)
        correct_count += int(player.cq5_first_try_correct)

        player.comp_correct = correct_count
        player.comp_bonus_amount = cu(correct_count * 0.25)
        player.comp_first_try_recorded = True

        

class WaitForScoring(WaitPage):
    group_by_arrival_time = True

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS and not player.participant.timed_out

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            timeout_ms=WAIT_PAGE_TIMEOUT * 1000,
            participant_code=player.participant.code,
        )

    @staticmethod
    def after_all_players_arrive(group: Group):
        players = group.get_players()
        if len(players) == 2:
            finalize_pair_outcome(players[0], players[1])
        else:
            finalize_singleton_outcome(players[0])


class WaitTimeout(Page):
    @staticmethod
    def is_displayed(player: Player):
        return bool(player.participant.timed_out)


# ARCHIVED / UNUSED (Belief(PageO)))
# This old page refers to p_intervene and should not be used with the current mechanism.

# class Belief(Page):
#     form_model = 'player'
#     form_fields = ['belief_no_intervention']

#     @staticmethod
#     def is_displayed(player: Player):
#         return player.round_number == C.NUM_ROUNDS and not player.participant.timed_out

#     @staticmethod
#     def before_next_page(player: Player, timeout_happened):
#         # benchmark probability in percent
#         p_intervene = player.session.config['p_intervene']
#         true_no_intervention = int(round((1 - p_intervene) * 100))
#         player.true_no_intervention = true_no_intervention

#         report = player.field_maybe_none('belief_no_intervention')

#         if report is None:
#             player.belief_bonus_earned = False
#         else:
#             player.belief_bonus_earned = (abs(report - true_no_intervention) <= 5)

#         bonus = player.session.config.get('belief_bonus', 0)
#         player.belief_bonus_amount = bonus if player.belief_bonus_earned else 0









class DummyOutcome(Page):
    form_model = 'player'
    form_fields = ['belief_p_performance']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS and not player.participant.timed_out

    @staticmethod
    def vars_for_template(player: Player):
        won = player.part2_winner
        belief_bonus = player.session.config.get('belief_bonus')

        task_word = (
            "puzzles"
            if player.framing == 'iq'
            else "questions"
        )
            
        return dict(
            won=won,
            belief_bonus_formatted=f"{belief_bonus:.2f}",
            task_word=task_word,
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Store the true randomly drawn probability that the Performance rule applies
        player.true_p_performance = player.p_performance

        # Participant's guess
        report = player.field_maybe_none('belief_p_performance')

        # Bonus if the guess exactly matches the computer's drawn value
        player.belief_bonus_earned = (report == player.true_p_performance)

        bonus = player.session.config.get('belief_bonus', 0)
        player.belief_bonus_amount = bonus if player.belief_bonus_earned else 0

        set_payoffs(player)


class Part2StartScreen(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS and not player.participant.timed_out




class OutcomeCalculation(Page):

    timeout_seconds = 7

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def get_timeout_seconds(player: Player):
        return 7

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        pass






class WebcamCheck(Page):
    form_model = 'player'
    form_fields = ['webcam_success', 'webcam_error']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS and not player.participant.timed_out

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.webcam_prompted = True


class ConfidenceCheck(Page):
    form_model = 'player'
    form_fields = ['final_guess_more_puzzles']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS and not player.participant.timed_out


class End(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            comp_correct=player.comp_correct,
            comp_bonus_amount=player.comp_bonus_amount,
        )


page_sequence = [
    WaitForScoring,
    WaitTimeout,
    Consent,
    ProlificID,
    ConsentDeclined,
    AIWarning,
    AICheck,
    InstructionsPart1,
    InstructionsPart1Competition,
    InstructionsPart1Timing,
    Puzzle,
    ConfidenceCheck,
    InstructionsPart2,
    InstructionsPart2Rules,
    InstructionsPart2Probability,
    InstructionsPart2Examples,
    Comprehension,
    Part2StartScreen,
    OutcomeCalculation,
    DummyOutcome,
    # WebcamCheck,
    End,
]