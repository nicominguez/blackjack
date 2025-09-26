import matplotlib.pyplot as plt
from simulation import run_simulation
from player import *

def plot_bankroll_histories(bankroll_histories: list, labels: list):
    """Plots multiple players' bankrolls throughout the simulation."""
    plt.figure(figsize=(12, 6))

    for bh, label in zip(bankroll_histories, labels):
        x = range(len(bh))
        plt.plot(x, bh, label=label)
    
    plt.xlabel("Hands Played")
    plt.ylabel("Bankroll")
    plt.title("Player Bankrolls Throughout Simulation")
    plt.grid(True)
    plt.legend()
    plt.show()

def main():
    num_hands = 10000
    bet_amount = 5

    # Run simulations
    bh_rand = run_simulation(p=RandomStrategyPlayer(), num_hands=num_hands, bet_amount=bet_amount)[5]
    bh_basic = run_simulation(p=BasicStrategyPlayer(), num_hands=num_hands, bet_amount=bet_amount)[5]
    bh_chart1 = run_simulation(p=ChartPlayer1(), num_hands=num_hands, bet_amount=bet_amount)[5]
    bh_chart2 = run_simulation(p=ChartPlayer2(), num_hands=num_hands, bet_amount=bet_amount)[5]

    # Plot all bankroll histories
    plot_bankroll_histories(
        bankroll_histories=[bh_rand, bh_basic, bh_chart1, bh_chart2],
        labels=["Random", "Only Hit/Stand", "Basic Strategy", "Perfect Strategy"]
    )

if __name__ == "__main__":
    main()
