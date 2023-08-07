import platform

# 判断当前系统是mac还是windows
def get_system():
    """
    判断当前系统是mac还是windows
    :return:
    """
    system = platform.system()
    if system == 'Windows':
        return 'Windows'
    elif system == 'Darwin':
        return 'Mac'
    else:
        return 'Linux'



def get_system_dir(cloud:str,pj:str):
    platform = get_system()
    if platform == 'Windows':
        return f'//{cloud}//file//{pj}//'
    elif platform == 'Mac':
        return f'/Volumes/file/{pj}/'
    else:
        return f'/mnt/{cloud}/file/{pj}/'



def get_system_data_dir(cloud:str,pj:str,data:str):
    platform = get_system()
    if platform == 'Windows':
        return f'//{cloud}//file//{pj}//{data}//'
    elif platform == 'Mac':
        return f'/Volumes/file/{pj}/{data}/'
    else:
        return f'/mnt/{cloud}/file/{pj}/{data}/'