# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

from cmath import phase
from mailbox import linesep
from posixpath import split
import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
    
    def get_guid(self):
        return(self.guid)
    
    def get_title(self):
        return(self.title)

    def get_description(self):
        return(self.description)
    
    def get_link(self):
        return(self.link)

    def get_pubdate(self):
        return(self.pubdate)


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhaseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase

    def is_phrase_in(self, text):
        phrase = self.phrase.lower()
        phrase = phrase.split()
        text = text.lower()

        punc_dict = dict()
        for character in string.punctuation:
            punc_dict[character] = " "
        new_text = text.translate(str.maketrans(punc_dict))
        new_text = new_text.split()
        
        index_list = [i for i in range(len(new_text)) if phrase[0] == new_text[i]]

        for i in index_list:
            if phrase == new_text[i:i+len(phrase)]:
                return(True)
            else:
                return(False)
# Problem 3
class TitleTrigger(PhaseTrigger):
    def __init__(self, phrase):
        PhaseTrigger.__init__(self, phrase)
    
    def evaluate(self, story):
        title = story.get_title()

        return(TitleTrigger.is_phrase_in(self, title))

# Problem 4
class DescriptionTrigger(PhaseTrigger):
    def __init__(self, phrase):
        PhaseTrigger.__init__(self, phrase)
    
    def evaluate(self, story):
        description = story.get_description()

        return(DescriptionTrigger.is_phrase_in(self, description))

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, timestr):
        self.time = datetime.strptime(timestr, "%d %b %Y %H:%M:%S")

# Problem 6
class BeforeTrigger(TimeTrigger):
    def __init__(self, timestr):
        TimeTrigger.__init__(self, timestr)
    
    def evaluate(self, story):
        pubtime = story.get_pubdate()
        if pubtime.tzinfo is not None:
            self.time = self.time.replace(tzinfo=pytz.timezone("EST"))

        if pubtime < self.time:
            return(True)
        else:
            return(False)

class AfterTrigger(TimeTrigger):
    def __init__(self, timestr):
        TimeTrigger.__init__(self, timestr)
    
    def evaluate(self, story):
        pubtime = story.get_pubdate()
        if pubtime.tzinfo is not None:
            self.time = self.time.replace(tzinfo=pytz.timezone("EST"))

        if self.time < pubtime:
            return(True)
        else:
            return(False)

# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger
    
    def evaluate(self, story):
        return(not self.trigger.evaluate(story))

# Problem 8
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    
    def evaluate(self, story):
        return(self.trigger1.evaluate(story) and self.trigger2.evaluate(story))

# Problem 9
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    
    def evaluate(self, story):
        return(self.trigger1.evaluate(story) or self.trigger2.evaluate(story))


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    filtered_stories = list()
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filtered_stories.append(story)
            else:
                continue

    return(filtered_stories)



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    def trigger_match(type, trigger_types):
        for trigger in trigger_types:
            if type.lower() == trigger[:len(type)].lower():
                return(trigger)

    trigger_types = ["TitleTrigger", "DescriptionTrigger", "BeforeTrigger", "AfterTrigger", "AndTrigger", "OrTrigger", "NotTrigger"]
    pot_triggers = dict()
    trigger_list  = list()
    for trigger in lines:
        splittedtrigger = trigger.split(",")
        name = splittedtrigger[0]

        if name != "ADD":
            type = splittedtrigger[1]
            filter = splittedtrigger[2:]

            trigger_type = trigger_match(type, trigger_types)
            if trigger_type in trigger_types[:4]:
                trig = trigger_type + "(\"" + filter[0] + "\")"
            elif trigger_type == "NotTrigger":
                trig = trigger_type + "(" + "pot_triggers[\"" + filter[0] + "\"]"
            else:
                trig = trig = trigger_type + "(" + "pot_triggers[\"" + filter[0] + "\"]," + "pot_triggers[\"" + filter[1] + "\"]" + ")"
            pot_triggers[name] = eval(trig)
        else:
            for element in splittedtrigger[1:]:
                trigger_list.append(pot_triggers[element])

    return(trigger_list)


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("COVID")
        t2 = DescriptionTrigger("cases")
        t3 = AndTrigger(t1, t2)
        triggerlist = [t3]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            # stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

