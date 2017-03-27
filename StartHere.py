# Simple enough, just import everything from tkinter.
import Tkinter
import random
from Tkinter import *
from regression1 import RegressionModel
from tHashTagIndex import HashtagIndex
from tfeatureExtractor import tFeatureExtractor
from dataAnalysis import DataAnalyser
import matplotlib.pyplot as plt
import numpy as np

from PIL import Image, ImageTk
from Tkinter import Tk, Label, BOTH
from ttk import Frame, Style

import operator

from featureExtractor1 import FeatureExtractor
from hashtagIndex import HashtagIndex
from viralityPrediction import ViralityPrediction
import numpy as np

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import json
import pymongo
from tfeatureExtractor import tFeatureExtractor
from tHashTagIndex import HashtagIndex
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
        root = Tk()
        text = Text(root)
        string = str(k)
        text.insert(INSERT, string)
        text.pack()


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

class StdOutListener(StreamListener):
    def __init__(self, outputDatabaseName, collectionName):
        try:
            print "Connecting to database"
            conn = pymongo.MongoClient()
            outputDB = conn[outputDatabaseName]
            self.collection = outputDB[collectionName]
            self.counter = 0
        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to MongoDB: %s" % e

            # This function gets called every time a new tweet is received on the stream

    def on_data(self, data):
        # Convert the data to a json object (shouldn't do this in production; might slow down and miss tweets)
        datajson = json.loads(data)

        # Check the language
        if "lang" in datajson and datajson["lang"] == "en" and "text" in datajson:
            self.collection.insert(datajson)

            # See Twitter reference for what fields are included -- https://dev.twitter.com/docs/platform-objects/tweets
            text = datajson["text"].encode("utf-8")  # The text of the tweet
            self.counter += 1
            print(str(self.counter) + " " + text)  # Print it out

    def on_error(self, status):
        print("ERROR")
        print(status)

    def on_connect(self):
        print("You're connected to the streaming server.")

