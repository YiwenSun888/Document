import matplotlib.pyplot as plt
import numpy as np

res = '../benchmarks/results/x64_asammdf_7.0.1_mdfreader_4.1.rst'
topic = 'Convert'
aspect = 'ram'
for_doc = True

with open(res, 'r') as f:
    lines = f.readlines()

platform = 'x86' if '32 bit' in lines[2] else 'x64'

idx = [i for i, line in enumerate(lines) if line.startswith('==')]

table_spans = {'open': [idx[1] + 1, idx[2]],
               'save': [idx[4] + 1, idx[5]],
               'get': [idx[7] + 1, idx[8]],
               'convert' : [idx[10] + 1, idx[11]],
               'merge' : [idx[13] + 1, idx[14]]}


start, stop = table_spans[topic.lower()]

cat = [l[:50].strip(' \t\n\r\0*') for l in lines[start: stop]]
time = np.array([int(l[50:61].strip(' \t\n\r\0*')) for l in lines[start: stop]])
ram = np.array([int(l[61:].strip(' \t\n\r\0*')) for l in lines[start: stop]])

if aspect == 'ram':
    arr = ram
else:
    arr = time

y_pos = list(range(len(cat)))

fig, ax = plt.subplots()
fig.set_size_inches(15, 3.8 / 12 * len(cat) + 1.2)

asam_pos = [i for i, c in enumerate(cat) if c.startswith('asam')]
mdfreader_pos = [i for i, c in enumerate(cat) if c.startswith('mdfreader')]

ax.barh(asam_pos, arr[asam_pos], color='green', ecolor='green')
ax.barh(mdfreader_pos, arr[mdfreader_pos], color='blue', ecolor='black')
ax.set_yticks(y_pos)
ax.set_yticklabels(cat)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Time [ms]' if aspect == 'time' else 'RAM [MB]')
if topic == 'Get':
    ax.set_title('Get all channels (36424 calls) - {}'.format('time' if aspect == 'time' else 'ram usage'))
else:
    ax.set_title('{} test file - {}'.format(topic, 'time' if aspect == 'time' else 'ram usage'))
ax.xaxis.grid()

fig.subplots_adjust(bottom=0.72/fig.get_figheight(), top=1-0.48/fig.get_figheight(), left=0.4, right=0.9)

if aspect == 'time':
    if topic == 'Get':
        name = '{}_get_all_channels.png'.format(platform)
    else:
        name = '{}_{}.png'.format(platform, topic.lower())
else:
    if topic == 'Get':
        name = '{}_get_all_channels_ram_usage.png'.format(platform)
    else:
        name = '{}_{}_ram_usage.png'.format(platform, topic.lower())

plt.show()