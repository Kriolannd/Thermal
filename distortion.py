import random
import os
import threading
from time import sleep
import logging
import datetime


class Process:
    def __init__(self, f1, f2, f4, f5, f6, f7):
        self.paramsline = None
        self.f4 = open(f4, 'r')
        self.f5 = open(f5, 'a')
        self.f2 = open(f2, 'r')
        self.f1 = open(f1, 'a')
        self.f7 = open(f7, 'a')
        self.f6 = open(f6, 'r')

        self.dt = 0.1
        self.step = 0
        self.true_state = 1
        self.changed_state = 1

    def _follow(self, f):
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line or line == "\n":
                sleep(self.dt)
                continue
            yield line

    def _process_line(self, line):
        return float(line.split(";")[1])

    def _write_f1(self, t_true, t_changed, state_true, state_changed):
        values = {
            'state_true': self.true_state,
            'temp_true': int(t_true),
            'temp_seeming': int(t_changed)
        }

        if state_true:
            values['change_state_true'] = 1

        if state_changed:
            values['change_state_done'] = 1

        line = 'time=' + str(self.step) + ' '
        self.step += 1

        for key, value in values.items():
            line += str(key) + '=' + str(value) + ' '

        self.f1.write(line + '\n')
        self.f1.flush()

    def start(self):
        # loglines = self._follow(self.f4)
        for line_f4 in self._follow(self.f4):
            for paramsline in self.f2:
                pass
            self.paramsline = paramsline
            true_temp = self._process_line(line_f4)
            sigma = float(self.paramsline.split(";")[0])
            changed_temp = random.gauss(true_temp, sigma)
            print("true_temp " + str(true_temp) + " changed_temp " + str(changed_temp) + " sigma " + str(sigma))
            self._write_f1(true_temp, changed_temp, 1, 1)
            logging.info(str(datetime.datetime.now().strftime("%m.%d.%Y %H:%M:%S.%f")) + ";" + str(changed_temp))
            print("t1 " + str(self.true_state))

    def switch_distortion(self):
        for line_f6 in self._follow(self.f6):
            # params = ""
            # for paramsline in self.f2:
            #     print(paramsline)
            #     params = paramsline
            #     pass
            # print("after loop: " + params)
            alpha = float(self.paramsline.split(";")[1])
            self.true_state = 0 if self.true_state == 1 else 1
            if random.random() > alpha:
                self.changed_state = 0 if self.changed_state == 1 else 1
                self.f7.write(line_f6)
                self.f7.flush()
            print("t2 " + str(self.true_state))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="F5.txt", filemode="a", format="%(message)s")
    # Process("F1.txt", "F2.txt", "F4.txt", "F5.txt", "F6.txt").start()

    p = Process("F1.txt", "F2.txt", "F4.txt", "F5.txt", "F6.txt", "F7.txt")
    t1 = threading.Thread(target=p.start)
    t2 = threading.Thread(target=p.switch_distortion)

    # starting thread 1
    t1.start()
    t2.start()
    t1.join()
