import matplotlib.pyplot as plt
from .lexical_tools import sentence_len_freq, get_content


def create_bar_freq(book):
    content = get_content(book)
    seq = sentence_len_freq(content)
    bands = [''] * len(seq) if len(seq) > 30 else ['{}'.format(10 * i) for i in range(1, len(seq) + 1)]
    x_val = list(range(len(seq)))
    fig, ax = plt.subplots()
    ax.bar(x=x_val,
           height=seq,
           color="green",
           align="center",
           tick_label=bands)
    ax.set_ylabel('Sentence frequencies')
    ax.set_xlabel('Sentence lengths bands (upper limits)')
    ax.set_title('Sentence length frequencies')
    name = "".join(book.title.lower().split())
    plt.savefig(f'{name}')
