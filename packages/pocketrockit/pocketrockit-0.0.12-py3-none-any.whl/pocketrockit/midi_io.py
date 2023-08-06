#!/usr/bin/env python3

"""Stuff needed to communicate with MIDI devices
"""

import logging
import time
from collections.abc import Iterable
from contextlib import contextmanager, suppress

import fluidsynth
import pygame.midi


def logger() -> logging.Logger:
    """Named logger"""
    return logging.getLogger("pr.midi_io")


def choose(choices: Iterable[str], *wishlist: str) -> str:
    """Choose from a list of strings until we found someting matching"""
    for wish in wishlist:
        with suppress(StopIteration):
            return next(name for name in choices if wish in name)
    raise KeyError(f"{wishlist}")


# def read_midi(loop, event_queue, terminator):
# logger().debug(">> read_midi")

# try:
# available_input_ports = set(mido.get_input_names())
# logger().info("Available MIDI input ports: \n%s", "  \n".join(available_input_ports))

# chosen_input = choose(
# available_input_ports, "OP-1", "Sylphyo", "USB MIDI Interface", "Midi Through"
# )
# logger().info("Chosen: %r", chosen_input)

# with mido.open_input(chosen_input) as inport:
# while not terminator.is_set():
# if (event := inport.receive()).type == "clock":
# continue
# asyncio.run_coroutine_threadsafe(event_queue.put(event), loop=loop)
# logger().debug("read_midi: got termination signal")

# except Exception as exc:
# logger().error("Unhandled exception in read_midi thread: %s", exc)

# logger().debug("<< read_midi")


@contextmanager
def midi_output_pygame():
    """
    fluidsynth -vv -a pipewire -z 256 -g 2 FluidR3_GM.sf2
    """
    try:
        pygame.midi.init()
        for i in range(pygame.midi.get_count()):
            print(pygame.midi.get_device_info(i))
        player = pygame.midi.Output(2)
        player.set_instrument(0)
        yield player
    finally:
        del player
        pygame.midi.quit()


@contextmanager
def midi_output_fluidsynth():
    """
    Todo: make behave like subprocess
    """
    try:
        midi_out = fluidsynth.Synth(gain=2.0, samplerate=44100.0)
        midi_out.setting("audio.period-size", 256)
        midi_out.start(driver="pulseaudio")
        fluid = midi_out.sfload("FluidR3_GM.sf2")
        for i in range(128):
            midi_out.program_select(i, fluid, 0, i)
        midi_out.program_select(128, midi_out.sfload("JV_1080_Drums.sf2"), 128, 0)
        yield midi_out
    finally:
        midi_out.delete()


def midi_output_device(name: str):
    return midi_output_fluidsynth()


def device_id(choices: Iterable[str]):

    input_devices = {
        i: bname.decode()
        for i in range(pygame.midi.get_count())
        for _, bname, is_input, *_, in (pygame.midi.get_device_info(i),)
        if is_input
        if any(c.lower() in bname.decode().lower() for c in choices)
    }
    print(input_devices)

    input_device_id = None
    for c in choices:
        for dev_id, dev_name in input_devices.items():
            if c.lower() in dev_name.lower():
                return dev_id


def midi_input_pygame(choices: Iterable[str], event_queue, terminator) -> None:
    try:
        pygame.midi.init()

        if (input_device_id := device_id(choices)) is None:
            logger().info("No MIDI devices attached")
            return

        input_device = pygame.midi.Input(input_device_id)
        while not terminator.is_set():
            if not input_device.poll():
                time.sleep(0.01)
                continue
            for status, d1, d2, d3, tick in (
                (*data, tick) for data, tick in input_device.read(100) if data != (248, 0, 0, 0)
            ):
                print(status, d1, d2, d3, tick)
    finally:
        pygame.midi.quit()


def midi_input_device(name: str, choices, event_queue, terminator) -> None:
    midi_input_pygame(choices=choices, event_queue=event_queue, terminator=terminator)
