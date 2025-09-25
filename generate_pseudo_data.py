import random
import pandas as pd
from typing import List, Any, Tuple
from datetime import datetime, timedelta

from utils import Constants # Import Constants from utils

# --- Constants for Game Simulation ---
SESSION_CHANCE = 0.6
ASSISTED_GOAL_CHANCE = 0.10
INJURY_CHANCE = 0.03
MIN_DRILL_MINUTES = 20
MAX_DRILL_MINUTES = 60
MIN_GAME_MINUTES = 45
MAX_GAME_MINUTES = 90
MIN_SCORE = 0
MAX_SCORE = 5
MIN_NORMAL_GAME_PLAYERS = 4
MAX_NORMAL_GAME_PLAYERS = 11
MIN_REAL_GAME_PLAYERS = 7
MAX_REAL_GAME_PLAYERS = 11
GOAL_ASSIGNMENT_OFFSET = 2

# --- Game Type Strings ---
DRILL_GAME_TYPE = "Drill"
NORMAL_GAME_TYPE = "Normal Game"
REAL_GAME_TYPE = "Real Game"
NO_OPPONENT_NAME = "N/A"
INTERNAL_OPPONENT_NAME = "NFT Weingarten"

# --- Date Formats ---
INPUT_DATE_FORMAT = "%Y-%m-%d"
OUTPUT_DATE_FORMAT = "%m/%d/%Y"

# --- Player and Opponent Names ---
NFT_WEINGARTEN_PLAYERS: List[str] = [
    "Alice Smith", "Bob Johnson", "Charlie Brown", "Diana Prince", "Eve Adams",
    "Frank White", "Grace Lee", "Harry Davis", "Ivy King", "Jack Wilson",
    "Karen Green", "Liam Hall", "Mia Clark", "Noah Lewis", "Olivia Scott",
    "Peter Young", "Quinn Hill", "Rachel Ward", "Sam Baker", "Tina Moore",
    "Ursula Vance", "Victor Stone"
]
NFT_WEINGARTEN_KEEPERS: List[str] = ["Zoe Adams", "Yara Singh"]
OPPONENT_NAMES: List[str] = ["Weingarten", "Stuttgart", "Munich", "Dresden", "Berlin", "Koln"]

def _handle_drill_game_type() -> Tuple[List[str], str, int, int, List[str], List[str]]:
    """
    Handles the logic for 'Drill' game type.
    Returns players to generate data for, opponent name, team score, opponent score, and empty scoring player lists.
    """
    max_nft_weingarten_participants = len(NFT_WEINGARTEN_PLAYERS) + len(NFT_WEINGARTEN_KEEPERS)
    num_participants = random.randint(3, max_nft_weingarten_participants)
    
    all_nft_weingarten_participants = NFT_WEINGARTEN_PLAYERS + NFT_WEINGARTEN_KEEPERS
    players_to_generate_data_for = random.sample(all_nft_weingarten_participants, num_participants)
    
    session_opponent_name = NO_OPPONENT_NAME
    session_team_score = MIN_SCORE
    session_opponent_score = MIN_SCORE
    return players_to_generate_data_for, session_opponent_name, session_team_score, session_opponent_score, [], []

