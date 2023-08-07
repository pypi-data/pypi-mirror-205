# source: https://github.com/neonbjb/DL-Art-School

import os
import numpy as np
import pathlib
import torch
import torchaudio

def find_audio_files(base_path, globs=['*.wav', '*.mp3', '*.flac', '*.ogg']):
    path = pathlib.Path(base_path)
    paths = []
    for glob in globs:
        paths.extend([str(f) for f in path.rglob(glob)])
    # return [path for path in paths if os.path.basename(path) > '33437.ogg']
    return paths

def load_wav_to_torch(full_path):
    import scipy.io.wavfile
    sampling_rate, data = scipy.io.wavfile.read(full_path)
    if data.dtype == np.int32:
        norm_fix = 2 ** 31
    elif data.dtype == np.int16:
        norm_fix = 2 ** 15
    elif data.dtype == np.float16 or data.dtype == np.float32:
        norm_fix = 1.
    else:
        raise NotImplemented(f"Provided data dtype not supported: {data.dtype}")
    return (torch.FloatTensor(data.astype(np.float32)) / norm_fix, sampling_rate)

def load_audio(audiopath, sampling_rate, raw_data=None):
    audiopath = str(audiopath)
    if raw_data is not None:
        # Assume the data is wav format. SciPy's reader can read raw WAV data from a BytesIO wrapper.
        audio, lsr = load_wav_to_torch(raw_data)
    else:
        if audiopath[-4:] == '.wav':
            audio, lsr = load_wav_to_torch(audiopath)
        elif audiopath[-5:] == '.flac' or audiopath[-4:] == '.ogg':
            import soundfile as sf
            audio, lsr = sf.read(audiopath)
            audio = torch.FloatTensor(audio)
        elif audiopath[-4:] == '.mp3':
            # https://github.com/neonbjb/pyfastmp3decoder  - Definitely worth it.
            from pyfastmp3decoder.mp3decoder import load_mp3
            audio, lsr = load_mp3(audiopath, sampling_rate)
            audio = torch.FloatTensor(audio)
        else:
            raise Exception(f'unsupported audio extension. try one of [mp3, .flac, .wav]')

    # Remove any channel data.
    if len(audio.shape) > 1:
        if audio.shape[0] < 5:
            audio = audio[0]
        else:
            assert audio.shape[1] < 5
            audio = audio[:, 0]

    if lsr != sampling_rate:
        audio = torchaudio.functional.resample(audio, lsr, sampling_rate)

    # Check some assumptions about audio range. This should be automatically fixed in load_wav_to_torch, but might not be in some edge cases, where we should squawk.
    # '2' is arbitrarily chosen since it seems like audio will often "overdrive" the [-1,1] bounds.
    if torch.any(audio > 2) or not torch.any(audio < 0):
        print(f"Error with {audiopath}. Max={audio.max()} min={audio.min()}")
    audio.clip_(-1, 1)

    return audio

class AudioFolderDataset(torch.utils.data.Dataset):
    def __init__(self, path, sampling_rate=22050, pad_to=600000):
        self.audiopaths = find_audio_files(path)
        self.sampling_rate = sampling_rate
        self.pad_to = pad_to

    def __getitem__(self, index):
        try:
            return self.get_batch_item(self.audiopaths[index], self.sampling_rate, self.pad_to)
        except:
            print(f"Error loading audio for file {self.audiopaths[index]}")
            # Recover gracefully. It really sucks when we outright fail.
            return self[index+1]

    def __len__(self):
        return len(self.audiopaths)
    
    @staticmethod
    def get_batch_item(audio_path, sampling_rate=22050, pad_to=600000):
        audio_norm = load_audio(audio_path, sampling_rate)
        orig_length = audio_norm.shape[-1]
        
        if audio_norm.shape[-1] > pad_to:
            print(f"Warning - {audio_path} has a longer audio clip than is allowed: {audio_norm.shape[-1]}; allowed: {pad_to}. "
                f"Truncating the clip, though this will likely invalidate the prediction.")
            audio_norm = audio_norm[:pad_to]
        else:
            padding = pad_to - audio_norm.shape[-1]
            if padding > 0:
                audio_norm = torch.nn.functional.pad(audio_norm, (0, padding))

        return {
            'clip': audio_norm,
            'samples': orig_length,
            'path': audio_path
        }
