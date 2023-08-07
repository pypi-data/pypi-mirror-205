# source: https://github.com/neonbjb/DL-Art-School

import torch

loaded_options = None

def checkpoint(fn, *args):
    if loaded_options is None:
        enabled = False
    else:
        enabled = loaded_options['checkpointing_enabled'] if 'checkpointing_enabled' in loaded_options.keys() else True
    if enabled:
        return torch.utils.checkpoint.checkpoint(fn, *args)
    else:
        return fn(*args)
    
def sequential_checkpoint(fn, partitions, *args):
    if loaded_options is None:
        enabled = False
    else:
        enabled = loaded_options['checkpointing_enabled'] if 'checkpointing_enabled' in loaded_options.keys() else True
    if enabled:
        return torch.utils.checkpoint.checkpoint_sequential(fn, partitions, *args)
    else:
        return fn(*args)