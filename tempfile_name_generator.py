from datetime import datetime

def get_tempfilename(path,extension):
    now = datetime.now()
    datestring=now.strftime("%d%m%Y%H%M%S%f").rstrip('0')
    filename=f"{path}/tempImg-{datestring}{extension}"
    return filename