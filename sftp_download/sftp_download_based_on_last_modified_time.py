from datetime import datetime, time, timedelta
import paramiko

def list_files_acc_to_lmt(sftp_credentials: dict, minutes: int, hours: int, last_days:int, sftp_path_to_extract: str):
    '''
     List files from sftp that have arrived in last n days according to last modified time
    :param sftp_credentials: A dictionary with SFTP Hostname, Password and Username
    :param minutes: no of minutes at while the file ingestion for today takes place
    :param hours: no of hours  at while the file ingestion for today takes place
    :param last_days: no of days for while the list of files is needed
    :param sftp_path_to_extract: SFTP Path where we need to check for the files
    :return: list of files
    '''

    #Establishing Paramiko connection
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(sftp_credentials['HOSTNAME'], username=sftp_credentials['USERNAME'],
                password=sftp_credentials['PASSWORD'])
    ftp = ssh.open_sftp()

    #Modify hours and minutes according to dag schedule
    today_midnight = datetime.combine(datetime.today(), time.min)+ timedelta(hours=hours)+timedelta(minutes=minutes)
    prev_midnight = today_midnight - timedelta(days=last_days)

    print("Today's date:", today_midnight)
    print("Previous Day's date:", prev_midnight)

    files_ = []
    for file in ftp.listdir_attr(sftp_path_to_extract):
        mtime = datetime.fromtimestamp(file.st_mtime)
        if (prev_midnight <= mtime) and (mtime < today_midnight):
            files_.append(file.filename)

    return files_

if __name__ == '__main__':

    #Enter Credentials
    sftp_credentials = {
        "HOSTNAME": '',
        "USERNAME": '',
        "PASSWORD": ''
    }

    #Your ingestion Pipeline timing today (eg: 18:30)
    minutes = 30
    hours = 18
    #No of previous days you want to
    last_days = 1

    sftp_path_to_extract = "/upload"

    files = list_files_acc_to_lmt(sftp_credentials, minutes, hours, last_days, sftp_path_to_extract)
    print(files)
