import alarm
import board
import os
import audiomp3
import audiopwmio
import time
import random

deep_sleep_after_seconds = 60

print('start!')

mp3files = ['/sounds/' + f for f in os.listdir('/sounds/') if f.endswith('.mp3')]
mp3files.sort()
print(f'found {len(mp3files)} mp3 files')

audio = audiopwmio.PWMAudioOut(board.GP0)

def get_sound_to_play():
    wake_alarm = alarm.wake_alarm
    if not isinstance(wake_alarm, alarm.pin.PinAlarm):
        print('first run')
        return 0
    return random.randint(0, len(mp3files) - 1)

def play():
    index = get_sound_to_play()
    file = mp3files[index]
    print(f'playing file {index} of {len(mp3files)}, {file}')
    decoder = audiomp3.MP3Decoder(open(file, "rb"))
    audio.play(decoder)
    print('playing', decoder.file)
    time.sleep(0.5)
    # This allows you to do other things while the audio plays!
    while audio.playing:
        pass
    print('done')

while True:
    play()

    pin_alarm = alarm.pin.PinAlarm(pin=board.GP18, value=True, pull=True)
    deep_sleep_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + deep_sleep_after_seconds)
    
    alarm.light_sleep_until_alarms(pin_alarm, deep_sleep_alarm)
    if isinstance(alarm.wake_alarm, alarm.time.TimeAlarm):
        print('going into deep sleep, night night')
        alarm.exit_and_deep_sleep_until_alarms(pin_alarm)
    else:
        print('woke from light sleep due to button press')


