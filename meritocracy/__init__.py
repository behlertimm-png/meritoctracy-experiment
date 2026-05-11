from otree.api import *
import random


doc = """
Meritocracy experiment skeleton.
"""


class C(BaseConstants):
    NAME_IN_URL = 'meritocracy'
    PLAYERS_PER_GROUP = 2

    # 36 puzzles = 36 rounds
    NUM_ROUNDS = 36

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


class Group(BaseGroup):
    part1_winner = models.IntegerField()
    part2_winner = models.IntegerField()
    
    # Old fields from old part 2 mechanism, kept for now so old code/data references don't break
    selected_player = models.IntegerField()
    intervene = models.BooleanField()

    # New Part 2 mechanism
    p_performance = models.IntegerField()
    performance_rule_applies = models.BooleanField()
    random_winner = models.IntegerField()

    # To determine the payoff relevant part
    paying_part = models.IntegerField()
    paying_winner = models.IntegerField()

    def set_part1_winner(self):
        players = self.get_players()
        p1 = players[0]
        p2 = players[1]

        if p1.total_correct > p2.total_correct:
            self.part1_winner = p1.id_in_group
        elif p2.total_correct > p1.total_correct:
            self.part1_winner = p2.id_in_group
        else:
            self.part1_winner = random.choice([1, 2])


class Player(BasePlayer):
    # --- Consent Form ---

    consent = models.StringField(
    choices=[
            ['yes', 'I agree and confirm that I live in the US and am 18 years of age or older.'],
            ['no', 'I don’t agree.'],
        ],
    widget=widgets.RadioSelect,
    label="",
    )


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
    stop_part1 = models.BooleanField(initial=False)
    action = models.StringField(blank=True)


        
        # --- Comprehension questions (Part 2) ---
    cq1 = models.IntegerField(
        choices=[
            [1, 'A. The participant with fewer mistakes wins'],
            [2, 'B. The computer selects one of the two participants at random, giving each an equal chance.'],
            [3, 'C. The winner is randomly selected based on Part 1 scores'],
            [4, 'D. The participant who solved more puzzles in Part 1 wins'],
        ],
        widget=widgets.RadioSelect,
        label="Q1. How does the Random rule determine the winner?",
    )

    cq2 = models.IntegerField(
        choices=[
            [1, 'A. The winner is randomly selected regardless of Part 1 performance'],
            [2, 'B. The participant who solved more puzzles in Part 1 wins'],
            [3, 'C. Both participants win'],
            [4, 'D. The computer cancels Part 2'],
        ],
        widget=widgets.RadioSelect,
        label="Q2. If the Performance rule applies with a 100% chance, how is the winner determined?",
    )

    cq3 = models.IntegerField(
        choices=[
            [1, 'A. The participant who solved more puzzles in Part 1 wins'],
            [2, 'B. The computer selects the winner at random, regardless of Part 1 performance'],
            [3, 'C. The faster participant wins'],
            [4, 'D. No one wins'],
        ],
        widget=widgets.RadioSelect,
        label="Q3. If the chance that the Performance rule applies is 0%, how is the winner determined?",
    )

    cq4 = models.IntegerField(
        choices=[
            [1, 'A. 30'],
            [2, 'B. 70'],
            [3, 'C. 50'],
            [4, 'D. 100'],
        ],
        widget=widgets.RadioSelect,
        label="Q4. Suppose the chance that the Performance rule applies is 30%. Out of 100 similar cases, in how many cases is the winner selected at random, regardless of Part 1 performance?",
    )

    cq5 = models.IntegerField(
        choices=[
            [1, 'A. Yes'],
            [2, 'B. No'],
        ],
        widget=widgets.RadioSelect,
        label="Q5. If you solved fewer puzzles than your paired participant in Part 1, is it guaranteed that you will lose Part 2?",
    )

    comp_correct = models.IntegerField(initial=0)
    comp_bonus_amount = models.CurrencyField(initial=0)

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

    # --- Webcam check ---
    webcam_success = models.BooleanField(initial=False)
    webcam_error = models.LongStringField(blank=True)
    webcam_prompted = models.BooleanField(initial=False)



