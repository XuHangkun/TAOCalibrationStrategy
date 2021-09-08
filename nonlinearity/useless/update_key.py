from utils import read_pickle_data,save_pickle_data

# f = "./input/shadowing_info.pkl"
# f = "./input/ra_fit_info.pkl"
f = "./input/nake_true_info.pkl"
data = read_pickle_data(f)
print(data)
key_info = {
        "n_prompt":"O16",
        "n_delay":"nH"
    }
for key in key_info:
    data[key_info[key]] = data.pop(key)
print(data)
save_pickle_data(data,f)
