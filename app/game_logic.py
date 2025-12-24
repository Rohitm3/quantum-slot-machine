class GameState:
    """
    Manages game state: credits, bets, wins
    """
    
    def __init__(self, starting_credits=100):
        """Initialize game state"""
        self.credits = starting_credits
        self.starting_credits = starting_credits
        self.bet_amount = 10
        self.total_spins = 0
        self.total_wins = 0
        self.biggest_win = 0
        
    def can_spin(self):
        """Check if player has enough credits"""
        return self.credits >= self.bet_amount
    
    def place_bet(self):
        """Deduct bet from credits"""
        if self.can_spin():
            self.credits -= self.bet_amount
            self.total_spins += 1
            return True
        return False
    
    def add_winnings(self, amount):
        """Add winnings to credits"""
        self.credits += amount
        if amount > 0:
            self.total_wins += 1
            if amount > self.biggest_win:
                self.biggest_win = amount
    
    def reset(self):
        """Reset to starting state"""
        self.credits = self.starting_credits
        self.total_spins = 0
        self.total_wins = 0
        self.biggest_win = 0
    
    def get_stats(self):
        """Get game statistics"""
        win_rate = (self.total_wins / self.total_spins * 100) if self.total_spins > 0 else 0
        return {
            'credits': self.credits,
            'total_spins': self.total_spins,
            'total_wins': self.total_wins,
            'win_rate': win_rate,
            'biggest_win': self.biggest_win,
            'net_profit': self.credits - self.starting_credits
        }


class SymbolMapper:
    """
    Maps quantum measurement results to slot symbols
    """
    
    def __init__(self, use_8_symbols=True):
        """
        Initialize symbol mapper
        
        Args:
            use_8_symbols: If True, use 8 symbols (3 qubits)
                          If False, use 2 symbols (1 qubit)
        """
        self.use_8_symbols = use_8_symbols
        
        # Simple mapping for 1-qubit (2 symbols)
        self.symbol_map_simple = {
            "0": "🍒",
            "1": "💎"
        }
        
        # Extended mapping for 3-qubits (8 symbols)
        self.symbol_map_extended = {
            "000": "🍒",  # Cherry - Common
            "001": "🍋",  # Lemon - Common
            "010": "🍊",  # Orange - Uncommon
            "011": "🍇",  # Grape - Uncommon
            "100": "🔔",  # Bell - Rare
            "101": "⭐",  # Star - Rare
            "110": "💎",  # Diamond - Very Rare
            "111": "7️⃣"   # Seven - Jackpot!
        }
        
        # Payout table (for triple matches)
        self.payout_table = {
            "🍒": 10,
            "🍋": 15,
            "🍊": 20,
            "🍇": 25,
            "🔔": 30,
            "⭐": 50,
            "💎": 100,
            "7️⃣": 200
        }
    
    def bits_to_symbol(self, bits):
        """
        Convert quantum measurement bits to symbol
        
        Args:
            bits: String of bits ("0", "1" or "000", "001", etc.)
            
        Returns:
            Symbol emoji
        """
        if self.use_8_symbols:
            return self.symbol_map_extended.get(bits, "❓")
        else:
            return self.symbol_map_simple.get(bits, "❓")
    
    def get_payout(self, symbol):
        """Get base payout for a symbol"""
        return self.payout_table.get(symbol, 0)


class WinChecker:
    """
    Checks for winning combinations
    """
    
    def __init__(self):
        self.symbol_mapper = SymbolMapper()
    
    def check_win(self, reel_results):
        """
        Check if reel results constitute a win
        
        Args:
            reel_results: List of symbols ["🍒", "💎", "🍒"]
            
        Returns:
            (win_type, payout)
        """
        # Triple match
        if reel_results[0] == reel_results[1] == reel_results[2]:
            symbol = reel_results[0]
            base_payout = self.symbol_mapper.get_payout(symbol)
            return "triple", base_payout * 3
        
        # Double match (any two)
        elif reel_results[0] == reel_results[1] or \
             reel_results[1] == reel_results[2] or \
             reel_results[0] == reel_results[2]:
            
            # Find the matching symbol
            if reel_results[0] == reel_results[1]:
                symbol = reel_results[0]
            elif reel_results[1] == reel_results[2]:
                symbol = reel_results[1]
            else:
                symbol = reel_results[0]
            
            base_payout = self.symbol_mapper.get_payout(symbol)
            return "double", max(base_payout // 2, 5)
        
        # No match
        else:
            return "none", 0
    
    def get_win_message(self, win_type, payout):
        """Generate win message"""
        if win_type == "triple":
            return f"🎉 TRIPLE MATCH! WIN {payout} CREDITS! 🎉"
        elif win_type == "double":
            return f"🎊 DOUBLE MATCH! WIN {payout} CREDITS! 🎊"
        else:
            return "Try again! 🎰"


class QuantumStateTracker:
    """
    Tracks and formats quantum state information for display
    """
    
    def __init__(self):
        self.steps = [
            "Initialized - Qubits in |0⟩ ground state",
            "Superposition - Hadamard gates applied",
            "Rotation - RY gates adjusting probabilities",
            "Entanglement - CNOT gates creating correlations",
            "Measurement - Wavefunction collapsing",
            "Oracle - Pattern matching in progress",
            "Arithmetic - Calculating payout",
            "Complete - Results ready"
        ]
    
    def get_state_message(self, step_number):
        """Get quantum state message for current step"""
        if 0 <= step_number < len(self.steps):
            return f"Step {step_number + 1}: {self.steps[step_number]}"
        return "Ready"