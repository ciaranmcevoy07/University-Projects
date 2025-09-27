import re
str='O Tst, que ta muito tst'
str2 = 'tst'
a = re.search(str2 + r'(.+?)', str, re.IGNORECASE)
str = re.sub(r'\b' + str2 + r'\b', 'pneu', str2, flags=re.IGNORECASE)
print(str)