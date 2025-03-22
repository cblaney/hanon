
import mido
import warnings
import time


def getMidiFile(filepath, print_meta=False):
    mid = mido.MidiFile(filepath)
    if print_meta:
        print(f"Filename={mid.filename}")
        print(f"Type={mid.type}")
        print(f"Ticks Per Beat={mid.ticks_per_beat}")
        mid.print_tracks(meta_only=True)
    return mid

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

_buff = []
def on_message(msg):
    msg.time = time.time()
    _buff.append(msg)
    print(msg)

def readMidi(port):
    port.callback = on_message
    print(f"Listening for MIDI on: {port}")
    input("Press Enter to stop\n")
    port.callback = None

def messages2file(buffer, ticks_per_beat=480, tempo=500000):
    track = mido.MidiTrack()
    prevtime = buffer[0].time
    curtime = 0
    for msg in buffer:
        # Set msg.time to delta-time (dsec)
        curtime = msg.time 
        msg.time -=  prevtime
        prevtime = curtime

        # Convert Seconds to ticks
        msg.time = mido.second2tick(msg.time, ticks_per_beat, tempo)
        track.append(msg)

    file =  mido.MidiFile()
    file.tracks.append(track)
    return file


import concurrent.futures
import threading
import signal

pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)

if __name__ == "__main__":
    print('Hello!')
    # Initialize MIDI device
    # Testing using VMPK/CASIO
    portHint = "CASIO"
    inport = getMidiInput(portHint)
    outport = getMidiOutput(portHint)

    # Get Midi File
    # Testing using Hanon 1
    fileHint = './Exercise 1.mid'
    midifile = getMidiFile(fileHint, print_meta=True)
    
    # Play
    pool.submit(readMidi, inport)

    # playMidi_future = pool.submit(playMidi, midifile, outport)

    # try:
    #         while playMidi_future.running():
    #             time.sleep(1)
    # except KeyboardInterrupt:
    #     print("Playback interrupted!")
    #     playMidi_future.cancel()

    # finally:
    #     print("Jobs Done")
    #     pool.shutdown(wait=False, cancel_futures=True)

    pool.shutdown(wait=True)
    outport.reset()
    inport.close()

    myfile = messages2file(_buff)
    myfile.print_tracks()
    playMidi(myfile, outport)

    outport.close()

    print('Goodbye!')

