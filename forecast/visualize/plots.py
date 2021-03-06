import matplotlib.pyplot as plt
import numpy as np

from .savefig import savefig


plt.style.use('ggplot')


@savefig
def plot_scatter(
        df,
        x,
        y,
        figsize=(10, 10),
        **kwargs):

    f, a = plt.subplots(figsize=figsize)
    df.plot(x=x, y=y, kind='scatter', ax=a, **kwargs)

    return f


def plot_line(
        y,
        x=None,
        figsize=(10, 10),
        **kwargs
):

    f, a = plt.subplots(figsize=figsize)

    if x is None:
        x = np.arange(len(y))

    a.plot(x, y, **kwargs)

    return f


@savefig
def plot_grouped(
        df,
        y,
        group_type='year_and_month'
):

    if group_type == 'year_and_month':
        group_idx = [df.index.year, df.index.month]

    elif group_type == 'month':
        group_idx = [df.index.month]

    elif group_type == 'hour':
        group_idx = [df.index.hour]

    else:
        raise ValueError('group_type of {} not supported'.format(group_type))

    groups = df.groupby(group_idx).agg(
        {y: [np.mean, np.std, np.median, np.min, np.max]})

    fig, axes = plt.subplots(nrows=3, figsize=(15, 10))

    groups[y]['mean'].plot(ax=axes[0], kind='line')
    groups[y]['median'].plot(ax=axes[0], kind='line')
    groups[y]['std'].plot(ax=axes[1], kind='line')
    groups[y]['amin'].plot(ax=axes[2], kind='line')
    groups[y]['amax'].plot(ax=axes[2], kind='line')

    axes[0].set_title('{} grouped by {}'.format(y, group_type))

    for ax in axes:
        ax.legend()

    return fig


@savefig
def plot_distribution(df, y, set_xlim=True):

    fig, axes = plt.subplots(
        nrows=2, figsize=(12, 5), sharex=True
    )

    series = df.loc[:, y]

    series.plot(ax=axes[0], kind='hist', bins=1000)
    series.plot(ax=axes[1], kind='kde')

    xlim = series.mean() + series.std() * 3

    for ax in axes:
        ax.set_xlabel(y)
        if set_xlim:
            ax.set_xlim([-xlim, xlim])

    return fig
