import alarm
import board
import os
import audiomp3
import audiopwmio
import digitalio
import time
import random
import audiomixer

deep_sleep_after_seconds = 60

print('start!')

mp3files = ['/sounds/' + f for f in os.listdir('/sounds/') if f.endswith('.mp3')]
mp3files.sort()
print(f'found {len(mp3files)} mp3 files')

audio = audiopwmio.PWMAudioOut(board.GP0)
mute = digitalio.DigitalInOut(board.GP20)
mute.direction = digitalio.Direction.OUTPUT
mixer = audiomixer.Mixer(voice_count=1, sample_rate=22050, channel_count=1,
                         bits_per_sample=16, samples_signed=True, buffer_size=2048)
audio.play(mixer)

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
    with open(file, "rb") as mp3:
        decoder = audiomp3.MP3Decoder(mp3)
        mixer.play(decoder)
        mute.value = True
        print('playing', decoder.file)
        time.sleep(0.5)
        # This allows you to do other things while the audio plays!
        while mixer.playing:
            pass
        mute.value = False
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
