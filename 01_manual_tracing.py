from time import sleep
import logfire

# With kwargs:
logfire.configure()


logfire.info('Hello {name}', name='world')

activity = 'work'
with logfire.span('doing some slow {activity}...', activity=activity):
    logfire.info('{fruit=}', fruit='banana')
    sleep(0.123)
    with logfire.span('more nesting'):
        status = 'ominous'
        logfire.warn('this is {status}', status=status)
        sleep(0.456)
        logfire.info('done')


# With f-strings:
name = 'world'
logfire.info(f'Hello {name}')

activity = 'work'
with logfire.span(f'doing some slow {activity}...'):
    fruit = 'banana'
    logfire.info(f'{fruit=}')
    sleep(0.123)
    with logfire.span('more nesting'):
        status = 'ominous'
        logfire.warn(f'this is {status}')
        sleep(0.456)
        logfire.info('done')
