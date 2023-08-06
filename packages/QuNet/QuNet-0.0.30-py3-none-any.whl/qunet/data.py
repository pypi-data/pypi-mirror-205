import copy
import torch

class Data:
    """
    Data class. Its iterator gives out data in batches of batch_size examples in each.
    """
    def __init__(self, dataset, shuffle=False, batch_size=64,  whole_batch=False, n_packs=1, n_batches=-1) -> None:
        """
        Data class. Its iterator gives out data in batches of batch_size examples in each.

        Args
        ------------
            dataset (tensor or list of tensors):
                data for batches formation - it can be a torch tensor or a list (tuple) of tensors of the same length
            shuffle (bool = False):
                shuffle or not data
            batch_size (int = 64):
                minibatch size; then you can change
            whole_batch (bool = False):
                take only batches of size batch_size (if the number of examples is not divisible by batch_size)
            n_packs (int = 1)
                split the dataset into n_packs packs; the iterator terminates on the first pack and the next time it is called, it starts at the second pack, and so on.
            n_batches (int = -1)
                print only n_batches of the first batches (if n_batches < 0, then all)

        Example:
        ------------        
        ```
        X, Y = torch.rand(1000,2),  torch.rand(1000,)
        data = Data( (X,Y),  batch_size=128)
        for x,y in data:
            print(x.shape, y.shape)
        ```
        """
        assert torch.is_tensor(dataset) or type(dataset) is list or type(dataset) is tuple, f"data = tensor or [X, Y, ...] <- list or tuple; got: {type(dataset)}"

        self.data = self.set_data_list(dataset)
        self.check_data(self.data)

        self.shuffle    = shuffle      # перемешивать или нет данные
        self.batch_size = batch_size   # размер минибатча
        self.start = 0                 # индекс начала текущего батча
        self.n_packs = n_packs         # разбить весть датасет на n_packs паков
        self.pack_id = 0               # номер текущего пака
        self.whole_batch = whole_batch # брать только батчи размера batch_size
        self.n_batches = n_batches     # выдать только сктолько первых батчей

    #---------------------------------------------------------------------------

    def set_data_list(self, data):
        if   torch.is_tensor(data):  # dataset will be list of tensors
            return data
        elif type(data) is tuple:
            return list(data)
        elif type(data) is list:
            return data

        assert True, "dataset should be tensor or tuple (list) of tensors"
    #---------------------------------------------------------------------------

    def check_data(self, data):
        """ check data in list of tensors """
        if torch.is_tensor(data):
            return True

        for i,d in enumerate(data): # check data
            assert torch.is_tensor(d), "all data in dataset should be torch tensors"
            if i==0:
                count_first = len(d)
            else:
                assert len(d) == count_first, "all tensors must have the same length (number of examples)"
        return True
    #---------------------------------------------------------------------------

    def reset(self):
        self.start = 0
        self.pack_id = 0

    #---------------------------------------------------------------------------

    def copy(self):
        return copy.deepcopy(self)

    #---------------------------------------------------------------------------

    def add(self, data):
        """
        добавляем датасет с той-же структурой данных
        """
        if torch.is_tensor(data.data):
            assert torch.is_tensor(self.data) , "Data.add: method add works only with simple list of tensors"
            self.data = torch.cat([self.data, data.data], dim=0)

        for i, (cur, new) in enumerate(zip(self.data, data.data)):
            assert torch.is_tensor(cur) and torch.is_tensor(new), "Data.add: method add works only with simple list of tensors"
            assert cur.shape[1:] == new.shape[1:], "Data.add: data should have the same shape (except first index)"
            self.data[i] = torch.cat([cur, new], dim=0)

        return self
    #---------------------------------------------------------------------------

    def count(self):
        """ Считаем количество данных """
        if torch.is_tensor(self.data):
            return len(self.data)
        return len(self.data[0])

    #---------------------------------------------------------------------------

    def mix(self, data, idx=None):
        """ Перемешать данные. С list по памяти эффективнее, чем с tuple."""
        if idx is None:
            idx = torch.randperm(  self.count() )

        if torch.is_tensor(data):
            return data[idx]

        for i in range(len(data)):
            data[i] = data[i][idx]
        return data

    #---------------------------------------------------------------------------

    def transform(self):
        """ Может переопределить наследник, для, например, пересортировке данных """
        pass

    #---------------------------------------------------------------------------

    def get_batch(self, data, s, B):
        if torch.is_tensor(data):
            return data[s: s+B]
        return [ d[s: s+B] for d in data ]

    #---------------------------------------------------------------------------

    def __next__(self):
        if (self.start >= self.count() )                                             \
        or                                                                           \
           (self.whole_batch and self.start + self.batch_size > self.count() )       \
        or                                                                           \
           (self.n_batches > 0 and self.start // self.batch_size >= self.n_batches ):
                self.start = self.pack_id = 0
                if self.shuffle:
                    self.data = self.mix(self.data)
                self.transform()
                raise StopIteration

        n = self.count() // self.n_packs
        if self.start > self.pack_id * n + n:
            self.pack_id += 1
            raise StopIteration

        batch = self.get_batch(self.data, self.start, self.batch_size)
        self.start += self.batch_size
        return batch

    def __iter__(self):
        return self

    def __len__(self):
        nb = self.count()  // self.batch_size
        if not self.whole_batch and self.count()  % self.batch_size:
            nb += 1
        return nb

    def unit_test():
        X, Y = torch.rand(1000,2),  torch.rand(1000,)
        data = Data( (X,Y),  batch_size=128)
        return True

#===============================================================================
#                                   Main
#===============================================================================
if __name__ == '__main__':
    X = torch.rand((100,))
    data = Data(X, batch_size=50)
    for x in data:
        print(x)
        x[:] = 0
    for x in data:
        print(x)
