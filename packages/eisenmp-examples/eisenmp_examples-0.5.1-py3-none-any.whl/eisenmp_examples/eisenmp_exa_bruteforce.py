"""Generator module, Worker in /worker folder

Mandatory:
- import eisenmp
- worker must have the 'toolbox' (kwargs) as arg in entry function (arg count 1)
- path to worker module and the entry function reference, all are str

"""
import math
import os
import io
import time
from zipfile import ZipFile

import eisenmp
import eisenmp.utils.eisenmp_utils as e_utils

try:
    from eisenmp.utils_exa.eisenmp_search import SearchStr
    from eisenmp.utils_exa.eisenmp_download import DownLoad
    import eisenmp.utils_exa.eisenmp_utils as utils_exa
except ImportError:
    from eisenmp_examples.utils_exa.eisenmp_search import SearchStr
    from eisenmp_examples.utils_exa.eisenmp_download import DownLoad
    import eisenmp_examples.utils_exa.eisenmp_utils as utils_exa

dir_name = os.path.dirname(__file__)  # absolute dir path


class ModuleConfiguration:
    """
    | Loading the worker module has nothing to do with name resolution in 'this' module.
    | We can load from network share.

    | We have full access to all queues and methods. eisenmp = eisenmp.Mp()
    | We can transfer as much variable values to the worker as we want. Smaller is better. Spawn start copies values.

    """
    # path to worker module and entry function reference, worker module import in [isolated] process environment
    # -------------------- MANDATORY WORKER STRINGS (large worker live in /worker) --------------------
    bruteforce_module = {
        'worker_path': os.path.join(dir_name, 'worker', 'eisenmp_exa_wrk_bf_bruteforce.py'),
        'worker_ref': 'worker_entrance',
    }
    list_reducer_module = {
        'worker_path': os.path.join(dir_name, 'worker', 'eisenmp_exa_wrk_bf_reduce.py'),
        'worker_ref': 'worker_entrance',
    }
    lang_dicts_paths = [
        r'.\lang_dictionaries\ger\german.dic',
        r'.\lang_dictionaries\eng\words.txt'
    ]

    lang_dicts_url_zip_dct = {

        'https://github.com/44xtc44/eisenmp_examples/raw/dev/eisenmp_examples/lang_dictionaries/ger/german.zip':
            'german.dic',
        'https://github.com/44xtc44/eisenmp_examples/raw/dev/eisenmp_examples/lang_dictionaries/eng/SCOWL-wl.zip':
            'words.txt',
    }

    def __init__(self):
        # load order list, first module is called in an endless loop, you can append your own loop inside the worker
        self.worker_modules = []  # this example sets it later in `worker_module_set`

        # Multiprocess vars - override default
        # self.PROCS_MAX = 2  # your process count, default is None: one proc/CPU core
        # self.ROWS_MAX = 50_000  # your workload spread, list (generator) to calc in one loop, default None: 1_000
        self.RESULTS_STORE = True  # keep in dictionary, will crash the system if store GB network chunks in mem
        self.RESULTS_PRINT = True  # result rows of output are collected in a list, display if processes are stopped
        self.RESULTS_DICT_PRINT = True  # shows content of results dict with ticket numbers, check tickets
        # self.START_METHOD = 'fork'  # 'spawn' is default if unused; also use 'forkserver' or 'fork' on Unix only

        # Worker part - toolbox vars survive multiple worker calls
        self.multi_tool_get = None  # custom var to allow only one download of MULTI_TOOL; init later in this example
        self.MULTI_TOOL = None  # pre-defined toolbox.MULTI_TOOL can host the dict from mp_tools_q

        self.INFO_ENABLE = True  # info thread collects list row count, makes sense if no instances start overlapped
        self.INFO_THREAD_MAX = None  # target value for info thread to calculate % and ETA if 'enable_info' set

        # custom
        self.use_file_system = False  # False: download and unzip in mem        ------------ SWITCH --------------------
        self.result_lbl = None  # set by caller
        self.num_lists = 0  # add one for each list done, print out worker
        self.lowercase = True
        self.url = None  # 'use_file_system' False, URL of csv file
        self.zipped_filename = None  # None: have to loop over two archives; name of the uncompressed file in zip arch.
        self.str_permutation = None  # the search string we want to find in the dictionary/wordlist
        # instance creation overlaps if shrink on; info thread dev needs full length wordlist and sequence on mp_info_q
        self.shrink_wordlist = False   # shrink wordlist to len(search_str) is much faster


