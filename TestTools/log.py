import logging
import os
import threading
from TestTools import getinfo
# import readConfig

upPath = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class Log:
    def __init__(self):
        global logPath, resultPath, proDir
        resultPath = os.path.join(upPath, "TestResult")
        # create result file if it doesn't exist
        if not os.path.exists(resultPath):
            os.mkdir(resultPath)
        # defined test result file name by localtime
        logPath = os.path.join(resultPath, getinfo.get_date())
        # create test result file if it doesn't exist
        if not os.path.exists(logPath):
            os.mkdir(logPath)
        # defined logger
        self.logger = logging.getLogger()
        # defined log level
        self.logger.setLevel(logging.INFO)

        # write log file
        # defined handler
        handler = logging.FileHandler(os.path.join(logPath, "output.log"), encoding="utf-8")
        # defined formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # defined formatter
        handler.setFormatter(formatter)
        # add handler
        self.logger.addHandler(handler)

        # print on console
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        self.logger.addHandler(console)

    def get_logger(self):
        return self.logger

    def build_start_line(self, case_name):
        self.logger.info("--------" + case_name + " START--------")

    def build_end_line(self, case_name):
        self.logger.info("--------" + case_name + " END--------")

    def build_case_line(self, case_name, code, msg):
        self.logger.info(case_name + " - Code: " + code + " - Msg: " + msg)

    def get_report_path(self):
        """
        get report file path
        :return:
        """
        report_path = os.path.join(logPath, "report.html")
        return report_path

    def get_result_path(self):
        """
        get test result path
        :return:
        """
        return logPath

    def write_result(self, result):
        """

        :param result:
        :return:
        """
        result_path = os.path.join(logPath, "report.txt")
        fb = open(result_path, "wb")
        try:
            fb.write(result)
        except FileNotFoundError as ex:
            self.logger.error(str(ex))


class MyLog:
    log = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_log():

        if MyLog.log is None:
            MyLog.mutex.acquire()
            MyLog.log = Log()
            MyLog.mutex.release()

        return MyLog.log

