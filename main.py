
FILE_PATH = r"E:\DataSets\cifar-10-python\cifar-10-batches-py\data_batch_1"

def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict

if __name__ == "__main__":
    dataset = unpickle(FILE_PATH)
    print(dataset)