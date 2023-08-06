![Alt text](/wallpaper.png?raw=true "Title")
# GRN-Stability Selection

[![master](https://github.com/soelmicheletti/grn-thresholding/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/soelmicheletti/grn-thresholding/actions/workflows/python-app.yml)[![PyPI - Python Version](https://img.shields.io/pypi/v/grn-thresholding?style=flat&colorA=0f0f0f&colorB=0f0f0f)](https://pypi.org/project/grn-thresholdin/)

Stability selection is a generally applicable subsampling-based framework for feature selection, allowing to bound the number of false positives if the exchangeability condition holds. Here we apply it in the context of gene regulatory networks: given a network-inference algorithm, we return the set of edges selected by stability selection. 

## Install

```bash
$ pip install grn-stability-selection
```


## Usage

```python
import giraffe

def giraffe_wrapper(expression, motif, ppi, regularization = 0):
    return giraffe.Giraffe(expression, motif, ppi, regularization = regularization).get_regulation()

stability = StabilitySelection(giraffe_wrapper, lambdas = np.linspace(lambda_min, lambda_max, grid_size), K = 100, v = 30)
stable_edges = stability(expression = expression, motif = motif, ppi = ppi)
```

The example above runs [giraffe](TODO), a matrix factorization based algorithm for gene regulatory network inference, with different values of the regularization parmeter. After assigning a relevance score to each edge, it applies thresholding as is in the [stability selection paper](https://rss.onlinelibrary.wiley.com/doi/pdf/10.1111/j.1467-9868.2010.00740.x?casa_token=zNJa8W_cynwAAAAA:_49AqlilJp_TP_9X2vopg6TFGoiBA-rkTJrpjZW8TurMEcOayPP4p25TUkpTzeTabnzOA5udoWyGJ5tTzw). 

## Appreciation
 
This implementation is inspired by the [scikit-learn compatible implementation](https://github.com/scikit-learn-contrib/stability-selection) by Thomas Huijskens and colleagues. Shout-out for their great work and useful [blog post](https://thuijskens.github.io/2018/07/25/stability-selection/)!

## Citation

```bibtex
@article{meinshausen2010stability,
  title={Stability selection},
  author={Meinshausen, Nicolai and B{\"u}hlmann, Peter},
  journal={Journal of the Royal Statistical Society: Series B (Statistical Methodology)},
  volume={72},
  number={4},
  pages={417--473},
  year={2010},
  publisher={Wiley Online Library}
}

```
