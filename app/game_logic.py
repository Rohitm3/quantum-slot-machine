class GameState:

    def __init__(self):

        # setting up some default values for the start of the game
        self.starting_credits: int = 100 
        self.bet_amount: int = 10  

        self.credits: int = 100 
        self.total_spins: int = 0
        self.total_wins: int = 0
        self.high_score: int = 0

    def __post_init__(self):
        self.credits = self.starting_credits

    
    def can_spin(self) -> bool:
        return self.credits >= self.bet_amount # returns true if we aren't broke yet

    def place_bet(self) -> bool:
        if not self.can_spin():
            return False
        # pay the 10 credits to play
        self.credits -= self.bet_amount
        self.total_spins += 1
        return True


    def add_winnings(self, amount: int) -> None: # add the prize money back to our total balance
        self.credits += amount
        if amount > 0:
            self.total_wins += 1
            # keep track of the high score
            self.high_score = max(self.high_score, amount)

    def reset(self) -> None:    #rest everything
        self.credits = self.starting_credits
        self.total_spins = 0
        self.total_wins = 0
        self.high_score = 0

    def get_stats(self) -> dict:
        # sidebar metrics calculation
        win_rate = (self.total_wins / self.total_spins * 100) if self.total_spins else 0.0
        return {
            "credits": self.credits,
            "total_spins": self.total_spins,
            "total_wins": self.total_wins,
            "win_rate": win_rate,
            "high_score": self.high_score,
            "net_profit": self.credits - self.starting_credits,
        }