import subprocess

branches = []

returnvalue = subprocess.Popen(
    ['git', 'ls-remote', '--heads'], stdout=subprocess.PIPE)
returnvalue = returnvalue.communicate()[0].split()
for i in range(len(returnvalue)):
    if i % 2 != 0:
        branches.append(returnvalue[i].split("/")[-1])

print(branches)
