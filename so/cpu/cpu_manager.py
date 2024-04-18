import threading
import time
from queue import Queue, PriorityQueue

class CPUManager:
    def __init__(self, gui=None):
        self.gui = gui
        self.algorithm = "FCFS"
        self.queues = {
            "FCFS": Queue(),
            "SJF": PriorityQueue(),
            "Priority": PriorityQueue(),
            "Lottery": Queue()  # Placeholder para implementação futura
        }
        self.queue = self.queues[self.algorithm]
        self.cores = [threading.Thread(target=self.worker, args=(i,)) for i in range(4)]
        self.active_processes = []

    def set_algorithm(self, alg):
        self.algorithm = alg
        self.queue = self.queues[alg]  # Altera a fila ativa com base no algoritmo selecionado

    def worker(self, core_id):
        while True:
            if self.algorithm in ["Priority", "SJF"]:
                priority, process = self.queue.get(block=True)
            else:
                process = self.queue.get(block=True)

            if process is None:
                break

            if process not in self.active_processes:
                self.active_processes.append(process.id)

            self.execute_process(process, core_id)

    def execute_process(self, process):
        self.gui.add_log(f"Processo {process.id} selecionado para execução.")
        subprocesses = process.get_sub_processes()
        total_subprocesses = len(subprocesses)
        current_subprocess = 0

        while current_subprocess < total_subprocesses:
            threads = []
            for i in range(4):
                if current_subprocess < total_subprocesses:
                    sp = subprocesses[current_subprocess]
                    thread = threading.Thread(target=self.process_subprocesses, args=([sp], i))
                    threads.append(thread)
                    thread.start()
                    current_subprocess += 1
            for thread in threads:
                thread.join()
        self.gui.add_log(f"Todos os subprocessos de {process.id} foram finalizados")
        self.gui.memory_manager.write_using_paging(process)
        self.gui.update_memory_display()

    def process_subprocesses(self, subprocesses, core_id):
        for sp in subprocesses:
            self.start_clock()
            self.gui.add_log(f"Core {core_id + 1}: Executando {sp.id}")
            self.gui.memory_manager.write_using_paging(sp)
            self.gui.update_memory_display()
            self.end_clock()
            self.gui.add_log(f"Core {core_id + 1}: {sp.id} concluído")



    def start_clock(self):
        self.gui.add_log("Clock começou.")
        time.sleep(0.5)  # Simula um clock de 500ms
    def end_clock(self):
        self.gui.add_log("Clock finalizou.")

    def add_process(self, process):
        if self.algorithm == "FCFS":
            self.queue.put(process)
        elif self.algorithm == "Priority":
            priority_level = {'Crítica': 1, 'Média': 2, 'Baixa': 3}
            priority = priority_level.get(process.priority, 3)
            self.queue.put((priority, process))
        elif self.algorithm == "SJF":
            job_length = len(process.get_sub_processes())
            self.queue.put((job_length, process))
        else:
            self.queue.put(process)

        if self.gui:
            self.gui.add_log(f"Processo {process.id} adicionado à fila usando algoritmo {self.algorithm}.")

    def run(self):
        while not self.queue.empty():
            if self.algorithm in ["Priority", "SJF"]:
                _, process = self.queue.get()
            else:
                process = self.queue.get()
            self.execute_process(process)

        self.finalize()  # É finalizado quando não há mais processos na fila

    def finalize(self):
        self.gui.add_log("Todos os processos foram processados.")
        [self.queue.put(None) for _ in range(4)]  # Parar o worker
        self.gui.add_log("Sistema Finalizado")
        self.stop()

    def stop(self):
        for core in self.cores:
            core.join()

