import torch

with open("partea_speciala.txt", "r", encoding="utf-8") as f:
    text = f.read()

print("length of data: ", len(text))
print(text[:1000])

chars = sorted(list(set(text)))
print(len(chars))
print(''.join(chars))

stoi = {ch: i for i, ch in enumerate(chars)}
itos = {i: ch for i, ch in enumerate(chars)}
encode = lambda s: [stoi[c] for c in s]
decode = lambda l: ''.join(itos[i] for i in l)

print(encode("hii there"))
print(decode(encode("hii there")))


data = torch.tensor(encode(text), dtype=torch.long)
print(data.shape, data.dtype)
print(data[:1000])


# split the data intro training and validation sets (90% - 10%)
n = int(0.9 * len(data))
train_data = data[:n]
val_data = data[n:]

block_size = 8
print(train_data[:block_size+1])
