import pickle
def read_pickle_data(file_path):
    file  = open(file_path,"rb")
    data = pickle.load(file)
    file.close()
    return data

def save_pickle_data(data,file_path):
    file  = open(file_path,"wb")
    pickle.dump(data,file)
    file.close()
