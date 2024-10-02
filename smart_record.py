import os
import sys
import regex

project_root_path = os.path.dirname(os.path.abspath(__file__))

record_target_dir_list = [os.path.join(project_root_path, "outputs", "bungeenerf", "amsterdam")]

collect_target_dir_list = []

for rtd in record_target_dir_list:
    all_folders = os.listdir(rtd)
    for folder in all_folders:
        # match start with "en" or "hac"
        if regex.match(r"^(en|hac)", folder):
            collect_target_dir_list.append(os.path.join(rtd, folder))

log_file_list = []

for ctd in collect_target_dir_list:
    # if exist hacpp.log, record it
    if os.path.exists(os.path.join(ctd, "hacpp.log")):
        log_file_list.append(os.path.join(ctd, "hacpp.log"))

data_list = []

for log in log_file_list:
    with open(log, "r") as f:
        log_str = f.read()
    print (f"file_path: {log}")
    print (log_str)
    try:
        # match "feat_threshold: xxx\n" and get xxx to float
        feat_threshold = regex.search(r"feat_threshold: (\d+\.\d+)", log_str).group(1)
        offset_threshold = regex.search(r"offset_threshold: (\d+\.\d+)", log_str).group(1)
        scale_threshold = regex.search(r"scale_threshold: (\d+\.\d+)", log_str).group(1)
        # match "enable_entropy_skipping: xxxx" xxxx as string
        enable_entropy_skipping = regex.search(r"enable_entropy_skipping: (\w+)", log_str).group(1)
        enable_entropy_skipping = True if enable_entropy_skipping == "True" else False
        file_dir_name = os.path.dirname(log)
        # just a dir name, not dir path
        file_dir_name = os.path.basename(file_dir_name)
        # match "aaa_bbb_ccc_ddd_eee_fff", get fff as float
        grad = regex.search(r"_(\d+\.\d+)$", file_dir_name).group(1)
        # match "aaa_bbb_ccc_ddd_eee_fff", get bbb as float
        lamda = regex.search(r"_(\d+\.\d+)_", file_dir_name).group(1)
        # match "Total xxx", xxx is a float
        total_size = regex.search(r"Total (\d+\.\d+)", log_str).group(1)
        psnr = regex.search(r"PSNR :.*1;35m  (\d+\.\d+)", log_str).group(1)
        print(f"feat_threshold: {feat_threshold}, offset_threshold: {offset_threshold}, scale_threshold: {scale_threshold}, enable_entropy_skipping: {enable_entropy_skipping}, grad: {grad}, total_size: {total_size}, psnr: {psnr}")
        data_list.append(
            {
                "feat_threshold": float(feat_threshold),
                "offset_threshold": float(offset_threshold),
                "scale_threshold": float(scale_threshold),
                "enable_entropy_skipping": enable_entropy_skipping,
                "grad": float(grad),
                "total_size": float(total_size),
                "psnr": float(psnr),
                "lamda": float(lamda)
            }
        )
    except Exception as e:
        print(f"Error: {e}")
        continue

plot_line_config_list = [
    {
        "feat_threshold": 0.03,
        "offset_threshold": 0,
        "scale_threshold": 0,
        "enable_entropy_skipping": True,
        "grad": 0.0002,
    },
    {
        "feat_threshold": 0.07,
        "offset_threshold": 0,
        "scale_threshold": 0,
        "enable_entropy_skipping": True,
        "grad": 0.0002,
    },
    {
        "feat_threshold": 1.5,
        "offset_threshold": 0,
        "scale_threshold": 0,
        "enable_entropy_skipping": True,
        "grad": 0.0002,
    },
    {
        "feat_threshold": 0.1,
        "offset_threshold": 0,
        "scale_threshold": 0,
        "enable_entropy_skipping": False,
        "grad": 0.0002,
    }
]

line_x_s = []
line_y_s = []

for config in plot_line_config_list:
    line_x = []
    line_y = []
    lamda_list = []
    for data in data_list:
        if data["feat_threshold"] == config["feat_threshold"] and data["offset_threshold"] == config["offset_threshold"] and data["scale_threshold"] == config["scale_threshold"] and data["enable_entropy_skipping"] == config["enable_entropy_skipping"] and data["grad"] == config["grad"]:
            line_x.append(data["total_size"])
            line_y.append(data["psnr"])
            lamda_list.append(data["lamda"])
    # sort line_x_s using lmada_list
    line_x = [x for _, x in sorted(zip(lamda_list, line_x))]
    line_y = [y for _, y in sorted(zip(lamda_list, line_y))]
    line_x_s.append(line_x)
    line_y_s.append(line_y)

#use json to save data
import json
json_str = json.dumps(data_list, indent=4)
with open("smart_record.json", "w") as f:
    f.write(json_str)

with open("line_x_s.json", "w") as f:
    f.write(json.dumps(line_x_s, indent=4))

with open("line_y_s.json", "w") as f:
    f.write(json.dumps(line_y_s, indent=4))
    
