import utility

def main(funs):

    result_array = []
    all = {}
    sway1 = {}
    sway2 = {}
    xpln1 = {}
    xpln2 = {}
    top = {}
    seedarr = [937162211, 6541321, 9879653, 9362224, 937162268,
               936162874, 6662211, 21352211, 77632211, 933362211,
               9376442211, 541321, 33879653, 7265224, 6222158,
               630148470, 51327910, 89462111, 7054511, 9332211]
    def meanval(x):
        return round(x/len(seedarr),2)

    for seed in seedarr:
        utility.getCliArgs(seed)
    # if (utility.args.help):
    #     print(utility.help)
        result_array.append(utility.explnFunc())
        print(seed)
        for i in result_array[-1].items():
            print(i)
    for i in result_array[0]['all'].keys():
        all[i] = 0
        sway1[i] = 0
        sway2[i] = 0
        xpln1[i] = 0
        xpln2[i] = 0
        top[i] = 0
    for result in result_array:
        # print(result)
        for key in result['all'].keys():
            all[key] += result['all'][key]
            sway1[key] += result['sway1'][key]
            sway2[key] += result['sway2'][key]
            xpln1[key] += result['xpln1'][key]
            xpln2[key] += result['xpln2'][key]
            top[key] += result['top'][key]
    print("============================================\nDataset: healthCloseIsses12mths0001-hard.csv")
    print("============================================\nMean results of best outcomes from 20 runs\n============================================\n")
    print("\t",'\t'.join(all.keys()))
    print("all\t",'\t'.join([str(meanval(i)) for i in all.values()]))
    print("sway1\t",'\t'.join([str(meanval(i)) for i in sway1.values()]))
    print("xpln1\t",'\t'.join([str(meanval(i)) for i in xpln1.values()]))
    print("sway2\t",'\t'.join([str(meanval(i)) for i in sway2.values()]))
    print("xpln2\t",'\t'.join([str(meanval(i)) for i in xpln2.values()]))
    print("top\t",'\t'.join([str(meanval(i)) for i in top.values()]))

    # else:
    #     for what, _ in funs.items():
    #         if utility.args.go == "all" or what == utility.args.go:
    #             if funs[what]() == False:
    #                 fails += 1
    #                 print("❌ fail:",what)
    #             else: pass
    # if (fails == 0): return 0
    # else: return 1

if __name__ == "__main__":
    main(utility.egs)
