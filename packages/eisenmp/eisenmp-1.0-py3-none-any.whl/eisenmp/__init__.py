"""

A Python ``multiprocess, multi CPU`` module.
An example function cracks a game quest.

::

    Inheritance - proc: ProcEnv -> QueueCollect -> Mp
        Create Queue/Process -> Collect messages in boxes -> Manage, feed queues

    Thread names are in ProcEnv:
        QueueCollect [print_q, output_q, input_q, tools_q, info_q],
        GhettoGang [view_output_q_box, tools_q feeder],
        [ProcInfo]

"""
import time
import threading

import eisenmp.utils.eisenmp_utils as e_utils
import eisenmp.utils.eisenmp_constants as const
from eisenmp.eisenmp_q_coll import QueueCollect


class Mp(QueueCollect):
    """MultiProcessManager.

    """

    def __init__(self):
        super().__init__()
        self.kwargs = None

    def start(self, **kwargs):
        """enable Processes and eisenmp worker threads.
        """
        self.reset()
        self.kwargs = kwargs
        self.run_proc(**kwargs)

        self.enable_q_box_threads()

        self.enable_info_q()  # never disable, else sender blocks, nobody consumes from q
        if 'INFO_ENABLE' in kwargs and kwargs['INFO_ENABLE']:
            self.enable_info_thread()  # collect worker send nums from info box and shows % and ETA
        return

    def reset(self):
        """"""
        self.all_threads_stop = False  # frequent calls without exit, see bruteforce
        self.begin_proc_shutdown = False  # frequent calls without exit, see bruteforce

    def run_q_feeder(self, **kwargs):
        """Threaded instance, run multiple q_feeder, called by manager of worker
        """
        self.kwargs.update(kwargs)  # upd kwargs with generator, queues and header_msg
        threading.Thread(name='eisenmp_q_feeder',  # better than class thread here, no overlap, interesting.
                         target=self.q_feeder,
                         ).start()

    def q_feeder(self):
        """Queue.
        Chunk list producer of generator input.

        - A ticket is attached as header to identify the workload (list chunks)
        - Serial number to rebuild the modified results in the right order
        """
        kw = self.kwargs
        generator = kw['generator']  # no generator for run_q_feeder, crash for sure
        rows_max = kw['ROWS_MAX'] if 'ROWS_MAX' in kw and kw['ROWS_MAX'] else const.ROWS_MAX  # processor workload
        feeder_input_q = kw['input_q'] if 'input_q' in kw else self.mp_input_q  # use default if not specified
        q_name = q_name_get(self.q_name_id_lst, feeder_input_q)

        start = time.perf_counter()
        num_gen = e_utils.consecutive_number()
        while 1:
            if self.all_threads_stop:
                break
            chunk_lst = create_transport_header(num_gen, q_name)
            for _ in range(rows_max):
                try:
                    chunk_lst.append(next(generator))
                except StopIteration:
                    chunk_lst.append(const.STOP_MSG)  # signal stop to one worker module, worker module 'loader' to many
                    self.mp_print_q.put(f'\n\tgenerator empty, '
                                        f'run time iterator {round((time.perf_counter() - start))} seconds\n')
                    self.q_input_put(feeder_input_q, chunk_lst)
                    return

            self.q_input_put(feeder_input_q, chunk_lst)

    def q_input_put(self, feeder_input_q, chunk_lst):
        while 1:
            if self.all_threads_stop:
                break
            if feeder_input_q.empty():
                feeder_input_q.put(chunk_lst)
                break


def q_name_get(q_name_id_lst, feeder_input_q):
    """Queue name must be assigned.
    Name will be dictionary key in result dict, dict in dict.
    Results are stored like so: {Queue_name: {__TID__1: [foo, bar], {__TID__2: [baz, boo]}}}.
    """
    q_name = ''  # result can be stored as dict[q_name] = {_TID_1: foo, _TID_2: bar}
    for tup in q_name_id_lst:
        name, q_id, _ = tup  # name id q_ref
        if q_id == id(feeder_input_q):  # find feeder_input_q in q_name_id_lst, unique Python id() for objects
            q_name = name
            break
    if not q_name:
        q_name = 'mp_input_q'
    return q_name


def create_transport_header(num_gen, q_name):
    """Semicolon to split easy.
    """
    ticket = q_name + ';' + const.TICKET_ID_PREFIX + f'{str(next(num_gen))};'  # ';_TID_1;'
    return [ticket]
