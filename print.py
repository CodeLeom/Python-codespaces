from game import CoinRush

game = CoinRush()
state = game.get_state()
for x in state:
    print(f"{x:.3f}")