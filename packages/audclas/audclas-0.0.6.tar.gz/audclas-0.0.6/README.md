# AudClas

Package that uses audio classification model extracted from neonbjb/DL-Art-School - for filtering fine audio files.

# Classes

Classifier model returns one of 6 possible labels:

| label | class name |
| ----- | ---------- |
| 0     | fine       |
| 1     | env_noise  |
| 2     | music      |
| 3     | two_voices |
| 4     | reverb     |
| -     | unknown    |

# Installation

`pip install audclas`

# examples of usage

For single audio file:

```py
    from audclas.tortoise_audio_classifier import TortoiseAudioClassifier
    classifier = TortoiseAudioClassifier()

    label = classifier('wavs/test.wav')

    print(label)
```

For directory containing audio files (it searches recursively for all .wav / .mp3 files):

```py
    from tqdm import tqdm
    from audclas.tortoise_audio_classifier import TortoiseAudioClassifier
    classifier = TortoiseAudioClassifier()

    batch_size = 32
    do_classify, total = classifier.prepare_classify_dir_job('/content/wavs', batch_size)

    fine_audio_paths = []

    for result in tqdm(do_classify(), total=total):
        for audio_path, audio_label in result:
            if audio_label == 'fine':
                fine_audio_paths.append(audio_path)

    print(f'directory contains {len(fine_audio_paths)} fine files (total files: {total * batch_size})')
```
