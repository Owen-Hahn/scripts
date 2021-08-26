import secrets
import sys

words =[]

for file in sys.argv[1:]:
    with open(file) as f:
        for line in f:
            if len(line) > 5:
                words.append(line[0].upper() + line[1:-1])


password = ''
for i in range(3):
    password += secrets.choice(words)

print(password)
