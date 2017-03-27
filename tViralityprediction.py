from regression1 import RegressionModel
from tHashTagIndex import HashtagIndex
from tfeatureExtractor import tFeatureExtractor
from dataAnalysis import DataAnalyser
import matplotlib.pyplot as plt
import numpy as np

class ViralityPrediction:
    SCORE_PLOT_FILENAME = "hashtags_score.png"
    CLASSIFICATION = True
    K = 10

    def __init__(self, normalize=False, balance=False, tweet_threshold=0, score=False, dump_model=True):
        self.model = RegressionModel()
        if not self.model.load():
            training_set, testing_set = self.model.load_datasets(
                balance=balance, viral_threshold=tweet_threshold)

            if ViralityPrediction.CLASSIFICATION == True:
                training_set = self.model.normaliseFeats(training_set)
                testing_set = self.model.normaliseFeats(testing_set)
                self.model.trainClassifier(training_set, normalize=normalize)
                if score:
                    self.model.scoreClassifier(testing_set)

            else:
                self.model.trainRegression(training_set, normalize=normalize)
                if score:
                    self.model.scoreRegression(testing_set)

            if dump_model:
                self.model.dump()

    def predict(self, features, hashtag_threshold=None):
        k=0
        tweets_values=self.model.predictClassifier(features)
        for i in tweets_values:
             k=k+1
        print(k)


    def score(self, expected, predicted, labels=None, showPlot=True, savePlot=False):
        if showPlot or savePlot:
            x = np.arange(len(expected))
            width = 0.8
            ticks = x + x * width

            fig = plt.figure()
            ax = fig.add_subplot(111)
            bar1 = ax.bar(ticks, expected, color='green')
            bar2 = ax.bar(ticks + width, predicted, color='blue')
            ax.set_xlim(-width, (ticks + width)[-1] + 2 * width)
            ax.set_ylim(0, max(max(expected), max(predicted)) * 1.05)
            ax.set_xticks(ticks + width)
            if labels is not None:
                xtickNames = ax.set_xticklabels(labels)
                plt.setp(xtickNames, rotation=45, fontsize=10)
            ax.set_title('Expected and predicted retweet count per hashtag')
            ax.legend((bar1[0], bar2[0]), ('Expected', 'Predicted'))

            if savePlot:
                plt.savefig(DataAnalyser.PLOT_DIR + ViralityPrediction.SCORE_PLOT_FILENAME, format='png')
            if showPlot:
                plt.show()

        return np.mean(predicted - expected) ** 2


if __name__ == "__main__":
    vp = ViralityPrediction(normalize=True, balance=True, tweet_threshold=50000,
        score=False, dump_model=False)
    hashtagIndex = HashtagIndex()
    hashtags = [k for (k, v) in hashtagIndex.items(sort=True, descending=True, min_values=1)]
    print "Extracting features....."
    tids,tfeaturesList,viralityList = tFeatureExtractor.loadFromDB()
    vp.predict(tfeaturesList)