def _handle_normal_game_type(session_team_score: int, session_opponent_score: int) -> Tuple[List[str], str, List[str], List[str], List[str], List[str]]:
    """
    Handles the logic for 'Normal Game' type.
    Returns players to generate data for, opponent name, scoring player lists for team A and B,
    and participants for team A and B.
    """
    session_opponent_name = INTERNAL_OPPONENT_NAME

    X = random.randint(MIN_NORMAL_GAME_PLAYERS, MAX_NORMAL_GAME_PLAYERS)
    possible_Y = [val for val in [X-1, X, X+1] if MIN_NORMAL_GAME_PLAYERS <= val <= MAX_NORMAL_GAME_PLAYERS]
    Y = random.choice(possible_Y)

    total_players_needed = X + Y + 2
    all_nft_weingarten_participants = NFT_WEINGARTEN_PLAYERS + NFT_WEINGARTEN_KEEPERS
    
    if total_players_needed > len(all_nft_weingarten_participants):
        available_players_count = len(NFT_WEINGARTEN_PLAYERS)
        if available_players_count < X + Y:
            X = min(X, available_players_count // 2)
            Y = min(Y, available_players_count - X)

    available_nft_players_for_selection = list(NFT_WEINGARTEN_PLAYERS)
    available_nft_keepers_for_selection = list(NFT_WEINGARTEN_KEEPERS)

    team_a_keeper = random.sample(available_nft_keepers_for_selection, 1)
    available_nft_keepers_for_selection = [k for k in available_nft_keepers_for_selection if k not in team_a_keeper]

    team_a_players = random.sample(available_nft_players_for_selection, X)
    available_nft_players_for_selection = [p for p in available_nft_players_for_selection if p not in team_a_players]

    team_b_keeper = random.sample(available_nft_keepers_for_selection, 1)
    team_b_players = random.sample(available_nft_players_for_selection, Y)

    nft_weingarten_team_a_participants = team_a_players + team_a_keeper
    nft_weingarten_team_b_participants = team_b_players + team_b_keeper

    players_to_generate_data_for = nft_weingarten_team_a_participants + nft_weingarten_team_b_participants

    num_goals_to_assign_a = random.randint(max(MIN_SCORE, session_team_score - GOAL_ASSIGNMENT_OFFSET), session_team_score)
    scoring_players_team_a = random.sample(nft_weingarten_team_a_participants, num_goals_to_assign_a)

    num_goals_to_assign_b = random.randint(max(MIN_SCORE, session_opponent_score - GOAL_ASSIGNMENT_OFFSET), session_opponent_score)
    scoring_players_team_b = random.sample(nft_weingarten_team_b_participants, num_goals_to_assign_b)

    return players_to_generate_data_for, session_opponent_name, scoring_players_team_a, scoring_players_team_b, nft_weingarten_team_a_participants, nft_weingarten_team_b_participants

def _handle_real_game_type(session_team_score: int, session_opponent_score: int) -> Tuple[List[str], str, List[str]]:
    """
    Handles the logic for 'Real Game' type.
    Returns players to generate data for, opponent name, and scoring players for NFT Weingarten.
    """
    session_opponent_name = random.choice(OPPONENT_NAMES)

    X = random.randint(MIN_REAL_GAME_PLAYERS, MAX_REAL_GAME_PLAYERS)
    
    nft_weingarten_team_players = random.sample(NFT_WEINGARTEN_PLAYERS, X - 1)
    nft_weingarten_team_keepers = random.sample(NFT_WEINGARTEN_KEEPERS, 1)
    
    players_to_generate_data_for = nft_weingarten_team_players + nft_weingarten_team_keepers

    num_goals_to_assign = random.randint(max(MIN_SCORE, session_team_score - GOAL_ASSIGNMENT_OFFSET), session_team_score)
    scoring_players_nft_weingarten = random.sample(players_to_generate_data_for, num_goals_to_assign)

    return players_to_generate_data_for, session_opponent_name, scoring_players_nft_weingarten

def generate_pseudo_data(start_date: str = "2024-01-01", end_date: str = "2024-12-31", sessions_per_player_per_day: int = 1) -> pd.DataFrame:
    """
    Generates pseudo data for player performance and attendance in football games/training sessions.

    Args:
        start_date (str): The start date for the data in 'INPUT_DATE_FORMAT' format.
        end_date (str): The end date for the data in 'INPUT_DATE_FORMAT' format.
        sessions_per_player_per_day (int): Number of sessions each player participates in per day (if attended).

    Returns:
        pd.DataFrame: A DataFrame containing the generated pseudo data.
    """



    data_list: List[List[Any]] = []
    start_dt: datetime = datetime.strptime(start_date, INPUT_DATE_FORMAT)
    end_dt: datetime = datetime.strptime(end_date, INPUT_DATE_FORMAT)

    all_dates: List[datetime] = [start_dt + timedelta(days=i) for i in range((end_dt - start_dt).days + 1)]

    # Simulate game/training days (e.g., 3-5 days a week)
    game_dates: List[datetime] = []
    for current_date in all_dates:
        if random.random() < SESSION_CHANCE:  # ~60% chance of a session on any given day
            game_dates.append(current_date)

    for current_date in game_dates:
        session_game_type = random.choice(Constants.GAME_TYPES)

        session_opponent_name = NO_OPPONENT_NAME
        session_team_score = random.randint(MIN_SCORE, MAX_SCORE)
        session_opponent_score = random.randint(MIN_SCORE, MAX_SCORE)

        if session_game_type == DRILL_GAME_TYPE:
            players_to_generate_data_for, session_opponent_name, session_team_score, session_opponent_score, scoring_players_team_a, scoring_players_team_b = _handle_drill_game_type()
            scoring_players_nft_weingarten = [] # Drills don't have NFT Weingarten scoring players in this context
            nft_weingarten_team_a_participants = [] # Not applicable for drills
            nft_weingarten_team_b_participants = [] # Not applicable for drills

        elif session_game_type == NORMAL_GAME_TYPE:
            players_to_generate_data_for, session_opponent_name, scoring_players_team_a, scoring_players_team_b, nft_weingarten_team_a_participants, nft_weingarten_team_b_participants = _handle_normal_game_type(session_team_score, session_opponent_score)
            scoring_players_nft_weingarten = [] # Not applicable for normal games in this context

        elif session_game_type == REAL_GAME_TYPE:
            players_to_generate_data_for, session_opponent_name, scoring_players_nft_weingarten = _handle_real_game_type(session_team_score, session_opponent_score)
            scoring_players_team_a = [] # Not applicable for real games in this context
            scoring_players_team_b = [] # Not applicable for real games in this context
            nft_weingarten_team_a_participants = players_to_generate_data_for # All generated players are NFT Weingarten
            nft_weingarten_team_b_participants = [] # Not applicable for real games


        # Now iterate through the players for whom we need to generate data
        for player in players_to_generate_data_for:
            for _ in range(sessions_per_player_per_day):                
                minutes_played = 0
                goal_scored = False
                assisted_goal = False
                in_winning_team = False
                got_injured = False

                is_nft_weingarten_main_team_player = (session_game_type == DRILL_GAME_TYPE) or \
                                                     (session_game_type == REAL_GAME_TYPE) or \
                                                     (session_game_type == NORMAL_GAME_TYPE and player in nft_weingarten_team_a_participants)
                is_nft_weingarten_opponent_team_player = (session_game_type == NORMAL_GAME_TYPE and player in nft_weingarten_team_b_participants)

                # Generate detailed stats
                minutes_played = random.randint(MIN_GAME_MINUTES, MAX_GAME_MINUTES) if session_game_type != DRILL_GAME_TYPE else random.randint(MIN_DRILL_MINUTES, MAX_DRILL_MINUTES)
                # Goal scored logic based on new requirements
                if session_game_type == NORMAL_GAME_TYPE:
                    goal_scored = (player in scoring_players_team_a) or (player in scoring_players_team_b)
                    assisted_goal = random.uniform(0.0, 1.0) <= ASSISTED_GOAL_CHANCE
                elif session_game_type == REAL_GAME_TYPE:
                    goal_scored = player in scoring_players_nft_weingarten
                    assisted_goal = random.uniform(0.0, 1.0) <= ASSISTED_GOAL_CHANCE
                
                got_injured = random.uniform(0.0, 1.0) <= INJURY_CHANCE

                in_winning_team = False
                if session_game_type != DRILL_GAME_TYPE:
                    if is_nft_weingarten_main_team_player:
                        in_winning_team = session_team_score > session_opponent_score
                    elif is_nft_weingarten_opponent_team_player:
                        in_winning_team = session_opponent_score > session_team_score

                row_data = [
                    current_date.strftime(OUTPUT_DATE_FORMAT), # DATE_COL
                    player, # PLAYER_NAME_COL
                    minutes_played, # MINUTES_PLAYED_COL
                    goal_scored, # GOAL_SCORED_COL
                    assisted_goal, # ASSISTED_GOAL_COL
                    in_winning_team, # IN_WINNING_TEAM_COL
                    session_game_type, # GAME_TYPE_COL
                    got_injured, # GOT_INJURED_COL
                    session_opponent_name, # OPPONENT_NAME_COL
                    session_team_score, # TEAM_SCORE_COL
                    session_opponent_score, # OPPONENT_SCORE_COL
                ]
                
                data_list.append(row_data)

    columns = [
        Constants.DATE_COL,
        Constants.PLAYER_NAME_COL,
        Constants.MINUTES_PLAYED_COL,
        Constants.GOAL_SCORED_COL,
        Constants.ASSISTED_GOAL_COL,
        Constants.IN_WINNING_TEAM_COL,
        Constants.GAME_TYPE_COL,
        Constants.GOT_INJURED_COL,
        Constants.OPPONENT_NAME_COL,
        Constants.TEAM_SCORE_COL,
        Constants.OPPONENT_SCORE_COL,
    ]

    df = pd.DataFrame(data_list, columns=columns)
    return df

if __name__ == "__main__":
    # Example usage:
    pseudo_df: pd.DataFrame = generate_pseudo_data(start_date="2023-01-01", end_date="2025-12-31", sessions_per_player_per_day=1)
    
    # Save to CSV
    output_path: str = Constants.PSEUDO_DATA_OUTPUT_PATH
    pseudo_df.to_csv(output_path, index=False)
    print(f"Generated {len(pseudo_df)} records and saved to {output_path}")
