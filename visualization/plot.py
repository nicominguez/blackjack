import matplotlib.pyplot as plt
from executables.simulation import run_simulation
from src.player import *


def plot_bankroll_history(bankroll_history: list):
    """Plots player's bankroll throughout simulation."""
    plt.figure(figsize=(12, 6))
    x = range(len(bankroll_history))
    y = bankroll_history
    plt.plot(x, y, label="Bankroll")
    min_val, max_val = min(y), max(y)
    plt.axhline(
        min_val, color="red", linestyle="--", linewidth=1, label=f"min = {min_val}"
    )
    plt.axhline(
        max_val, color="green", linestyle="--", linewidth=1, label=f"max = {max_val}"
    )
    plt.xlabel("Hands Played")
    plt.ylabel("Bankroll")
    plt.title("Player Bankroll Throughout Simulation")
    plt.grid(True)
    plt.legend()
    plt.show()


def main():
    bh = run_simulation(num_hands=10000, bet_amount=5)[5]
    plot_bankroll_history(bh)


if __name__ == "__main__":
    main()
