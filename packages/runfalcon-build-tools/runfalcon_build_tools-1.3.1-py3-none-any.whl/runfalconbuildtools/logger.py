from datetime import datetime

class Logger:

    def __init__(self, owner:str):
        self.owner = owner

    def __get_log_message(self, type:str, message:str) -> str:
        now = datetime.now()
        msg:str = now.strftime("%d/%m/%Y %H:%M:%S")
        msg += ' ({owner})'.format(owner = self.owner)
        msg += ' - [{msg_type}]'.format(msg_type = type)
        msg += ' :: {the_message}'.format(the_message = message)
        return msg

    def __print_message(self, message:str):
        print(message)

    def debug(self, message:str):
        self.__print_message(self.__get_log_message('debug', message))

    def info(self, message:str):
        self.__print_message(self.__get_log_message('info', message))

    def warn(self, message:str):
        self.__print_message(self.__get_log_message('warn', message))

    def error(self, message:str):
        self.__print_message(self.__get_log_message('error', message))
        
    def error(self, message:str, error:any):
        self.__print_message(self.__get_log_message('error', message + '\n' + str(error)))
