import os
from src.MessageSeverity import MessageSeverity
from src.Writer import Writer
from mysql.connector.pooling import MySQLConnectionPool


class LoggerService:

    def __init__(self):
        self._pool = MySQLConnectionPool(
            user=os.getenv('RDS_USERNAME'),
            password=os.getenv('RDS_PASSWORD'),
            host=os.getenv('RDS_HOSTNAME'),
            database=os.getenv('RDS_DB_NAME'),
            pool_name="loggerPool",
            pool_size=5
        )
        self._writer = Writer(self._pool)

    def log(self, *args, **kwargs):
        if args:
            self._writer.add_message(args[0], MessageSeverity.Information.value)
        else:
            if 'object' in kwargs:
                kwargs['object']['severity_id'] = MessageSeverity.Information.value
                self._writer.add(**kwargs)

    def error(self, *args, **kwargs):
        if args:
            self._writer.add_message(args[0], MessageSeverity.Error.value)
        else:
            if 'object' in kwargs:
                kwargs['object']['severity_id'] = MessageSeverity.Error.value
                self._writer.add(**kwargs)

    def warn(self, *args, **kwargs):
        if args:
            self._writer.add_message(args[0], MessageSeverity.Warning.value)
        else:
            if 'object' in kwargs:
                kwargs['object']['severity_id'] = MessageSeverity.Warning.value
                self._writer.add(**kwargs)

    def debug(self, *args, **kwargs):
        if args:
            self._writer.add_message(args[0], MessageSeverity.Debug.value)
        else:
            if 'object' in kwargs:
                kwargs['object']['severity_id'] = MessageSeverity.Debug.value
                self._writer.add(**kwargs)

    def verbose(self, *args, **kwargs):
        if args:
            self._writer.add_message(args[0], MessageSeverity.Verbose.value)
        else:
            if 'object' in kwargs:
                kwargs['object']['severity_id'] = MessageSeverity.Verbose.value
                self._writer.add(**kwargs)