
import os
# , 'bilbao', 'hollywood', 'pompidou', 'quebec', 'rome'
for lmbda in [0.0005]:  # Optionally, you can try: 0.003, 0.002, 0.001, 0.0005
    for cuda, scene in enumerate(['amsterdam']):
        #one_cmd = f'CUDA_VISIBLE_DEVICES={3} python train.py -s data/bungeenerf/{scene} --eval --lod 30 --voxel_size 0 --update_init_factor 128 --iterations 30_000 -m outputs/bungeenerf_0.02_thred/{scene}/{lmbda} --lmbda {lmbda} --enable_entropy_skipping --feat_threshold 0.1 --offset_threshold 0 --scale_threshold 0'
        #os.system(one_cmd)
        two_cmd = f'CUDA_VISIBLE_DEVICES={3} python eval.py -s data/bungeenerf/{scene} --eval --lod 30 --voxel_size 0 --update_init_factor 128 --iterations 30_000 -m outputs/bungeenerf_0.02_thred/{scene}/{lmbda} --lmbda {lmbda} --feat_threshold 0.1 --offset_threshold 0 --scale_threshold 0'
        os.system(two_cmd)

lmbda = 0.0005
scene = 'amsterdam'
"""
import runpy
import train
import eval
import sys
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "3"

sys.argv = [
    'train.py',  # script name
    '-s', f'data/bungeenerf/{scene}',
    '--eval',
    '--lod', '30',
    '--voxel_size', '0',
    '--update_init_factor', '128',
    '--iterations', '30000',
    '-m', f'outputs/bungeenerf_0.02_thred/{scene}/{lmbda}',
    '--lmbda', f'{lmbda}',
    # '--enable_entropy_skipping',
    '--feat_threshold', '0.1',
    '--offset_threshold', '0',
    '--scale_threshold', '0'
]
train.main()
eval.main()
"""