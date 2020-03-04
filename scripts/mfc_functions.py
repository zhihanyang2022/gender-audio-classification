import numpy as np
import scipy.io.wavfile
import scipy.misc
import librosa
from skimage.transform import resize

kDEBUG = False
kSAMPLE_RATE = 48000

def pad_signal(signal, target_len=47998):
    
    num_zeros_needed = target_len - len(signal)
    
    if num_zeros_needed > 0:

        num_zeros_front = np.random.randint(num_zeros_needed)
        num_zeros_back = num_zeros_needed - num_zeros_front
        return np.pad(signal, (num_zeros_front, num_zeros_back), mode='constant')

    else:
        return signal
    
def pre_emphasis(signal):
    first_amp = signal[0]
    all_amps_without_first = signal[1:]
    all_amps_without_last = signal[:-1]
    emphasized_signal = np.append(first_amp, all_amps_without_first - 0.97 * all_amps_without_last)
    return emphasized_signal

def reshape(mfc):
    return resize(np.rollaxis(np.array([mfc] * 3), 0, 3), (224, 224, 3))
    
def save_as_jpg(mfc_3d, fpath):
    scipy.misc.toimage(mfc_3d, cmin=0, cmax=255).save(fpath)

def pipeline(wav_fpath, save_fpath):
    
    sr, signal = scipy.io.wavfile.read(wav_fpath)
    if kDEBUG:
        print(signal.shape, signal)
    emphasized_signal = pre_emphasis(signal)
    
    # the following code applies dft, mel filter banks, logging, dct and normalization all at once
    # truly convenient
    
    mfc = librosa.feature.mfcc(
        y=emphasized_signal.astype(float), 
        sr=kSAMPLE_RATE, 
        n_mfcc=12, 
        dct_type=2, 
        norm='ortho', 
        lifter=22,
        n_fft = int(kSAMPLE_RATE * 0.025),
        hop_length= int(kSAMPLE_RATE * 0.01),
        power=2,
        center=False,
        window='hanning',
        n_mels=40
    )

    mfc_3d = reshape(mfc)
    save_as_jpg(mfc_3d, save_fpath)