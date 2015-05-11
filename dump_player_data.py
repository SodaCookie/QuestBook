import pickle
print("Resetting player data.")
with open("player.data", "wb") as file:
  pickle.dump({}, file)