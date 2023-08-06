from __future__ import print_function
from runfalconbuildtools.command_line_executor import CommandLineExecutor

def test_execute_ok_with_args():
    executor:CommandLineExecutor = CommandLineExecutor()
    executor.execute('ls', ['-l'])
    print(' >>>>> test_execute_ok_with_args OUT: {}'.format(executor.stdout))
    assert executor.return_code == 0

def test_execute_ok_no_args():
    executor:CommandLineExecutor = CommandLineExecutor()
    executor.execute('ls')
    assert executor.return_code == 0

def test_execute_error():
    executor:CommandLineExecutor = CommandLineExecutor()
    executor.execute('lsX', ['-l'])
    print(' >>>>> test_execute_error ERROR {}'.format(executor.stderr))
    print(' >>>>> test_execute_error OUT {}'.format(executor.stdout))
    assert executor.return_code != 0

def test_execute_script_from_string_ok():
    executor:CommandLineExecutor = CommandLineExecutor()
    script:str = '#!/bin/sh\nset -e\nls -l'
    executor.execute_script(script)
    print(' >>>>> test_execute_script_from_string_ok OUT {}'.format(executor.stdout))
    print(executor.stderr)
    assert executor.return_code == 0