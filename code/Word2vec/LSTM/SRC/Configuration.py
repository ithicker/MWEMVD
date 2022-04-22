import os


class Configuration:
    """
    记录工程中的配置信息
    """
    root_path = os.path.abspath(os.path.join(os.getcwd(), "../"))
    data_path = os.path.abspath(os.path.join(root_path, './data/'))    # 存放数据文件的根目录
    Func_path = os.path.abspath(os.path.join(data_path, '9_projects_Functions'))    # 数据文件中的项目文件夹

    Non_vul_func = 'Non_vulnerable_functions'   # 不易感染源码的目录名称
    Vul_func = 'Vulnerable_functions'           # 易受感染源码的目录名称

