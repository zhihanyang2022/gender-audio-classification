import time
import sounddevice as sd
import scipy.io.wavfile

sr = 48000
sd.default.device = 0

print('==========')

while True:
    resp = input('Type y when you have a number from 0 to 9 in mind: ')
    if 'y' in resp:
        break

print("Speak that number immediately after you see 'Speak now!':")
print('3')
time.sleep(0.5)
print('2')
time.sleep(0.5)
print('1')
time.sleep(0.3)

def record_wav(duration=0.99):
    array1d = sd.rec(int(duration * sr), samplerate=sr, channels=1)
    time.sleep(0.2)
    print('Speak now!')
    sd.wait()
    return array1d

recording = record_wav()
scipy.io.wavfile.write(filename='myvoice.wav', rate=sr, data=recording)

print('==========')
