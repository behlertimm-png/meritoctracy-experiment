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
    final_winner = models.IntegerField()
    selected_player = models.IntegerField()
    intervene = models.BooleanField()


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
            [1, 'A. Only you'],
            [2, 'B. Only the other participant'],
            [3, 'C. Either you or the other participant, with equal chance'],
            [4, 'D. The person who did better in Part 1'],
        ],
        widget=widgets.RadioSelect,
        label="Q1. Who does the computer randomly select in Part 2?",
    )

    cq2 = models.IntegerField(
        choices=[
            [1, 'A. The computer checks who solved more puzzles in Part 1'],
            [2, 'B. The computer randomly chooses the winner based on Part 1 scores'],
            [3, 'C. The computer declares the randomly selected person the winner, regardless of Part 1 performance'],
            [4, 'D. The computer cancels Part 2'],
        ],
        widget=widgets.RadioSelect,
        label="Q2. What does it mean when the computer “intervenes” in Part 2?",
    )

    cq3 = models.IntegerField(
        choices=[
            [1, 'A. The person selected by computer'],
            [2, 'B. The person who solved more puzzles in Part 1'],
            [3, 'C. The person who solved more puzzles in Part 2'],
            [4, 'D. No one wins'],
        ],
        widget=widgets.RadioSelect,
        label="Q3. Suppose the computer does not intervene. Who wins Part 2?",
    )

    cq4 = models.IntegerField(
        choices=[
            [1, 'A. Yes'],
            [2, 'B. No'],
        ],
        widget=widgets.RadioSelect,
        label="Q4. If you solved fewer puzzles than your partner in Part 1, is it guaranteed that you will lose Part 2?",
    )

    comp_correct = models.IntegerField(initial=0)
    comp_bonus_amount = models.CurrencyField(initial=0)

    # --- Beliefs ---
    belief_no_intervention = models.IntegerField(
     min=0,
     max=100,
    label="Your guess (0–100):",
)


    

    true_no_intervention = models.IntegerField(initial=0)
    belief_bonus_earned = models.BooleanField(initial=False)
    belief_bonus_amount = models.CurrencyField(initial=0)


    # --- Webcam check ---
    webcam_success = models.BooleanField(initial=False)
    webcam_error = models.LongStringField(blank=True)
    webcam_prompted = models.BooleanField(initial=False)



class Consent(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            participation_fee=player.session.config.get('participation_fee'),
            prize=player.session.config.get('prize'),
            bonus_cap=player.session.config.get('bonus_cap'),
            comp_pay_per_correct=player.session.config.get('comp_pay_per_correct'),
            belief_bonus=player.session.config.get('belief_bonus'),
        )


class WelcomeToStudy(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class InstructionsPart1(Page):
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



class Comprehension(Page):
    form_model = 'player'
    form_fields = ['cq1', 'cq2', 'cq3', 'cq4']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        correct = 0

        # Correct answers to Q1-Q4:
        # Q1: C (either you or other, equal chance) -> option 3
        if player.cq1 == 3:
            correct += 1

        # Q2: C (selected person wins regardless of Part 1) -> option 3
        if player.cq2 == 3:
            correct += 1

        # Q3: B (Part 1 better performer wins) -> option 2
        if player.cq3 == 2:
            correct += 1

        # Q4: No (not guaranteed, because intervention could make you win) -> option 2
        if player.cq4 == 2:
            correct += 1

        player.comp_correct = correct

        pay_per_correct = player.session.config.get('comp_pay_per_correct', 0)
        player.comp_bonus_amount = correct * pay_per_correct





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

        # 3) Part 2 mechanism
        # randomly select one of the two players (50/50)
        group.selected_player = random.choice([1, 2])

        # draw whether the computer intervenes
        p_intervene = group.session.config['p_intervene']
        group.intervene = (random.random() < p_intervene)

        # determine final winner
        if group.intervene:
            group.final_winner = group.selected_player
        else:
            group.final_winner = group.part1_winner




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
    form_fields = ['belief_no_intervention']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        won = (player.id_in_group == player.group.final_winner)
        return dict(won=won)

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


class WebcamCheck(Page):
    form_model = 'player'
    form_fields = ['webcam_success', 'webcam_error']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.webcam_prompted = True



class End(Page):

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS





page_sequence = [
    Consent,
    WelcomeToStudy,
    InstructionsPart1,
    InstructionsPart1Start,
    Puzzle,
    InstructionsPart2,
    Comprehension,
    WaitForScoring,
    DummyOutcome,
    WebcamCheck,
    End,
]