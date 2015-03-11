import pickle

with open("players.dat", "wb") as f:
    pickle.dump({}, f)