from __future__ import annotations
from dataclasses import dataclass

@dataclass
class GameState:
    """
    Tracks credits and simple stats.
    """
    starting_credits: int = 100
    bet_amount: int = 10

    credits: int = 100
    total_spins: int = 0
    total_wins: int = 0
    biggest_win: int = 0

    def __post_init__(self):
        self.credits = self.starting_credits

    def can_spin(self) -> bool:
        return self.credits >= self.bet_amount

    def place_bet(self) -> bool:
        if not self.can_spin():
            return False
        self.credits -= self.bet_amount
        self.total_spins += 1
        return True

    def add_winnings(self, amount: int) -> None:
        self.credits += amount
        if amount > 0:
            self.total_wins += 1
            self.biggest_win = max(self.biggest_win, amount)

    def reset(self) -> None:
        self.credits = self.starting_credits
        self.total_spins = 0
        self.total_wins = 0
        self.biggest_win = 0

    def get_stats(self) -> dict:
        win_rate = (self.total_wins / self.total_spins * 100) if self.total_spins else 0.0
        return {
            "credits": self.credits,
            "total_spins": self.total_spins,
            "total_wins": self.total_wins,
            "win_rate": win_rate,
            "biggest_win": self.biggest_win,
            "net_profit": self.credits - self.starting_credits,
        }
