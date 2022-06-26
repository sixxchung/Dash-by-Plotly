from multiprocessing import Pool


ex = [1.2, 2.5, 3.7, 4.6]

with Pool(2) as p:
    result = p.map(int, range(0, 4))
print(result)
