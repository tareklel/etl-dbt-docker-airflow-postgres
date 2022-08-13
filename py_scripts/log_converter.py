import re
import os
import csv


LOG_PATTERN = '^(\S+) (\S+) (\S+) \[(\S+?):(\S+) \] \"(.+?)\" (\S+) (\S+) \"(.+?)\" \"(.+?)\"'
BASEDIR = '../staging'


def parseApacheLogLine(logline):
    """ Parse a line in the Apache Common Log format
    Args:
        logline (str): a line of text in the Apache Common Log format
    Returns:
        tuple: either a dictionary containing the parts of the Apache Access Log and 1,
               or the original invalid log line and 0
    """
    match = re.search(LOG_PATTERN, logline)
    return [match.group(1), match.group(3), match.group(5), match.group(10)]


def convert_logs(**kwargs):
    log_list = kwargs['task_instance'].xcom_pull(task_ids='log_collection')
    field_names = ['clientip', 'username', 'time', 'user-agent']
    for file in log_list:
        logFile = os.path.join(BASEDIR, file)
        csv_filename = f'{BASEDIR}/{file[:-4]}.csv'
        with open(csv_filename, "w", encoding="utf-8") as c:
            writer = csv.writer(c)
            writer.writerow(field_names)
            with open(logFile) as f:
                for line in f:
                    writer.writerow(parseApacheLogLine(line))
                f.close()
            c.close()

