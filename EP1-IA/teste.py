def main():
    acoes = []
    pf = ("salame", "queijo", "rodolfo")
    acoes = [(0, i) for i in pf]
    for i in range(len(acoes)): print(acoes[i])
    print(str())
main()