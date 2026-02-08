from src.player import QLearningPlayer
from src.game import Game
from src.rules import HouseRules
import time


def train_q_learning_player(
    num_episodes: int = 100000,
    base_bet: int = 5,
    save_path: str = "_models/q_learning_player.pkl",
    verbose: bool = True
):

    print("=" * 60)
    print("Q-LEARNING BLACKJACK TRAINER")
    print("=" * 60)
    print(f"Training episodes: {num_episodes:,}")
    print(f"Base bet: ${base_bet}")
    print(f"Learning rate (α): 0.1")
    print(f"Discount factor (γ): 0.95")
    print(f"Exploration rate (ε): 0.3 → 0.05 (decaying)")
    print("=" * 60)
    print()

    player = QLearningPlayer(
        bankroll=10000,
        learning_rate=0.1,
        discount_factor=0.95,
        epsilon=0.3,
        training_mode=True
    )

    rules = HouseRules()
    game = Game(player=player, rules=rules, bet=base_bet)

    wins, losses, pushes = 0, 0, 0
    start_time = time.time()

    for episode in range(num_episodes):

        if episode < num_episodes * 0.5:
            player.epsilon = 0.3
        elif episode < num_episodes * 0.8:
            player.epsilon = 0.15
        else:
            player.epsilon = 0.05

        outcome = game.play_round()

        outcome_type = outcome.get("outcome")
        player.learn_from_hand(outcome_type)

        if outcome_type in ["win", "blackjack"]:
            wins += 1
        elif outcome_type in ["loss", "surr_loss"]:
            losses += 1
        elif outcome_type == "push":
            pushes += 1
        elif outcome_type == "broke":
            player.bankroll = 10000

        if verbose and (episode + 1) % 10000 == 0:
            total_games = wins + losses + pushes
            win_rate = (wins / total_games * 100) if total_games > 0 else 0
            elapsed = time.time() - start_time
            hands_per_sec = (episode + 1) / elapsed

            print(f"Episode {episode + 1:,}/{num_episodes:,}")
            print(f"  Win Rate: {win_rate:.2f}%")
            print(f"  W/L/P: {wins}/{losses}/{pushes}")
            print(f"  Q-table size: {len(player.q_table)} states")
            print(f"  Current ε: {player.epsilon:.3f}")
            print(f"  Speed: {hands_per_sec:.0f} hands/sec")
            print(f"  Bankroll: ${player.bankroll:,}")
            print()

    print("=" * 60)
    print("TRAINING COMPLETE!")
    print("=" * 60)

    total_time = time.time() - start_time
    total_games = wins + losses + pushes
    final_win_rate = (wins / total_games * 100) if total_games > 0 else 0

    print(f"Total hands: {total_games:,}")
    print(f"Final win rate: {final_win_rate:.2f}%")
    print(f"Q-table size: {len(player.q_table):,} state-action pairs")
    print(f"Training time: {total_time:.1f} seconds")
    print()

    print(f"Saving model to: {save_path}")
    player.save_model(save_path)

    player.training_mode = False
    player.epsilon = 0.0

    return player


if __name__ == "__main__":
    trained_player = train_q_learning_player(
        num_episodes=100000,
        base_bet=5,
        save_path="./_models/q_learning_player.pkl",
        verbose=True
    )

    print("\n✅ Training complete!")
    print("Model saved and ready to use!")
