import utility
import stats
import copy

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
        result_array.append(utility.explnFunc())
    var_dic = {}
    for i in result_array[0]['all'].keys():
        var_dic[i] = []
        all[i] = 0
        sway1[i] = 0
        sway2[i] = 0
        xpln1[i] = 0
        xpln2[i] = 0
        top[i] = 0

    data_store = {k:copy.deepcopy(var_dic) for k in result_array[0].keys()}

    for result in result_array:
        for key in result['all'].keys():
            all[key] += result['all'][key]
            sway1[key] += result['sway1'][key]
            sway2[key] += result['sway2'][key]
            xpln1[key] += result['xpln1'][key]
            xpln2[key] += result['xpln2'][key]
            top[key] += result['top'][key]
            for i in data_store.keys():
                data_store[i][key].append(result[i][key])
    print("============================================\nDataset: healthCloseIsses12mths0001-hard.csv")
    print("============================================\nMean results of best outcomes from 20 runs\n============================================\n")
    print("\t",'\t'.join(all.keys()))
    print("all\t",'\t'.join([str(meanval(i)) for i in all.values()]))
    print("sway1\t",'\t'.join([str(meanval(i)) for i in sway1.values()]))
    print("xpln1\t",'\t'.join([str(meanval(i)) for i in xpln1.values()]))
    print("sway2\t",'\t'.join([str(meanval(i)) for i in sway2.values()]))
    print("xpln2\t",'\t'.join([str(meanval(i)) for i in xpln2.values()]))
    print("top\t",'\t'.join([str(meanval(i)) for i in top.values()]))
    
    print('\n')
    print("============================================\nEffect Size Test Comparison - Cliff's Delta\n============================================")
    print("\t\t",'\t'.join(all.keys()))
    for i in [('all', 'all'), ('all', 'sway1'), ('all', 'sway2'), ('sway1', 'sway2'), ('sway1', 'xpln1'), ('sway2', 'xpln2'), ('sway1', 'top')]:
        print(i[0]+' to '+i[1]+'\t', '\t'.join(['=' if i else '≠' for i in [utility.cliffsDelta(data_store[i[0]][j], data_store[i[1]][j]) for j in all.keys()]]))


    print("\n\n============================================\nScottsKnot\n============================================")
    for i in all.keys():
        rxs = []
        print('\nScottsKnot for:',i)
        for k,v in [i for i in data_store.items() if i[0] != 'top']:
            rxs.append(stats.RX(v[i],"" + k))
        for rx in stats.tiles(stats.scottKnot(rxs)):
            print("",rx['rank'],rx['name'],rx['show'],sep='\t')


if __name__ == "__main__":
    main(stats.egs)
