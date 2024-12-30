from collections import deque


def prepare_data(file="input.txt"):
    with open(file) as f:
        lines = f.readlines()
    secrets = [int(line.strip()) for line in lines]

    return {"secrets": secrets}


def n_secret(secret, n):
    for _ in range(n):
        temp = secret * 64
        secret = (temp ^ secret) % 16777216
        temp = secret // 32
        secret = (temp ^ secret) % 16777216
        temp = secret * 2048
        secret = (temp ^ secret) % 16777216

    return secret


def solve1(secrets, **kwargs):
    return sum([n_secret(secret, 2000) for secret in secrets])


def solve2(secrets, **kwargs):
    total_dict = {}

    for secret in secrets:
        seller_dict = {}
        price = secret % 10
        sequence = deque([], maxlen=4)

        for _ in range(2000):
            secret = n_secret(secret, 1)
            new_price = secret % 10
            sequence.append(new_price - price)
            price = new_price

            if len(sequence) == 4:
                t_seq = tuple(sequence)
                if t_seq not in seller_dict:
                    seller_dict[t_seq] = price

        for k, v in seller_dict.items():
            total_dict[k] = total_dict.get(k, 0) + v
    return max(total_dict.values())
