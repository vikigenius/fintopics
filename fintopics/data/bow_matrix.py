# -*- coding: utf-8 -*-

from pathlib import Path

from scipy.io import mmwrite
from sklearn.feature_extraction.text import CountVectorizer

from fintopics import config


def prepare_bow_matrix(labeled) -> None:
    """Function to prepare the BOW matrix."""
    savedir = Path(config['data']['save_path'])
    cvect = CountVectorizer(strip_accents='ascii', min_df=2)

    cvect.fit((savedir / 'train.txt').read_text().splitlines())
    if labeled:
        savedir = savedir / 'labeled'

    train_dbyw = cvect.transform(
        (savedir / 'train.txt').read_text().splitlines(),
    )
    valid_dbyw = cvect.transform(
        (savedir / 'valid.txt').read_text().splitlines(),
    )
    test_dbyw = cvect.transform(
        (savedir / 'test.txt').read_text().splitlines(),
    )

    mmwrite(str(savedir / 'train.mtx'), train_dbyw)
    mmwrite(str(savedir / 'valid.mtx'), valid_dbyw)
    mmwrite(str(savedir / 'test.mtx'), test_dbyw)

    with (savedir / 'vocab').open('w', encoding='utf-8') as fvpw:
        fvpw.write('\n'.join(cvect.vocabulary_))

    with (savedir / 'mtx.flist').open('w') as flpw:
        flpw.write('{0}\n'.format(savedir.resolve() / 'train.mtx'))
        flpw.write('{0}\n'.format(savedir.resolve() / 'valid.mtx'))
        flpw.write('{0}\n'.format(savedir.resolve() / 'test.mtx'))