modConf = ModuleConfiguration()  # accessible in module
searchStr = SearchStr()


def load_lang_word_dict():
    """Load dictionaries from disk or gitHub"""
    word_dicts_file_system_load() if modConf.use_file_system else word_dicts_git_hub_load()


def start_raid():
    """
    - Manager -

    Decide raid tactics.
    Brute force on smaller strings. List reduce attempt for larger strings.

    Grab config values and push it to the two possible functions.

    - (A) len(String) <=  10, combined brute force dictionary attack.
    - (B) len(String) >=  11, Reduce a dictionary len(str) condensed list and count characters.

    See `mp_brute_force` and `mp_reduce` for more info.
    """
    modConf.str_permutation = searchStr.search_string
    if modConf.lowercase:
        modConf.str_permutation = modConf.str_permutation.lower()

    shrink = True if modConf.shrink_wordlist else False
    searchStr.word_dict_size(shrink, lowercase=modConf.lowercase)  # shrink remove words != len(search str)
    modConf.INFO_THREAD_MAX = math.factorial(len(modConf.str_permutation))  # info thread calc rows done and len

    # ---------- selection of generator function reference, no () ----------
    brute_force = True if len(modConf.str_permutation) <= 10 else False
    function_ref = mp_brute_force if brute_force else mp_reduce  # decide which function to call
    worker_module_set(function_ref)

    msg_b, msg_r = f'\n\t[BRUTE_FORCE]\t{modConf.str_permutation}', f'\n\t[LIST_REDUCTION]\t{modConf.str_permutation}'
    msg = msg_b if function_ref == mp_brute_force else msg_r
    print(msg)

    generator = function_ref(searchStr)  # `mp_brute_force` or `mp_reduce`
    words_dict = searchStr.words_dict if function_ref == mp_brute_force else None

    emp = eisenmp.Mp()
    emp.start(**modConf.__dict__)

    if brute_force:
        for _ in emp.proc_list:
            emp.mp_tools_q.put(words_dict)
    emp.run_q_feeder(generator=generator, input_q=emp.mp_input_q)
    return emp


def rt_loader():
    """rainbow table
    test if dict is only hosted in parent proc, if spawn
    """
    file_bin = bytearray()
    i = 0
    with open(r'f:\w.iso', 'rb') as bin_reader:
        while 1:
            if not (i % 100):
                print('.', end="", flush=True)
            chunk = bin_reader.read(io.DEFAULT_BUFFER_SIZE)
            if not chunk:
                print('\n')
                break
            file_bin += chunk
            i += 1
    rt_dct = {'rt': file_bin}
    return rt_dct


def worker_module_set(function_ref):
    """which worker module and function to load"""
    modConf.worker_modules = []  # del existing

    if function_ref == mp_brute_force:
        modConf.multi_tool_get = True
        modConf.worker_modules.append(modConf.bruteforce_module)
    else:
        modConf.multi_tool_get = False
        modConf.worker_modules.append(modConf.list_reducer_module)


def mp_brute_force(search_instance):
    """Generator Part

    - Worker 1 - only one worker is active at any time

    Produce str permutations for len(str), if len(str) = 3 we have 3! = 6 permutations
    Have a string and two tools. (A) wordlist as a dict and (B) itertools permutation generator.
    Searched string is hiding in the permutations.
    Check if the permutation makes sense and compare it with the wordlist.
    """
    generator = search_instance.generator(lowercase=modConf.lowercase)  # itertools
    return generator