def set_payoffs(player: Player):
    prize = player.session.config.get('prize', 0)

    won_competition = player.id_in_group == player.group.paying_winner

    competition_payoff = prize if won_competition else 0

    player.payoff = (
    competition_payoff
    + player.belief_bonus_amount
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

        prize = player.session.config.get('prize')
        belief_bonus = player.session.config.get('belief_bonus')

        return dict(
            participation_fee=player.session.config.get('participation_fee'),
            prize=prize,
            belief_bonus=belief_bonus,
            max_bonus=f"{prize + belief_bonus:.2f}",
        )



class ConsentDeclined(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1 and player.participant.vars.get('consent_declined', False)




class WelcomeToStudy(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class InstructionsPart1(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        prize = player.session.config.get('prize')
        return dict(
            prize_formatted=f"{prize:.2f}",
        )


class InstructionsPart1Start(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1



class Puzzle(Page):
    form_model = 'player'
    form_fields = ['answer', 'action']   # IMPORTANT

    timeout_seconds = 60

    @staticmethod
    def is_displayed(player: Player):
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
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        prize = player.session.config.get('prize')
        return dict(
            prize_formatted=f"{prize:.2f}",
        )


class Comprehension(Page):
    form_model = 'player'
    form_fields = ['cq1', 'cq2', 'cq3', 'cq4', 'cq5']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def error_message(player: Player, values):
        errors = {}

        if values['cq1'] != 2:
            errors['cq1'] = 'Incorrect. The correct answer is B: The computer selects one of the two participants at random, giving each an equal chance.'

        if values['cq2'] != 2:
            errors['cq2'] = 'Incorrect. The correct answer is B: The participant who solved more puzzles in Part 1 wins.'

        if values['cq3'] != 2:
            errors['cq3'] = 'Incorrect. The correct answer is B: The computer selects the winner at random, regardless of Part 1 performance.'

        if values['cq4'] != 2:
            errors['cq4'] = 'Incorrect. The correct answer is B: 70.'

        if values['cq5'] != 2:
            errors['cq5'] = 'Incorrect. The correct answer is B: No.'

        if errors:
            return errors

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.comp_correct = 5
        player.comp_bonus_amount = 0



class WaitForScoring(WaitPage):

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def after_all_players_arrive(group: Group):
        # 1) compute totals once, after both players finished all rounds
        for p in group.get_players():
            total = 0
            for pr in p.in_all_rounds():
                if pr.field_maybe_none('is_correct'):
                    total += 1
            p.total_correct = total

        # 2) determine Part 1 winner (tie-break handled inside set_part1_winner)
        group.set_part1_winner()

        # 3) Part 2 mechanism (NEW)

        # Step 1: draw p_performance from {0,10,...,100}
        group.p_performance = random.choice(list(range(0, 101, 10)))

        # Step 2: draw whether Performance rule applies
        group.performance_rule_applies = (random.random() < group.p_performance / 100)

        # Step 3: draw random winner (for Random rule)
        group.random_winner = random.choice([1, 2])

        # Step 4: determine final winner
        if group.performance_rule_applies:
            group.part2_winner = group.part1_winner
        else:
            group.part2_winner = group.random_winner

        # 4) FINAL STEP: randomly select which part is payoff-relevant
        group.paying_part = random.choice([1, 2])

        if group.paying_part == 1:
            group.paying_winner = group.part1_winner
        else:
            group.paying_winner = group.part2_winner


# ARCHIVED / UNUSED (Belief(PageO)))
# This old page refers to p_intervene and should not be used with the current mechanism.

class Belief(Page):
    form_model = 'player'
    form_fields = ['belief_no_intervention']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # benchmark probability in percent
        p_intervene = player.session.config['p_intervene']
        true_no_intervention = int(round((1 - p_intervene) * 100))
        player.true_no_intervention = true_no_intervention

        report = player.field_maybe_none('belief_no_intervention')

        if report is None:
            player.belief_bonus_earned = False
        else:
            player.belief_bonus_earned = (abs(report - true_no_intervention) <= 5)

        bonus = player.session.config.get('belief_bonus', 0)
        player.belief_bonus_amount = bonus if player.belief_bonus_earned else 0



class DummyOutcome(Page):
    form_model = 'player'
    form_fields = ['belief_p_performance']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        won = (player.id_in_group == player.group.part2_winner)
        belief_bonus = player.session.config.get('belief_bonus')
            
        return dict(
            won=won,
            belief_bonus_formatted=f"{belief_bonus:.2f}",
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Store the true randomly drawn probability that the Performance rule applies
        player.true_p_performance = player.group.p_performance

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
        return player.round_number == C.NUM_ROUNDS


class WebcamCheck(Page):
    form_model = 'player'
    form_fields = ['webcam_success', 'webcam_error']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.webcam_prompted = True


class FinalGuess(Page):
    form_model = 'player'
    form_fields = ['final_guess_more_puzzles']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS


class End(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS


page_sequence = [
    Consent,
    ConsentDeclined,
    InstructionsPart1,
    Puzzle,
    InstructionsPart2,
    Comprehension,
    Part2StartScreen,
    WaitForScoring,
    DummyOutcome,
    FinalGuess,
    # WebcamCheck,
    End,
]