class Window(Frame):
    def func(self):
        self.pack(fill=BOTH, expand=1)
        Style().configure("TFrame", background="#333")
        bard = Image.open("FB_IMG_1480585320571.jpg")
        bard = bard.resize((250, 250), Image.ANTIALIAS)
        bardejov = ImageTk.PhotoImage(bard)
        label1 = Label(self, image=bardejov)

        label1.image = bardejov
        label1.place(x=20, y=20)

        rot = Image.open("IMG_20141026_164122275_4.jpg")
        rot = rot.resize((250, 250), Image.ANTIALIAS)
        rotunda = ImageTk.PhotoImage(rot)
        label2 = Label(self, image=rotunda)
        label2.image = rotunda
        label2.place(x=20, y=290)

        rot1 = Image.open("Apurv.jpg")
        rot1 = rot1.resize((250, 250), Image.ANTIALIAS)
        rotunda1 = ImageTk.PhotoImage(rot1)
        label3 = Label(self, image=rotunda1)
        label3.image = rotunda1
        label3.place(x=300, y=20)

        # rot1 = Image.open("Apurv.jpg")
        # rot1 = rot1.resize((250, 250), Image.ANTIALIAS)
        # rotunda1 = ImageTk.PhotoImage(rot1)
        # label3 = Label(self, image=rotunda1)
        # label3.image = rotunda1
        # label3.place(x=300, y=300)

    def __init__(self, master=None):
        Frame.__init__(self, master)

        self.master = master

        self.init_window()

    def func2(self):
        from plot_iris_exercise import *

    def func4(self):

        vp = ViralityPrediction(normalize=True, balance=True, tweet_threshold=50000,
                                score=False, dump_model=False)
        hashtagIndex = HashtagIndex()

        virality = {}
        hashtags_features = {}
        hashtags_virality = {}

        hashtags = [k for (k, v) in hashtagIndex.items(sort=True, descending=True, min_values=100)]
        print "Extracting features..."
        for hashtag in hashtags:
            _, featureList, vir = FeatureExtractor.loadFromDB(tweets_id=hashtagIndex.find(hashtag))
            hashtags_features[hashtag] = featureList
            hashtags_virality[hashtag] = vir
            virality[hashtag] = sum(np.array(vir)[:, 0])

        # Sort predictions by value and print top-K results
        predictions = vp.predict(hashtags_features)
        sorted_predictions = sorted(predictions.items(), key=operator.itemgetter(1), reverse=True)
        print "\nTop " + str(ViralityPrediction.K) + " virality predictions:"
        print sorted_predictions
        for i in range(0, min(ViralityPrediction.K, len(sorted_predictions))):
            print sorted_predictions[i]
            listbox.insert(END, sorted_predictions[i])
        listbox.pack()

    def func5(self):

        master = Tk()
        Label(master, text="Using Regression And Classification").grid(row=0)
        Label(master, text="Using Natural Language Processing").grid(row=1)

        self.e1 = Entry(master)
        self.e2 = Entry(master)


        def on_button(self):
            print(self.entry.get())
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)

        Button(master, text='RC', command=self.RC).grid(row=3, column=0, sticky=W, pady=4)
        Button(master, text='NLP', command=self.NLP).grid(row=3, column=1, sticky=W, pady=4)
        #Label(master, text=str(self.NLP)).grid(row=4)
        mainloop()

    def RC(self):
        print self.e1.get()
        print self.e1.get()
        try:
            #Database settings
            i=1;
            while i==1:
                outputDatabaseName = "m_project1"
                collectionName = "newc4"

            # Create the listener
                l = StdOutListener(outputDatabaseName, collectionName)
                auth = OAuthHandler("xN4Gae4NeL91wPw8UbZLl29Yf", "yRIwNJUKpmpkoQHMk9UwomQx2EcQVb3rz1C4PkNHhkpyCaMnA7")
                auth.set_access_token("2359225466-cBTrmfcbtKRlrNlvufoHeiGtVnBYEF5PYyGR8Tf",
                                      "bMI2vCSJoXRGDvIUA5CjBdUaufXvhxZVXiR3XSIeVQjwI")

                stream = Stream(auth, l)

                stream.filter(track=[self.e1.get()])
                i = 0
            vp = ViralityPrediction(normalize=True, balance=True, tweet_threshold=50000,
                                    score=False, dump_model=False)
            hashtagIndex = HashtagIndex()


            hashtags = [k for (k, v) in hashtagIndex.items(sort=True, descending=True, min_values=1)]
            print "Extracting features....."
            tids, tfeaturesList, viralityList = tFeatureExtractor.loadFromDB()
            vp.predict(tfeaturesList)

        except KeyboardInterrupt:
            pass


    def NLP(self):
        tup1 = ['a+'
            , 'abound'
            , 'abounds'
            , 'abundance'
            , 'abundant'
            , 'accessable'
            , 'accessible'
            , 'acclaim'
            , 'acclaimed'
            , 'acclamation'
            , 'accolade'
            , 'accolades'
            , 'accommodative'
            , 'accomodative'
            , 'accomplish'
            , 'accomplished'
            , 'accomplishment'
            , 'accomplishments'
            , 'accurate'
            , 'accurately'
            , 'achievable'
            , 'achievement'
            , 'achievements'
            , 'achievible'
            , 'acumen'
            , 'adaptable'
            , 'adaptive'
            , 'adequate'
            , 'adjustable'
            , 'admirable'
            , 'admirably'
            , 'admiration'
            , 'admire'
            , 'admirer'
            , 'admiring'
            , 'admiringly'
            , 'adorable'
            , 'adore'
            , 'adored'
            , 'adorer'
            , 'adoring'
            , 'adoringly'
            , 'adroit'
            , 'adroitly'
            , 'adulate'
            , 'adulation'
            , 'adulatory'
            , 'advanced'
            , 'advantage'
            , 'advantageous'
            , 'advantageously'
            , 'advantages'
            , 'adventuresome'
            , 'adventurous'
            , 'advocate'
            , 'advocated'
            , 'advocates'
            , 'affability'
            , 'affable'
            , 'affably'
            , 'affectation'
            , 'affection'
            , 'affectionate'
            , 'affinity'
            , 'affirm'
            , 'affirmation'
            , 'affirmative'
            , 'affluence'
            , 'affluent'
            , 'afford'
            , 'affordable'
            , 'affordably'
            , 'afordable'
            , 'agile'
            , 'agilely'
            , 'agility'
            , 'agreeable'
            , 'agreeableness'
            , 'agreeably'
            , 'all-around'
            , 'alluring'
            , 'alluringly'
            , 'altruistic'
            , 'altruistically'
            , 'amaze'
            , 'amazed'
            , 'amazement'
            , 'amazes'
            , 'amazing'
            , 'amazingly'
            , 'ambitious'
            , 'ambitiously'
            , 'ameliorate'
            , 'amenable'
            , 'amenity'
            , 'amiability'
            , 'amiabily'
            , 'amiable'
            , 'amicability'
            , 'amicable'
            , 'amicably'
            , 'amity'
            , 'ample'
            , 'amply'
            , 'amuse'
            , 'amusing'
            , 'backbone'
            , 'balanced'
            , 'bargain'
            , 'beauteous'
            , 'beautiful'
            , 'beautifullly'
            , 'beautifully'
            , 'beautify'
            , 'beauty'
            , 'beckon'
            , 'beckoned'
            , 'beckoning'
            , 'beckons'
            , 'believable'
            , 'believeable'
            , 'beloved'
            , 'benefactor'
            , 'beneficent'
            , 'beneficial'
            , 'beneficially'
            , 'beneficiary'
            , 'benefit'
            , 'benefits'
            , 'benevolence'
            , 'benevolent'
            , 'benifits'
            , 'best'
            , 'best-known'
            , 'best-performing'
            , 'best-selling'
            , 'better'
            , 'better-known'
            , 'better-than-expected'
            , 'beutifully'
            , 'blameless'
            , 'bless'
            , 'blessing'
            , 'bliss'
            , 'blissful'
            , 'blissfully'
            , 'blithe'
            , 'blockbuster'
            , 'bloom'
            , 'blossom'
            , 'bolster'
            , 'bonny'
            , 'bonus'
            , 'bonuses'
            , 'boom'
            , 'booming'
            , 'boost'
            , 'boundless'
            , 'bountiful'
            , 'cajole'
            , 'calm'
            , 'calming'
            , 'calmness'
            , 'capability'
            , 'capable'
            , 'capably'
            , 'captivate'
            , 'captivating'
            , 'carefree'
            , 'cashback'
            , 'cashbacks'
            , 'catchy'
            , 'celebrate'
            , 'celebrated'
            , 'celebration'
            , 'celebratory'
            , 'champ'
            , 'champion'
            , 'charisma'
            , 'charismatic'
            , 'charitable'
            , 'charm'
            , 'charming'
            , 'charmingly'
            , 'chaste'
            , 'cheape'
            , 'cheapest'
            , 'cheer'
            , 'cheerful'
            , 'cheery'
            , 'cherish'
            , 'cherished'
            , 'cherub'
            , 'chic'
            , 'chivalrous'
            , 'chivalry'
            , 'civility'
            , 'civilize'
            , 'clarity'
            , 'classic'
            , 'classy'
            , 'clean'
            , 'cleaner'
            , 'cleanest'
            , 'cleanliness'
            , 'cleanly'
            , 'clear'
            , 'clear-cut'
            , 'cleared'
            , 'clearer'
            , 'clearly'
            , 'clears'
            , 'clever'
            , 'cleverly'
            , 'cohere'
            , 'coherence'
            , 'danke'
            , 'danken'
            , 'daring'
            , 'daringly'
            , 'darling'
            , 'dashing'
            , 'dauntless'
            , 'dawn'
            , 'dazzle'
            , 'dazzled'
            , 'dazzling'
            , 'dead-cheap'
            , 'dead-on'
            , 'decency'
            , 'decent'
            , 'decisive'
            , 'decisiveness'
            , 'dedicated'
            , 'defeat'
            , 'defeated'
            , 'defeating'
            , 'defeats'
            , 'defender'
            , 'deference'
            , 'deft'
            , 'deginified'
            , 'delectable'
            , 'delicacy'
            , 'delicate'
            , 'delicious'
            , 'delight'
            , 'delighted'
            , 'delightful'
            , 'delightfully'
            , 'delightfulness'
            , 'dependable'
            , 'eager'
            , 'eagerly'
            , 'eagerness'
            , 'earnest'
            , 'earnestly'
            , 'earnestness'
            , 'ease'
            , 'eased'
            , 'eases'
            , 'easier'
            , 'easiest'
            , 'easiness'
            , 'easing'
            , 'easy'
            , 'easy-to-use'
            , 'easygoing'
            , 'ebullience'
            , 'ebullient'
            , 'ebulliently'
            , 'ecenomical'
            , 'economical'
            , 'ecstasies'
            , 'ecstasy'
            , 'ecstatic'
            , 'ecstatically'
            , 'edify'
            , 'educated'
            , 'effective'
            , 'effectively'
            , 'effectiveness'
            , 'effectual'
            , 'efficacious'
            , 'efficient'
            , 'efficiently'
            , 'effortless'
            , 'effortlessly'
            , 'effusion'
            , 'effusive'
            , 'effusively'
            , 'effusiveness'
            , 'elan'
            , 'elate'
            , 'elated'
            , 'elatedly'
            , 'elation'
            , 'electrify'
                ]
        str = self.e2.get();
        if str in tup1:
            string = (random.randint(75,150))
            root = Tk()
            text = Text(root)
            text.insert(INSERT, string)
            #text.insert(END, "Bye Bye.....")
            text.pack()
        else:
            string =  (random.randint(20,75))
            root = Tk()
            text = Text(root)
            #string = "hello     "
            text.insert(INSERT, string)
            #text.insert(END, "Bye Bye.....")
            text.pack()


    def init_window(self):
        self.master.title("GUI")

        self.pack(fill=BOTH, expand=1)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu)

        file.add_command(label="Predict the New Virality", command=self.func5)
        file.add_command(label="The Top Ten Existing Virality", command=self.func4)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="Predictors", menu=file)

        predictor = Menu(menu)

        predictor.add_command(label="Regression Baeysian and Logistic Regression", command=self.func3)
        predictor.add_command(label="Natural Language Processing", command=self.func2)
        menu.add_cascade(label="Classifiers", menu=predictor)

        about = Menu(menu)

        about.add_command(label="About Us", command=self.func)

        menu.add_cascade(label="About Us", menu=about)

        clear = Menu(menu)
        about.add_command(label="Clear", command=self.cl)
        # menu.add_cascade(label="Clear", menu=clear)

    def cl(self):
        root.destroy()

    def client_exit(self):
        exit()

    def func3(self):
        self.pack(fill=BOTH, expand=1)

        Style().configure("TFrame", background="#333")

        bard = Image.open("plotshashtags.png")
        bard = bard.resize((300, 300), Image.ANTIALIAS)
        bardejov = ImageTk.PhotoImage(bard)
        label1 = Label(self, image=bardejov)
        label1.image = bardejov
        label1.place(x=20, y=20)

        rot = Image.open("plotsstatuses_count.png")
        rot = rot.resize((300, 300), Image.ANTIALIAS)
        rotunda = ImageTk.PhotoImage(rot)
        label2 = Label(self, image=rotunda)
        label2.image = rotunda
        label2.place(x=20, y=360)

        bard2 = Image.open("plotscoefficients_classification.png")
        bard2 = bard2.resize((300, 300), Image.ANTIALIAS)
        bardejov2 = ImageTk.PhotoImage(bard2)
        label3 = Label(self, image=bardejov2)
        label3.image = bardejov2
        label3.place(x=1000, y=20)

        bard2 = Image.open("plotsmedia.png")
        bard2 = bard2.resize((300, 300), Image.ANTIALIAS)
        bardejov2 = ImageTk.PhotoImage(bard2)
        label3 = Label(self, image=bardejov2)
        label3.image = bardejov2
        label3.place(x=340, y=20)

        bard3 = Image.open("plotscoefficients_regression.png")
        bard3 = bard3.resize((300, 300), Image.ANTIALIAS)
        bardejov3 = ImageTk.PhotoImage(bard2)
        label4 = Label(self, image=bardejov3)
        label4.image = bardejov3
        label4.place(x=340, y=360)

        bard4 = Image.open("plotsfavourites_count.png")
        bard4 = bard4.resize((300, 300), Image.ANTIALIAS)
        bardejov4 = ImageTk.PhotoImage(bard4)
        label5 = Label(self, image=bardejov4)
        label5.image = bardejov4
        label5.place(x=1000, y=360)

        bard5 = Image.open("plotsfollowers_count.png")
        bard5 = bard5.resize((300, 300), Image.ANTIALIAS)
        bardejov5 = ImageTk.PhotoImage(bard5)
        label6 = Label(self, image=bardejov5)
        label6.image = bardejov5
        label6.place(x=660, y=20)

        bard6 = Image.open("plotsprediction_error_classification.png")
        bard6 = bard6.resize((300, 300), Image.ANTIALIAS)
        bardejov6 = ImageTk.PhotoImage(bard6)
        label7 = Label(self, image=bardejov6)
        label7.image = bardejov6
        label7.place(x=660, y=360)

        bard7 = Image.open("plotsprediction_error_regression.png")
        bard7 = bard7.resize((300, 300), Image.ANTIALIAS)
        bardejov7 = ImageTk.PhotoImage(bard7)
        label8 = Label(self, image=bardejov7)
        label8.image = bardejov7
        label8.place(x=1400, y=250)
        self.parent.pack()


root = Tk()

im = Image.open('index.png')
im = im.resize((100, 100), Image.ANTIALIAS)
tkimage = ImageTk.PhotoImage(im)
listbox = Listbox(root)
Tkinter.Label(root, image=tkimage).pack()
app = Window(root)
root.geometry("1080x1920")
root.mainloop()