def mp_reduce(search_instance):
    """
    - Worker 2

    Took all language word list and put them in a dict.
    Deleted all words with more or less characters.

    Worker will now reduce the list generated from dict.
    Remove all words not matching characters and
    character count in search str from list.
    Worker puts result in output q.
    """
    generator = (word for word in search_instance.words_dict)  # generator expression; pre reduced in searchString;
    return generator


def word_dicts_file_system_load():
    """
    - Entry ZIP FS

    """
    extract_zip_wordlists()
    searchStr.create_key_word_val_none_dict(modConf.lang_dicts_paths, lowercase=modConf.lowercase)


def extract_zip_wordlists():
    """File system unzip.
    """
    dicts_ger_zip = os.path.join(dir_name, 'lang_dictionaries', 'ger', 'german.zip')
    dicts_eng_zip = os.path.join(dir_name, 'lang_dictionaries', 'eng', 'SCOWL-wl.zip')
    zip_lst = [dicts_ger_zip, dicts_eng_zip]
    for zip_file in zip_lst:
        with ZipFile(zip_file, 'r') as un_zip:
            un_zip.extractall(os.path.dirname(zip_file))


def word_dicts_git_hub_load():
    """
    - Entry ZIP load URL

    """
    downloader = DownLoad()
    mem_word_lst = []

    for url, in_zip in modConf.lang_dicts_url_zip_dct.items():
        modConf.url = url
        modConf.zipped_filename = in_zip
        wordlist_download(downloader)  # stored the response object
        mem_word_lst.extend(wordlists_in_memory(downloader))  # download the zip archive, open one file, return txt file

    if modConf.lowercase:  # store the word list in searchStr instance with lowercase if set {'ethic': None}
        # .rstrip() else single chars, later in shrink method of searchStr
        searchStr.loader_words_dict = {word.lower().rstrip(): None for word in mem_word_lst}
        pass
    else:
        searchStr.loader_words_dict = {word.rstrip(): None for word in mem_word_lst}
    pass


def wordlists_in_memory(downloader):
    """Open zip archive and load one file 'zipped_filename'
    Return as text.
    """
    archive = downloader.unzip_mem()
    # text files are all utf-8 encoded, else python tries to open cp1252 format on german windows
    with io.TextIOWrapper(archive.open(modConf.zipped_filename, 'r'), encoding="UTF-8") as file:
        txt_lst = file.readlines()
    return txt_lst


def wordlist_download(downloader):
    """Store response object in downloader instance.
    We could show dots during download, or open in binary, or csv, or ....
    """
    downloader.url = modConf.url
    downloader.zipped_filename = modConf.zipped_filename
    print(downloader.url)
    downloader.load_url()


def start_raid_sequential():
    """Blocks creation of a new instance,
    else next instance starts while previous instances runs
    """
    emp = start_raid()
    while 1:
        if emp.begin_proc_shutdown:
            break
        time.sleep(.1)


def main():
    """
    """
    str_list_alphabet_salad = [
        'AMGNO',
        'AACEFHKLMSS',
        'DIKKLOOR', 'BEEINNRST',
        'CEEHNNRST', 'EEHINORST',
        'EEEFFIKORRS', 'CFHHILORRS'
    ]

    start = time.perf_counter()

    utils_exa.empty_db_from_schema()  # collect exit msg (search string alphabet) from instances
    load_lang_word_dict()
    msg_result = e_utils.Result.result_dict  # shown in browser if example server is started

    for idx, string in enumerate(str_list_alphabet_salad):
        searchStr.search_string = string
        modConf.result_lbl = string
        modConf.lowercase = True

        modConf.shrink_wordlist = True  # either start_raid or start_raid_sequential
        start_raid() if modConf.shrink_wordlist else start_raid_sequential()  # else block instantiate

    while 1:
        # need a database for asking done; some instances may return earlier than other
        title_lst = utils_exa.table_select_column('exa', 'title')
        done = all(item in title_lst for item in str_list_alphabet_salad)

        if done:
            break
        time.sleep(1)

    print(f'bruteforce time: {round((time.perf_counter() - start))}')
    return msg_result


if __name__ == '__main__':
    main()
