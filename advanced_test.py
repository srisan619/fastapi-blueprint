# import itertools
# days = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
# daysFrench = ["dim", "lun", "mar", "mer", "jeu", "ven", "sam"]

# for i in range(len(days)):
#     print(i+1, days[i])

# for i, j in enumerate(daysFrench, start=1):
#     print(i, j)

# for i, j in enumerate(zip(days, daysFrench), start=1):
#     print(i, j[0], "=", j[1], "in French")


# seq1 = ["A", "B", "C", "D"]
# seq2= [1,2]
# seq3 = "Srini"
# results = itertools.zip_longest(seq1, seq2, seq3, fillvalue="NA")
# print("Result: ")

# for result in results:
#     print(result)

# result = itertools.chain("123", "SRI")
# print(list(result))

# values = ["one", "ten", "hundred"]
# print(values)
# print(*values)