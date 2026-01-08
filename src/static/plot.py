import matplotlib.pyplot as plt


def plot_bankroll_histories(bankroll_histories: list[list[int]], labels: list[str]):
    plt.figure(figsize=(12, 6))

    for bh, label in zip(bankroll_histories, labels):
        x = range(len(bh))
        plt.plot(x, bh, label=label)

    min_val = min(min(bh) for bh in bankroll_histories)
    max_val = max(max(bh) for bh in bankroll_histories)

    plt.axhline(
        min_val, color="red", linestyle="--", linewidth=1, label=f"min = {min_val}"
    )
    plt.axhline(
        max_val, color="green", linestyle="--", linewidth=1, label=f"max = {max_val}"
    )
    plt.xlabel("Hands Played")
    plt.ylabel("Bankroll")
    plt.title("Player Bankrolls Throughout Simulation")
    plt.grid(True)
    plt.legend()
    plt.show()

def plot_cumulative_winrates(cumulative_winrates: list[list[float]], labels: list[str]):
    plt.figure(figsize=(12, 6))

    for wr, label in zip(cumulative_winrates, labels):
        x = range(len(wr))
        plt.plot(x, wr, label=label)

    min_val = min(min(wr) for wr in cumulative_winrates)
    max_val = max(max(wr) for wr in cumulative_winrates)

    plt.axhline(
        min_val, color="red", linestyle="--", linewidth=1, label=f"min = {min_val}"
    )
    plt.axhline(
        max_val, color="green", linestyle="--", linewidth=1, label=f"max = {max_val}"
    )
    plt.xlabel("Hands Played")
    plt.ylabel("Cumulative Winrate")
    plt.title("Player Winrate Throughout Simulation")
    plt.grid(True)
    plt.legend()
    plt.show()
