
import logging
from aiosow.bindings import make_async, on, setup
from aiosow.routines import routine, spawn_consumer

on('command')
def get_input(*__args__, **__kwargs__) -> dict:
    logging.info('get_input')
    return { 'command': 'foo' }

routine(2, life=2, repeat=False)(lambda : { "command": "" })
