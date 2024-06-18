from gnss_tec import rnx


def read(date: str):
    pass


file = 'files/2019-06-23/DAEJ00KOR_R_20191740000_01D_30S_MO.rnx'

f = open(file).readlines()

for i, row in enumerate(f):
    if i <= 10:
        print(i, row)

'''
with open('files/2019-06-23/DAEJ00KOR_R_20191740000_01D_30S_MO.rnx') as obs_file:
    reader = rnx(obs_file)
    print(reader)
   
   for tec in reader:
        print(
            '{} {}: {} {}'.format(
                tec.timestamp,
                tec.satellite,
                tec.phase_tec,
                tec.p_range_tec,
            )
        )
    '''
