"""
Library Test File from mez64
"""

import logger as l
import asyncio
from pyeight.eight import EightSleep
import env


@asyncio.coroutine
def update_device(loop, device):
    while True:
        yield from device.update_device_data()
        device_info(device)

        yield from asyncio.sleep(60, loop)


@asyncio.coroutine
def update_user(loop, device):
    while True:
        yield from device.update_user_data()
        user_info(device)

        yield from asyncio.sleep(60*5, loop)


def user_info(device):
    for user in device.users:
        obj = device.users[user]

        print('{} User Current Sleep Score: {}'.format(
            obj.side, obj.current_sleep_score))
        # print('{} User Current Sleep Breakdown: {}'.format(obj.side, obj.current_sleep_breakdown))
        # print('{} User Current Sleep Stage: {}'.format(obj.side, obj.current_sleep_stage))
        # print('{} User Current Toss&Turns: {}'.format(obj.side, obj.current_tnt))
        # print('{} User Current Bed Temp: {}'.format(obj.side, obj.current_bed_temp))
        # print('{} User Current Room Temp: {}'.format(obj.side, obj.current_room_temp))
        # print('{} User Current Resp Rate: {}'.format(obj.side, obj.current_resp_rate))
        # print('{} User Current Heart Rate: {}'.format(obj.side, obj.current_heart_rate))

        # print('{} User Last Session Date: {}'.format(obj.side, obj.last_session_date))
        # print('{} User Last Sleep Score: {}'.format(obj.side, obj.last_sleep_score))
        # print('{} User Last Sleep Breakdown: {}'.format(obj.side, obj.last_sleep_breakdown))

        _LOG.debug('%s User Current: %s', obj.side, obj.current_values)
        _LOG.debug('%s User Last: %s', obj.side, obj.last_values)


def device_info(device):
    for user in device.users:
        obj = device.users[user]
        print('{} User Heat Level: {}'.format(obj.side, obj.heating_level))
        # print('{} User Heat Remaining: {}'.format(obj.side, obj.heating_remaining/3600))

        _LOG.debug('%s User Heating: %s', obj.side, obj.heating_values)
        _LOG.debug('%s User In Bed: %s', obj.side, obj.presence)

        heat_hist = []
        for i in range(0, 5):
            heat_hist.append(obj.past_heating_level(i))
        _LOG.debug('%s User Heating History: %s', obj.side, heat_hist)


@asyncio.coroutine
def eight_test(loop):
    """Eight test."""
    _LOG.debug('Starting pyEight test.')

    eight = EightSleep(env.email, env.password,
                       'America/Denver', True, None, loop)

    yield from eight.start()

    print(eight.token)

    while True:
        yield from asyncio.wait((
            update_device(loop, eight),
            update_user(loop, eight)
        ))

    yield from eight._api_session.close()


def main():
    """ Do main things.. """

    # This will server to mimic the HASS loop that we will pass in.
    hassloop = asyncio.get_event_loop()

    try:
        hassloop.run_until_complete(eight_test(hassloop))
    except KeyboardInterrupt:
        # Optionally show a message if the shutdown may take a while
        print("Attempting graceful shutdown…", flush=True)

        # Do not show `asyncio.CancelledError` exceptions during shutdown
        # (a lot of these may be generated, skip this if you prefer to see them)
        def shutdown_exception_handler(loop, context):
            if "exception" not in context \
                    or not isinstance(context["exception"], asyncio.CancelledError):
                hassloop.default_exception_handler(context)
        hassloop.set_exception_handler(shutdown_exception_handler)

        # Handle shutdown gracefully by waiting for all tasks to be cancelled
        tasks = asyncio.gather(
            *asyncio.Task.all_tasks(loop=hassloop), loop=hassloop, return_exceptions=True)
        tasks.add_done_callback(lambda t: hassloop.stop())
        tasks.cancel()

        # Keep the event loop running until it is either destroyed or all
        # tasks have really terminated
        while not tasks.done() and not hassloop.is_closed():
            hassloop.run_forever()

    finally:
        hassloop.close()


if __name__ == '__main__':
    main()
