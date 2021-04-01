# -*- coding: utf-8 -*-

import json
from pathlib import Path
from fintopics import config
from collections import Counter, OrderedDict


class LabelReduceEngine(object):
    def __init__(self, min_count, no_map):
        self.min_count = min_count
        self.keywords = [] if no_map else [
            'accounting',
            'revenue',
            'legal',
            'tax',
            'risk',
            'stock',
            'invest',
        ]

    def replace(self, label: str, count: int):
        for keyword in self.keywords:
            if keyword in label.lower():
                return keyword
        return 'other' if count < self.min_count else label


def prepare_labels(min_label_count, no_map):
    """Utility function to prepare labels."""
    savedir = Path(config['data']['save_path']) / 'labeled'
    labelset = {
        'train': (savedir / 'train_label.txt').read_text().splitlines(),
        'valid': (savedir / 'valid_label.txt').read_text().splitlines(),
        'test': (savedir / 'test_label.txt').read_text().splitlines(),
    }
    labelcounts = Counter(labelset['train'])
    sorted_labels = labelcounts.most_common()
    (savedir / 'label_counts.txt').write_text(
        '\n'.join(str(label_info) for label_info in sorted_labels),
    )
    lre = LabelReduceEngine(min_label_count, no_map)
    mapped_labels = OrderedDict()
    for label, count in labelcounts.most_common():
        mapped_labels.setdefault(lre.replace(label, count), len(mapped_labels))
    with (savedir / 'mapped_labels.json').open('w') as mlf:
        json.dump(mapped_labels, mlf)
    for key, labels in labelset.items():
        (savedir / '{0}.labels'.format(key)).write_text(
            '\n'.join(
                str(mapped_labels[lre.replace(label, labelcounts[label])]) for label in labels
            ),
        )
