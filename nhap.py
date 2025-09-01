a = [1,2,1]
a[-1:] += [3]
a[-1:] += [0]
a.insert(len(a),9)
print(a)