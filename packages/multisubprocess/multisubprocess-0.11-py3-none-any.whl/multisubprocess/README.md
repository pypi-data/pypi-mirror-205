# Executes multiple subprocesses concurrently and returns the output and return code of each subprocess. (Windows only)

### Tested against Windows 10 / Python 3.10 / Anaconda

## pip install multisubprocess

#### Important: Cannot be executed directly from the console! 



```python
from multisubprocess import multi_subprocess

allqueries = []
for q in range(20):
    allqueries.append(["ls", "-la", r"E:\textcompare"])

res = multi_subprocess(
    allqueries,
    byteinput=b"",
    shell=False,
    close_fds=False,
    start_new_session=True,
    bufsize=8192 * 40,
    invisible=True,
    timeout=15,
    max_threads=5,
    timeout_check_sleep=1,
    kill_all_at_end=True,
    blockbatch=False,
)



# Output from one subprocess
# from pprint import pprint
# from pprint import pprint
# pprint(res[(7, 'ls', '-la', 'E:\\textcompare')])
# defaultdict(<function <lambda> at 0x00000289E4B15750>,
#             {'proc': <Popen: returncode: 0 args: ['ls', '-la', 'E:\\textcompare']>,
#              'returncode': 0,
#              'start': 1682433358.1547163,
#              'stderr': <_io.BytesIO object at 0x00000289EFA2EFC0>,
#              'stderrready': b'',
#              'stdout': <_io.BytesIO object at 0x00000289EFA2EB10>,
#              'stdoutready': b'total 18\ndrwxr-xr-x 1 hansc hansc   0 Apr 24 20:'
#                             b'33 .\ndrwxr-xr-x 1 hansc hansc   0 Apr 24 20:33 .'
#                             b'.\n-rw-r--r-- 1 hansc hansc 321 Apr 24 15:41 text'
#                             b'1.txt\n-rw-r--r-- 1 hansc hansc 367 Apr 24 15:41 '
#                             b'text2.txt\n'})




    

    Args:
        allcommands (str | list): List of commands to execute or one command as a string.
        byteinput (bytes, optional): Input to be passed to the subprocess. Defaults to b"".
        shell (bool, optional): Whether to use shell to execute the command. Defaults to False.
        close_fds (bool, optional): Whether to close file descriptors. Defaults to True.
        start_new_session (bool, optional): Whether to start a new session. Defaults to True.
        bufsize (int, optional): Buffer size for the subprocess. Defaults to 1024 * 200.
        invisible (bool, optional): Whether to run the subprocess invisibly. Defaults to True.
        timeout (int, optional): Timeout for the subprocess. Defaults to 10000000.
        max_threads (int | None, optional): Maximum number of threads to use. Defaults to None (Number of CPUs).
        timeout_check_sleep (int, optional): Sleep time for timeout check. Defaults to 1.
        kill_all_at_end (bool, optional): Whether to kill all subprocesses of the main process at the end. Defaults to True.
        blockbatch (bool, optional): Whether to block batch processing. Defaults to False.
        debug (bool, optional): Whether to print debug information. Defaults to False.
        *args: Additional arguments to be passed to subprocess.Popen.
        **kwargs: Additional keyword arguments to be passed to subprocess.Popen.

    Returns:
        dict: A dictionary containing the output and return code of each subprocess.
		
		
```

