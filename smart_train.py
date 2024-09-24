import runpy
import train
import eval
import sys
import os

cuda = "3"

run_config = {
    'database': 'bungeenerf',
    'scene': 'amsterdam',
    'enable_entropy_skipping': True,
    'feat_threshold': 0.1,
    'offset_threshold': 0,
    'scale_threshold': 0,
    'densify_grad_threshold': 0.0002,
    'lmbda': 0.0005,
}

run_config_list = [run_config.copy() for _ in range(6)]
run_config_list[0]['densify_grad_threshold'] = 0.0001
run_config_list[2]['densify_grad_threshold'] = 0.02
run_config_list[3]['densify_grad_threshold'] = 0.0001
run_config_list[5]['densify_grad_threshold'] = 0.02

run_config_list[3]['enable_entropy_skipping'] = False
run_config_list[4]['enable_entropy_skipping'] = False
run_config_list[5]['enable_entropy_skipping'] = False


run_config_list_tnt = [{
    'database': 'tandt',
    'scene': 'truck',
    'enable_entropy_skipping': False,
    'feat_threshold': 0.1,
    'offset_threshold': 0,
    'scale_threshold': 0,
    'densify_grad_threshold': 0.0002,
    'lmbda': 0.0005,
}]

def run(idx, script_name):
    run_cfg = run_config_list[idx]
    scene = run_cfg['scene']
    enable_entropy_skipping = "--enable_entropy_skipping" if run_cfg['enable_entropy_skipping'] else ""
    feat_threshold = run_cfg['feat_threshold']
    offset_threshold = run_cfg['offset_threshold']
    scale_threshold = run_cfg['scale_threshold']
    densify_grad_threshold = run_cfg['densify_grad_threshold']
    lmbda = run_cfg['lmbda']
    en = "en" if run_cfg['enable_entropy_skipping'] else "hac"
    save_name = f"{en}_{lmbda}_{feat_threshold}_{offset_threshold}_{scale_threshold}_{densify_grad_threshold}"

    cmd = f'CUDA_VISIBLE_DEVICES={cuda} python {script_name} -s data/bungeenerf/{scene} --eval --lod 30 --voxel_size 0 --update_init_factor 128 --iterations 30_000 -m outputs/bungeenerf/{scene}/{save_name} --lmbda {lmbda} {enable_entropy_skipping} --feat_threshold {feat_threshold} --offset_threshold {offset_threshold} --scale_threshold {scale_threshold} --densify_grad_threshold {densify_grad_threshold}'
    print(cmd)
    os.system(cmd)

if __name__ == '__main__':
    for i in range(len(run_config_list_tnt)):
        run(i, 'train.py')
        run(i, 'eval.py')
        print(f"Finished {i+1}/{len(run_config_list)}")

#0 
#1
#2 551704
#3 6698350
#4 3041767
#5 528228