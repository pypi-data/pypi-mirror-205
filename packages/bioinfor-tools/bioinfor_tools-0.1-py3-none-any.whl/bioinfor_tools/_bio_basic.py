from pathlib import Path


class BioBasic:
    """
    - basic functions and property
        - read cfg
        - mkdir dir
        - module property
    """
    # 主路径位置
    BASE_DIR = Path(__file__).absolute().parent.parent
    # 日志路径
    LOGGING_SUMMARY = BASE_DIR / 'logging_summary.txt'

    def __init__(self, module):
        # 模块所在的绝对父目录
        self._module_dir = Path(module).absolute().parent
        # 模块的名称
        self._module_name = Path(module).name
