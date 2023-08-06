#!/usr/bin/env python3

"""POCKETROCKIT engine
"""

import asyncio
import concurrent
import logging
import threading
import time
from asyncio import sleep as async_sleep
from contextlib import ExitStack
from dataclasses import dataclass, field
from importlib.util import module_from_spec, spec_from_file_location
from itertools import count
from pathlib import Path
from types import ModuleType

from asyncinotify import Inotify, Mask

from .midi_io import midi_input_device, midi_output_device
from .misc import Singleton, colored, error, keyboard_reader, setup_logging, watchdog


@dataclass
class Env:
    """Some global environment"""

    bpm: int = 60


@dataclass
class Stage(metaclass=Singleton):
    """Access to the currently played music"""

    env: Env = field(default_factory=Env)
    active: bool = False
    players: list = field(default_factory=list)
    new_track: None | list = None
    file_to_track: str = ""
    tick: int = -1


def load_module(filepath: str | Path) -> ModuleType:
    """(Re)loads a python module specified by @filepath"""
    print(f"load module '{Path(filepath).stem}'")
    spec = spec_from_file_location(Path(filepath).stem, filepath)
    if not spec and spec.loader:
        raise RuntimeError("Could not load")
    module = module_from_spec(spec)
    assert module
    # here the actual track definition takes place
    spec.loader.exec_module(module)
    return module


@watchdog
async def music_loop() -> None:
    """Main loop collecting instructions to send it to MIDI"""
    with midi_output_device("fluidsynth") as midi_out:
        # wait for players to emerge (otherwise `tick` won't start at 0)
        while True:
            if Stage().players:
                break
            print("no players yet..")
            await async_sleep(1)
            continue

        for tick in count():
            last_now = time.time()
            Stage().tick = tick

            notes = []
            if tick % 1 == 0:
                print(f"== {tick // 16} {tick // 4} {tick % 4} {tick} ==")

            for name, stream in Stage().players:
                try:
                    source_loop, source_tick, origin, commands = next(stream)
                    if commands:
                        print(f"{name}: {source_loop}:{source_tick}:{origin} => {commands}")
                    if commands:
                        notes.extend(commands)
                except StopIteration:
                    pass
                except Exception as exc:  # pylint: disable=broad-except
                    error(f"exception in play: {exc}")

            for channel, note, velocity in notes:
                if velocity is None:
                    # print("OF", (channel, note))
                    midi_out.noteoff(channel, note)
                else:
                    # print("ON", (channel, note, velocity))
                    midi_out.noteon(channel, note, velocity)

            # make me absolute please
            waitfor = 60 / Stage().env.bpm / 4
            await async_sleep(max(0, (waitfor - (time.time() - last_now))))


@watchdog
async def watch_changes() -> None:
    """Watches for file changes in track definition file and reload on change"""
    stage = Stage()
    load_module(stage.file_to_track)
    with Inotify() as inotify:
        inotify.add_watch(
            Path(Stage().file_to_track).parent,
            Mask.CLOSE_WRITE,
        )
        async for event in inotify:
            print(event.path, event.mask)
            try:
                assert event.path
                load_module(event.path)
            except Exception as exc:  # pylint: disable=broad-except
                error(f"Caught {exc}")


def logger() -> logging.Logger:
    """Named logger"""
    return logging.getLogger("pr.engine")


@watchdog
async def handle_events(event_queue: asyncio.Queue, terminator):
    """Main event handler"""
    logger().debug(">> handle_events")
    try:
        while not terminator.is_set():
            try:
                event = await event_queue.get()
                if event.type in {pygame.WINDOWCLOSE, pygame.QUIT}:
                    logger().debug("quit/windowclose")
                    break
                elif event.type == pygame.MOUSEMOTION:
                    pass
                elif event.type == pygame.TEXTINPUT:
                    pass
                elif event.type == pygame.KEYDOWN:
                    pass
                elif event.type == pygame.KEYUP:
                    pass
                elif event.type == "note_on":
                    print("NOTEON", event)
                elif event.type == "note_off":
                    print("NOTEOFF", event)
                else:
                    logger().debug("event %s", event)
            except Exception as exc:  # pylint: disable=broad-except
                print(exc)
        logger().debug("handle_events: got termination signal")

    finally:
        logger().debug("<< handle_events")
        terminate(terminator)


def terminate(terminator) -> None:
    """Sends a signal to async tasks to tell them to stop"""
    try:
        terminator.set()
        time.sleep(0.2)
        asyncio.get_event_loop().stop()
        # pygame.event.post(pygame.event.Event(pygame.MOUSEMOTION))
        time.sleep(0.2)
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Got: {exc}")


@watchdog
async def handle_keyboard(loop, terminator):
    """Handles key press event"""
    try:
        async for key in keyboard_reader(loop, terminator):
            print(colored(key, "yellow"))
        print("Keyboard loop stopped - terminate program")
        terminate(terminator)
    except RuntimeError as exc:
        logger().debug("Could not run keyboard handler: %s", exc)


def run() -> None:
    """Runs the pocketrockit event loop forever"""
    setup_logging()

    event_queue: asyncio.Queue = asyncio.Queue()
    terminator = threading.Event()
    loop = asyncio.get_event_loop()

    with ExitStack() as block:
        pool = block.enter_context(concurrent.futures.ThreadPoolExecutor())

        loop.run_in_executor(
            pool,
            midi_input_device,
            "pygame",
            ["OP-1", "Sylphyo", "USB MIDI Interface", "Midi Through"],
            event_queue,
            terminator,
        )
        asyncio.ensure_future(handle_keyboard(loop, terminator))
        asyncio.ensure_future(handle_events(event_queue, terminator))
        asyncio.ensure_future(music_loop())
        asyncio.ensure_future(watch_changes())

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            logger().debug("KeyboardInterrput in main()")
        finally:
            terminate(terminator)
            logger().debug("finally - loop.run_forever()")
