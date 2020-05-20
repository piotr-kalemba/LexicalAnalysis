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





