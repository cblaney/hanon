
import mido
import warnings
import time


def getMidiFile(filepath):
    mid = mido.MidiFile(filepath)
    return mid

def printMidi(midi):
    for i, track in enumerate(midi.tracks):
        print('Track {}: {}'.format(i, track.name))
        for msg in track:
            print(msg)

def playMidi(midi, port):
    try:
        print(f"Playing MIDI with port: {port}")
        for msg in midi.play():
            port.send(msg)
            # print(msg)
    except KeyboardInterrupt:
        print("Playback interrupted")
    finally:
        port.reset()

def getMidiInput(hint):
    ports = mido.get_input_names()
    for port in ports:
        if port.find(hint) >= 0:
            return mido.open_input(port)

    # Can not find Hint
    port = mido.open_input()
    warnings.warn(f"Could not find input port with hint: {hint}.  Opening Default port: {port}")
    return port

def getMidiOutput(hint):
    ports = mido.get_output_names()
    for port in ports:
        if port.find(hint) >= 0:
            return mido.open_output(port)

    # Can not find Hint
    port = mido.open_output()
    warnings.warn(f"Could not find input port with hint: {hint}.  Opening Default port: {port}")
    return port

buff = []
def on_message(msg):
    msg.time = time.time()
    buff.append(msg)
    # print(msg)

def readMidi(port):
    port.callback = on_message
    print("Listening for MIDI input...")
    input("Press Enter to stop\n")
    port.callback = None

import concurrent.futures

if __name__ == "__main__":
    print('Hello!')
    # Initialize MIDI device
    # Testing using VMPK
    inport = getMidiInput("VMPK")
    outport = getMidiOutput("VMPK")

    # Get Midi File
    # Testing using Hanon 1
    midifile = getMidiFile('/home/clb/PycharmProjects/PyHanon/Exercise 1.mid')

    pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    # Play
    pool.submit(playMidi, midifile, outport)
    # Read
    pool.submit(readMidi, inport)

    pool.shutdown(wait=True)

    inport.close()
    outport.close()

    print('Goodbye!')
