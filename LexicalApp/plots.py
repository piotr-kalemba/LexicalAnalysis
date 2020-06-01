import pygal


class FreqChart:
    def __init__(self):
        self.chart = pygal.Bar()
        self.chart.title = 'Sentence length frequencies'
        self.chart.x_title = 'Sentence length'
        self.chart.y_title = 'Sentence frequency'

    def generate(self, seq):
        x_labels = [str(10 * i) for i in range(1, len(seq) + 1)]
        if len(seq) < 50:
            self.chart.x_labels = x_labels
        self.chart.add('Freq', seq)
        return self.chart.render(is_unicode=True)


class VocabChart:
    def __init__(self):
        self.chart = pygal.StackedBar(print_values=True)
        self.chart.title = 'Compare Book Lexicons'
        self.chart.x_title = 'Book'
        self.chart.y_title = 'Vocabulary Size'

    def generate(self, titles, hist_unique, common):
        self.chart.x_labels = titles
        stump = [common] * len(hist_unique)
        self.chart.add('Common Vocab', stump)
        # self.chart.add('Shared Vocab', hist_shared)
        self.chart.add('Unique Vocab', hist_unique)
        return self.chart.render(is_unicode=True)


