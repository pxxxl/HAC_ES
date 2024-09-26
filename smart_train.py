import runpy
import train
import eval
import sys
import os

cuda = "0"

feat_threshold_list = [0.1, 0.2, 0.5, 1.0]
lmbda_list = [0.0005, 0.001, 0.002, 0.004]

run_config_list_template = {
    'database': 'bungeenerf',
    'scene': 'amsterdam',
    'enable_entropy_skipping': False,
    'feat_threshold': 0.1,
    'offset_threshold': 0,
    'scale_threshold': 0,
    'densify_grad_threshold': 0.02,
    'lmbda': 0.0005,
}

run_config_list = []
for feat_threshold in feat_threshold_list:
    for lmbda in lmbda_list:
        run_config = run_config_list_template.copy()
        run_config['feat_threshold'] = feat_threshold
        run_config['lmbda'] = lmbda
        run_config['enable_entropy_skipping'] = True
        run_config_list.append(run_config)

for lmbda in lmbda_list:
    run_config = run_config_list_template.copy()
    run_config['lmbda'] = lmbda
    run_config_list.append(run_config)

def run(idx, config, script_name):
    run_cfg = config[idx]
    scene = run_cfg['scene']
    database = run_cfg['database']
    enable_entropy_skipping = "--enable_entropy_skipping" if run_cfg['enable_entropy_skipping'] else ""
    feat_threshold = run_cfg['feat_threshold']
    offset_threshold = run_cfg['offset_threshold']
    scale_threshold = run_cfg['scale_threshold']
    densify_grad_threshold = run_cfg['densify_grad_threshold']
    lmbda = run_cfg['lmbda']
    en = "en" if run_cfg['enable_entropy_skipping'] else "hac"
    save_name = f"{en}_{lmbda}_{feat_threshold}_{offset_threshold}_{scale_threshold}_{densify_grad_threshold}"

    cmd = f'CUDA_VISIBLE_DEVICES={cuda} python {script_name} -s data/{database}/{scene} --eval --lod 30 --voxel_size 0 --update_init_factor 128 --iterations 30_000 -m outputs/{database}/{scene}/{save_name} --lmbda {lmbda} {enable_entropy_skipping} --feat_threshold {feat_threshold} --offset_threshold {offset_threshold} --scale_threshold {scale_threshold} --densify_grad_threshold {densify_grad_threshold}'
    print(cmd)
    os.system(cmd)

if __name__ == '__main__':
    for i in range(len(run_config_list)):
        run(i, run_config_list, 'train.py')
        run(i, run_config_list, 'eval.py')
        print(f"Finished {i+1}/{len(run_config_list)}")

#0 
#1
#2 551704
#3 6698350
#4 3041767
#5 528228