#!/share/nas2/genome/biosoft/Python//3.7.3/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2023/4/28 13:31
# @Author : jmzhang
# @Email : jmzhang1911@gmail.com
from pathlib import Path
import datetime


def mkdir(*path: str):
    """mkdir recursive-dir"""
    for p in list(path):
        if not Path(p).exists():
            Path(p).mkdir(parents=True, exist_ok=True)


def read_cfg(config):
    with open(config, 'r', encoding='utf-8') as f:
        config_dict = {}
        for line in f:
            if line.strip().startswith('#') or line.strip() == '':
                continue
            k, v = line.strip().split()
            config_dict[k] = str(v).strip()
    return config_dict


def read_yaml(yaml_file):
    import yaml
    with open(yaml_file, 'r') as f:
        yaml_dict = yaml.safe_load(f)

    return yaml_dict


def make_summary(script_path, status='doing'):
    logging_summary = Path(__file__).parent / 'logging_summary.txt'
    try:
        with open(logging_summary, 'a') as f:
            info_log = 'datetime:{}\tpwd:{}\tscript_id:{}\tstatus:{}\n'. \
                format(datetime.datetime.now().replace(microsecond=0), Path().absolute(), Path(script_path).name,
                       status)
            f.write(info_log)
    except PermissionError:
        pass
