import math

from app.game_logic import GameState
from app.quantum_logic import QuantumSlotMachine


def test_game_state_bets_and_reset():
    game = GameState()
    for _ in range(10):
        assert game.place_bet()
    assert game.credits == 0
    assert not game.can_spin()
    assert not game.place_bet()
    assert game.total_spins == 10
    game.reset()
    assert game.credits == 100
    assert game.total_spins == 0
    assert game.total_wins == 0


def test_winnings_and_statistics():
    game = GameState()
    assert game.place_bet()
    game.add_winnings(20)
    stats = game.get_stats()
    assert stats["credits"] == 110
    assert stats["total_wins"] == 1
    assert stats["high_score"] == 20
    assert stats["net_profit"] == 10


def test_classical_payout_rules():
    slot = QuantumSlotMachine()
    assert slot.check_win(["🍒", "🍒", "🍒"]) == ("triple", 20)
    assert slot.check_win(["💎", "💎", "🍋"]) == ("double", 100)
    assert slot.check_win(["🍒", "🍋", "🍊"]) == ("none", 0)


def test_normal_circuit_has_measurements():
    slot = QuantumSlotMachine(entangle=False)
    circuit = slot.build_spin_circuit(variation_pct=0)
    assert circuit.num_qubits == 9
    assert circuit.num_clbits == 9
    assert circuit.count_ops().get("measure") == 9


def test_oracle_flag_matches_three_equal_reels():
    slot = QuantumSlotMachine()
    for _ in range(5):
        result, win_type, payout = slot.run_spin_with_oracle_demo()
        assert result.oracle_flag == ("1" if len(set(result.reels)) == 1 else "0")
        assert (win_type, payout) == slot.check_win(result.reels)


def test_oracle_variation_changes_rotation_angles():
    slot = QuantumSlotMachine()
    # Control the simulator-produced perturbation bits to test variation
    # without relying on probabilistic outcomes.
    bits = iter([1, 0, 1])
    slot._get_quantum_random_bit = lambda: next(bits)
    result, _, _ = slot.run_spin_with_oracle_demo(
        angle_val=math.pi / 2, variation_pct=20
    )
    rotations = [
        float(inst.operation.params[0])
        for inst in result.circuit.data
        if inst.operation.name == "ry"
    ]
    assert len(rotations) == 3
    assert math.isclose(rotations[0], math.pi * 0.6)
    assert math.isclose(rotations[1], math.pi * 0.4)
    assert math.isclose(rotations[2], math.pi * 0.6)
