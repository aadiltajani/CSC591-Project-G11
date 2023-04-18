def RULE(ranges, maxSize):
    t = {}
    for range in ranges:
        t[range.txt] = t[range.txt] if range.txt in t else []
        t[range.txt].append({"lo": range.lo, "hi": range.hi, "at": range.at})
    return prune(t, maxSize)

def prune(rule, maxSize):
    n = 0
    for txt, ranges in rule.items():
        n += 1
        if len(ranges) == maxSize[txt]:
            n += 1
            rule[txt] = None
    if n > 0: return rule
