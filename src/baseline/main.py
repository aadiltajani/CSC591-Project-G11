from testfile import getCliArgs
import utility

def main(funs):

    fails = 0
    getCliArgs()
    if (utility.args.help):
        print(utility.help)
    else:
        for what, _ in funs.items():
            if utility.args.go == "all" or what == utility.args.go:
                if funs[what]() == False:
                    fails += 1
                    print("❌ fail:",what)
                else: print("✅ pass:",what)
    if (fails == 0): return 0
    else: return 1

if __name__ == "__main__":
    main(utility.egs)
