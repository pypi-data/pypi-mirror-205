import os
import torch

from torch.utils.data import DataLoader, default_collate

from .modules.dataset import AudioFolderDataset
from .modules.stft import TacotronSTFT
from .modules.audio_mini_encoder import AudioMiniEncoderWithClassifierHead

output_labels = ['fine', 'env_noise', 'music', 'two_voices', 'reverb']

def to_label(label_tensor):
    return output_labels[label_tensor.item()]

class TortoiseAudioClassifier():
    def __init__(self, checkpoint_path='jbetker/tortoise-filtering-models') -> None:
        self.classifier = AudioMiniEncoderWithClassifierHead(5, **{
            'spec_dim': 80,
            'embedding_dim': 1024,
            'base_channels': 128,
            'depth': 3,
            'resnet_blocks': 2,
            'attn_blocks': 8,
            'num_attn_heads': 4,
            'dropout': .1
        })
        if os.path.exists(checkpoint_path):
            checkpoint = checkpoint_path
        else:
            from huggingface_hub import hf_hub_download
            checkpoint = hf_hub_download(checkpoint_path, 'noisy_audio_clips_classifier.pth')
        self.classifier.load_state_dict(torch.load(checkpoint))
        self.stft = TacotronSTFT()
        if torch.cuda.is_available():
            self.classifier.cuda()
            self.stft.cuda()
        
        self.classifier.eval()

    def __call__(self, file_path):
        batch_item = AudioFolderDataset.get_batch_item(file_path)
        batch = default_collate([batch_item])
        _, labels = self.classify_batch(batch)
        return to_label(labels[0]) if labels is not None else 'unknown'

    def prepare_classify_dir_job(self, audio_dir: str, batch_size=16):
        dataset = AudioFolderDataset(audio_dir)
        data_loader = DataLoader(dataset, batch_size, shuffle=False, num_workers=os.cpu_count() - 1)
        def callback():
            try:
                for batch in data_loader:
                    max_len = max(batch['samples'])
                    batch['clip'] = batch['clip'][:, :max_len]

                    no_hifreq_data, labels = self.classify_batch(batch)
                    if labels is None:
                        continue

                    yield [(batch['path'][b], to_label(labels[b])) for b in range(labels.size(0)) if not no_hifreq_data[b]]
                        
            except:
                print("Exception encountered. Will ignore and continue. Exception info follows.")
        return callback, len(data_loader)
    
    def classify_batch(self, batch):
        with torch.no_grad():
            if torch.cuda.is_available():
                clips = batch['clip'].cuda()
            else:
                clips = batch['clip']
                
            mels = self.stft.mel_spectrogram(clips)

            def get_spec_mags(clip):
                stft = torch.stft(clip, n_fft=22000, hop_length=1024, return_complex=True)
                stft = stft[0, -2000:, :]
                return (stft.real ** 2 + stft.imag ** 2).sqrt()
            
            no_hifreq_data = get_spec_mags(clips).mean(dim=1) < .01
            if torch.all(no_hifreq_data):
                return None, None

            return no_hifreq_data, torch.argmax(self.classifier(mels), dim=-1)

