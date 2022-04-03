import sys
import BranchPredictor

if __name__ == '__main__':
    predictor = sys.argv[1]
    k, b, m1, m2, n = 0, 0, 0, 0, 0
    if predictor == 'smith':
        b = int(sys.argv[2])
        tracefile = sys.argv[3]
    elif predictor == 'bimodal':
        m2 = int(sys.argv[2])
        tracefile = sys.argv[3]
    elif predictor == 'hybrid':
        k = int(sys.argv[2])
        m1 = int(sys.argv[3])
        n = int(sys.argv[4])
        m2 = int(sys.argv[5])
        tracefile = sys.argv[6]
    else:
        m1 = int(sys.argv[2])
        n = int(sys.argv[3])
        tracefile = sys.argv[4]

    branches = []
    addresses = []

    f = open(tracefile, "r", encoding='utf-8')
    taken, not_taken = 0, 0
    for x in f:
        branch = x.rstrip().split(" ")[1]
        if branch == 't':
            taken += 1
        else:
            not_taken += 1

        # addr = ""
        # for i in range(len(x)-1):
        #     addr += x[i]
        # while len(addr) != 8:
        #     addr = "0"+addr

        uaddr = int(x.rstrip().split(" ")[0], 16)
        branches.append(branch)
        addresses.append(uaddr)

    bp = BranchPredictor.BranchPredictor(predictor, k, b, m2, m1, n, tracefile)
    bp.execute(addresses, branches)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
