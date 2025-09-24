import matplotlib.pyplot as plt
from simulation import run_simulation

def plot_bankroll_history(bankroll_history: list):
    """Plots player's bankroll throughout simulation."""
    plt.figure(figsize=(12, 6))
    plt.plot(range(len(bankroll_history)), bankroll_history)
    plt.xlabel("Hands Played")
    plt.ylabel("Bankroll")
    plt.title("Player Bankroll Throughout Simulation")
    plt.grid(True)
    plt.show()

def main():
    bh = run_simulation(num_hands=1000, bet_amount=5)[5]
    plot_bankroll_history(bh)

if __name__ == "__main__":
    main()