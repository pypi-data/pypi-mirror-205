import io
import os
import subprocess
import threading
import time
from subprocesskiller import (
    kill_subprocs,
    kill_pid,
)
from kthread_sleep import sleep
from collections import defaultdict
from subprocess_alive import is_process_alive
from escape_windows_filepath import escape_windows_path

nested_dict = lambda: defaultdict(nested_dict)
startupinfo = subprocess.STARTUPINFO()
creationflags = 0 | subprocess.CREATE_NO_WINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE


def escape_path(path: str) -> str:
    """
    Escapes the given path by removing any leading or trailing whitespaces and checking if it contains any spaces.
    If the path contains spaces, it is assumed to be a Windows path and is escaped using the escape_windows_path function.
    Otherwise, the original path is returned.

    :param path: A string representing the path to be escaped.
    :type path: str
    :return: The escaped path.
    :rtype: str
    """
    path = path.strip()
    if " " in path:
        return escape_windows_path(path)
    return path


def multi_subprocess(
    allcommands: str | list,
    byteinput: bytes = b"",
    shell: bool = False,
    close_fds: bool = True,
    start_new_session: bool = True,
    bufsize: int = 1024 * 200,
    invisible: bool = True,
    timeout: int = 10000000,
    max_threads: int | None = None,
    timeout_check_sleep: int = 1,
    kill_all_at_end: bool = True,
    blockbatch: bool = False,
    debug=False,
    *args,
    **kwargs,
) -> dict:
    r"""
    Executes multiple subprocesses concurrently and returns the output and return code of each subprocess.

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
    """

    def kill_em_all():
        """
        Helper function to kill all subprocesses.
        """
        nonlocal allproc
        while True:
            if stopthread:
                return
            sleep(timeout_check_sleep)
            for process_ in list(allproc.keys()):
                try:
                    if process_ in allalive:
                        if time.time() - timeout > allproc[process_]["start"]:
                            kill_pid(pid=int(allproc[process_]["proc"].pid))
                except Exception as va:
                    if debug:
                        print(va)
                    continue

    if not max_threads:
        max_threads = os.cpu_count()
    if max_threads < 1:
        max_threads = 1
    allproc = nested_dict()
    allalive = set()
    alldone = list()
    wholeprocessdone = set()
    stopthread = False

    t = threading.Thread(target=kill_em_all)
    t.start()
    querylist = [(i,)+tuple(x) if isinstance(x, list) else (i,x) for i,x in enumerate(allcommands)]
    #coun = -1
    while len(alldone) != len(querylist):
        for q in set(querylist) - set(allproc.keys()):
            q2 = q[1:]
            # try:
            #     q = (coun,) + q2
            # except Exception as ad:
            #     q = (coun,) + (q2,)
            #coun = coun + 1
            allprockeys = list(allproc.keys())
            allalive.clear()
            for k in allprockeys:
                try:
                    actpid = allproc[k]["proc"].pid
                    if actpid in wholeprocessdone:
                        continue
                    if is_process_alive(actpid):
                        allalive.add(k)
                    else:
                        wholeprocessdone.add(actpid)
                except Exception as vas:
                    if debug:
                        print(vas)
                    continue

            if len(allalive) >= max_threads:
                for aliveprocess in allalive:
                    try:
                        for data in iter(
                            allproc[aliveprocess]["proc"].stdout.readline, b""
                        ):
                            allproc[aliveprocess]["stdout"].write(data)

                        # try:
                        #     allproc[aliveprocess]["stdout"].close()
                        # except Exception as i:
                        #     print(i)

                    except Exception as fe:
                        if debug:
                            print(fe)
                        break
                    if not blockbatch:
                        break
            alldone.append(q)
            allproc[q]["stdout"] = io.BytesIO()
            allproc[q]["stderr"] = io.BytesIO()
            if invisible:
                invisibledict = {
                    "startupinfo": startupinfo,
                    "creationflags": creationflags,
                }
            else:
                invisibledict = {}
            kwargs = kwargs | invisibledict
            allproc[q]["start"] = time.time()
            allproc[q]["proc"] = subprocess.Popen(
                list(q2) if isinstance(q2, tuple) else q2,
                *args,
                stdin=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                close_fds=close_fds,
                start_new_session=start_new_session,
                shell=shell,
                bufsize=bufsize,
                **kwargs,
            )
            if byteinput:
                allproc[q]["proc"].stdin.write(byteinput)
            allproc[q]["proc"].stdin.close()

    for aliveprocess in allproc:
        try:
            for data in iter(allproc[aliveprocess]["proc"].stdout.readline, b""):
                allproc[aliveprocess]["stdout"].write(data)
            allproc[aliveprocess]["stdoutready"] = allproc[aliveprocess][
                "stdout"
            ].getvalue()
            try:
                allproc[aliveprocess]["stdout"].close()
            except Exception as i:
                if debug:
                    print(i)
            # allproc[aliveprocess]["stdoutready"] = b"".join(
            #     allproc[aliveprocess]["stdoutready"]
            # )
        except Exception as sd:
            if debug:
                print(sd)
            continue

    for aliveprocess in allproc:
        try:
            for data in iter(allproc[aliveprocess]["proc"].stderr.readline, b""):
                allproc[aliveprocess]["stderr"].write(data)
            allproc[aliveprocess]["stderrready"] = allproc[aliveprocess][
                "stderr"
            ].getvalue()
            try:
                allproc[aliveprocess]["stderr"].close()
            except Exception as i:
                if debug:
                    print(i)

            # allproc[aliveprocess]["stderrready"] = b"".join(
            #     allproc[aliveprocess]["stderrready"]
            # )

        except Exception as sd:
            if debug:
                print(sd)
            continue
    for aliveprocess in allproc:
        try:
            allproc[aliveprocess]["returncode"] = allproc[aliveprocess]["proc"].wait()
        except Exception as sd:
            if debug:
                print(sd)
            continue
    stopthread = True
    while t.is_alive():
        sleep(0.005)
    if kill_all_at_end:
        try:
            kill_subprocs(dontkill=(("Caption", "conhost.exe"),))
        except Exception as ads:
            if debug:
                print(ads)
    return allproc
