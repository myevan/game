# -*- coding:utf8 -*-
import logging
import subprocess
import contextlib
import os

from ..base.error import Error

class ShellError(Error):
    def __init__(self, name, args, exit_code, error_text=""):
        super(Shell.Error, self).__init__(name)
        self.msg = msg
        self.args = args
        self.exit_code = exit_code
        self.error_text = error_text

    def __str__(self):
        if self.error_text:
            if '\n' in self.error_text:
                tail = f"\n{self.error_text}"
            else:
                tail = f":{self.error_text}"
        else:
            tail = ""

        return f"{self.__class__.__name__}<{self.name}>(args={self.args}, msg='{self.msg}', exit_code={self.exit_code}){tail}"

class Shell(object):
    def call(self, args):
        logging.debug("shell.call:{0}".format(str(args)))

        exit_code = subprocess.call(args)
        if exit_code:
            raise ShellError('CALL', args, exit_code)

    def read_pipe(self, args, ignore_error=False):
        logging.debug("shell.read_pipe:{0}".format(' '.join(args)))

        proc = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=isinstance(args, str))

        output, error = proc.communicate()
        if proc.returncode != 0 and not ignore_error:
            raise ShellError('READ_PIPE', args, proc.returncode)

        return output

    def write_pipe(self, args, data):
        logging.debug("shell.write_pipe:{0}".format(str(args)))

        proc = subprocess.Popen(
            args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=isinstance(args, str))

        proc.stdin.write(data)
        proc.stdin.close()
        if proc.wait():
            error_text = proc.stderr.read()
            raise ShellError('WRITE_PIPE', args, proc.returncode, error_text)

        return proc.stdout.read()

    def abort(self, msg):
        raise Exception(msg)

    @contextlib.contextmanager
    def pushd(self, new_dir):
        prv_dir = os.getcwd()
        os.chdir(new_dir)
        yield
        os.chdir(prv_dir)
