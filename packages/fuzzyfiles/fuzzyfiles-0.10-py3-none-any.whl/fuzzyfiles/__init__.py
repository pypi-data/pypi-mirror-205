from multisubprocess import multi_subprocess
from rapidfuzz import fuzz
from flatten_everything import flatten_everything, ProtectedList
import numpy as np
import pandas as pd


def fuzzy_file_search(
    querylist: list,
    files: str | list | tuple,
    fzf_path: str = "fzf.exe",
    fzfargs: tuple = ("-i",),
    shell: bool = False,
    close_fds: bool = False,
    start_new_session: bool = True,
    bufsize: int = 8192 * 4,
    invisible: bool = True,
    timeout: int = 60,
    max_threads: int | None = None,
    timeout_check_sleep: int | float = 3,
    kill_all_at_end: bool = True,
    blockbatch: bool = False,
) -> pd.DataFrame:
    r"""

    Args:
        querylist (list): List of queries to search for.

            Token	     Match type					        Description
            sbtrkt	     fuzzy-match				        Items that match sbtrkt
            'wild	     exact-match (quoted)		        Items that include wild
            ^music	     prefix-exact-match			        Items that start with music
            .mp3$	     suffix-exact-match			        Items that end with .mp3
            !fire	     inverse-exact-match		        Items that do not include fire
            !^music	     inverse-prefix-exact-match	        Items that do not start with music
            !.mp3$	     inverse-suffix-exact-match	        Items that do not end with .mp3

            A single bar character term acts as an OR operator. For example, the following query matches entries that
             start with core and end with either go, rb, or py.

            ^core go$ | rb$ | py$
            VERY IMPORTANT: ---- SPACE BEFORE and AFTER the single bar character term

            More information here: https://github.com/junegunn/fzf


        files (str | list | tuple): Path(s) to file(s) to search in.
        fzf_path (str, optional): Path to the fzf executable. Defaults to "fzf.exe".
        fzfargs (tuple, optional): Additional arguments to pass to fzf. Defaults to ("-i",).
        shell (bool, optional): Whether to use a shell to execute the command. Defaults to False.
        close_fds (bool, optional): Whether to close file descriptors. Defaults to False.
        start_new_session (bool, optional): Whether to start a new session. Defaults to True.
        bufsize (int, optional): Buffer size. Defaults to 8192 * 4.
        invisible (bool, optional): Whether to run the command invisibly (no window). Defaults to True.
        timeout (int, optional): Timeout in seconds. Defaults to 60.
        max_threads (int | None, optional): Maximum number of threads to use. Defaults to None (number of CPUs).
        timeout_check_sleep (int | float, optional): Time to sleep between timeout checks. Defaults to 3.
        kill_all_at_end (bool, optional): Whether to kill all not finished processes at the end. Defaults to True.
        blockbatch (bool, optional): Whether to block batch processing. Defaults to False.

    Returns:
        pd.DataFrame: A dataframe containing the search results.
    """
    fi = files
    if isinstance(fi, str):
        fi = [fi]
    elif isinstance(fi, tuple):
        fi = list(fi)
    allqueries = []
    allfilepa = []
    for filep in fi:
        with open(filep, mode="rb") as f:
            stringp = f.read()
        stringprep = stringp
        allqueries.append([stringprep, []])
        allfilepa.append(filep)
        for q in querylist:
            allqueries[-1][-1].append(
                [fzf_path, "-f", q, "--print-query", "--print0", "--sync", *fzfargs]
            )
    allres = []
    for fio, q in zip(allfilepa, allqueries):
        allres.append(
            multi_subprocess(
                q[1],
                byteinput=q[0],
                shell=shell,
                close_fds=close_fds,
                start_new_session=start_new_session,
                bufsize=bufsize,
                invisible=invisible,
                timeout=timeout,
                max_threads=max_threads,
                timeout_check_sleep=timeout_check_sleep,
                kill_all_at_end=kill_all_at_end,
                blockbatch=blockbatch,
            )
        )
        for key in list(allres[-1].keys()):
            allres[-1][key]["filepath"] = fio

    alldfs = []
    for i in range(len(allres)):
        alldfs.append(
            pd.concat(
                pd.DataFrame(allres[i].items())
                .apply(
                    lambda x: pd.DataFrame(x[1].items())
                    .set_index(0)
                    .T.assign(cmd=[x[0]]),
                    axis=1,
                )
                .to_list(),
                ignore_index=True,
            )
        )

    df = pd.concat(alldfs, ignore_index=True)

    df = df.drop(columns=["stdout", "stderr", "proc"])
    df["searchstring"] = df.cmd.str[3]
    df = df.drop(columns=["start", "cmd"]).rename(
        columns={"stdoutready": "stdout", "stderrready": "stderr"}
    )
    ra = pd.concat(
        [
            df,
            df.apply(
                lambda x: list(
                    flatten_everything(
                        [
                            (ProtectedList((q.split(b" | "))), q) if i == 0 else [q]
                            for i, q in enumerate(x.stdout.split(b"\x00", maxsplit=1))
                        ]
                    )
                ),
                axis=1,
                result_type="expand",
            ).rename(columns={0: "searchbinsplit", 1: "searchbin", 2: "match"}),
        ],
        axis=1,
    )
    df = ra.explode("searchbinsplit")
    rapiddf = df.apply(
        lambda x: fuzz.partial_ratio_alignment(x.match, x.searchbinsplit),
        axis=1,
        result_type="expand",
    ).rename(
        columns={
            0: "score",
            1: "src_start",
            2: "src_end",
            3: "dest_start",
            4: "dest_end",
        }
    )
    df = pd.concat([df.drop(columns="stdout"), rapiddf], axis=1)
    df.searchbinsplit = df.searchbinsplit.__array__().astype("S")
    df.searchbin = df.searchbin.__array__().astype("S")
    df.match = df.match.__array__().astype("S")
    df.filepath = df.filepath.astype("category")
    df.src_start = df.src_start.astype("Int64")
    df.src_end = df.src_end.astype("Int64")
    df.dest_start = df.dest_start.astype("Int64")
    df.dest_end = df.dest_end.astype("Int64")
    df.searchstring = df.searchstring.astype("category")
    df.stderr = df.stderr.astype("S")
    df.returncode = df.returncode.astype(np.uint8)

    df["match_detail"] = df.apply(lambda x: x["match"][x.src_start : x.src_end], axis=1)
    df.match_detail = df.match_detail.astype("S")

    return df.filter(
        [
            "searchbinsplit",
            "score",
            "searchbin",
            "match_detail",
            "filepath",
            "match",
            "src_start",
            "src_end",
            "dest_start",
            "dest_end",
            "searchstring",
            "stderr",
            "returncode",
        ]
    ).copy()
