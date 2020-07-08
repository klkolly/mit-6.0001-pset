# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

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

# TODO: NewsStory
class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        self.guid=guid
        self.title=title
        self.description=description
        self.link=link
        self.pubdate=pubdate
    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_description(self):
        return self.description
    def get_link(self):
        return self.link
    def get_pubdate(self):
        return self.pubdate




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
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self,phrase):
        self.trigger = phrase
    def is_phrase_in(self, text):
        # deal with text to see if phrase in text
        #first replace  puctuation to space. ,then replace space*2 to space loop until new len == old len. then  phrase.lower in dealed_text
        #maybe use 're' will be easy

        deal_text =''
        for char in text:
            if char in string.punctuation:
                deal_text +=' '
            else:
                deal_text += char
        latest_text_len = len(deal_text)

        while True:
            deal_text=deal_text.replace("  "," ")
            if latest_text_len > len(deal_text):
                latest_text_len = len(deal_text)
            else:
                break

        deal_text= deal_text.lower().replace(self.trigger.lower(),"*")
        deal_text_list = deal_text.split()

        return '*' in deal_text_list
    
    def get_trigger(self):
        return self.trigger
    
    def change_trigger(self,trigger):
        self.trigger = trigger






# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())

# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())


# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

class TimeTrigger(Trigger):
    def __init__(self,EST_time):
        self.trigger = datetime.strptime(EST_time,"%d %b %Y %H:%M:%S")


    def get_datetime(self):
        return self.trigger
    
    def change_trigger(self,EST_time):
        self.trigger = datetime.strptime(EST_time,"%d %b %Y %H:%M:%S")





# Problem 6
# TODO: BeforeTrigger and AfterTrigger


class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):

        #print("self.get_datetime()",self.get_datetime())
        #print("story.get_pubdate()",story.get_pubdate())
        return self.get_datetime() > story.get_pubdate().replace(tzinfo=None)


class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        return self.get_datetime() < story.get_pubdate().replace(tzinfo=None)

#self.get_datetime() 2016-10-12 23:59:59
#story.get_pubdate() 1987-10-15 00:00:00-05:00
#ERROR
#can't compare offset-naive and offset-aware datetimes   add timezone
#self.datetime = self.datetime.replace(tzinfo=pytz.timezone('UTC'))



# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):

    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, story):
        return not self.trigger.evaluate(story)
    def change_trigger(self,trigger):
        self.trigger = trigger


# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    def evaluate(self, story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)



# Problem 9
# TODO: OrTrigger

class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    def evaluate(self, story):
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)



#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    
    filtered_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filtered_stories.append(story)
        
    
    #return stories
    return filtered_stories



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

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    

    print(lines) # for now, print it so you see what it contains!
    # dict of function 
    trigger_dict={'TITLE':TitleTrigger, 'DESCRIPTION':DescriptionTrigger, \
                         'AFTER':AfterTrigger , 'BEFORE': BeforeTrigger,  \
                         'NOT':NotTrigger}
    trigger_composite_dict={'AND':AndTrigger, 'OR':OrTrigger}
    
    
    triggerdict={}
    triggerlist=[]
   
    for line in lines:
        line_list=line.split(',')
        if line_list[0]=='ADD':
            break

        
        if line_list[1] not in ['AND','OR','NOT']:
            triggerdict[line_list[0]] = trigger_dict[line_list[1]](line_list[2])
            
        elif not line_list[1]=='OR':
            triggerdict[line_list[0]] = trigger_composite_dict[line_list[1]](line_list[2], line_list[3])

        else:
            triggerdict[line_list[0]] =NotTrigger(line_list[2])
            
    print(triggerdict)
    print(triggerdict['t1'].get_trigger())
    for i in range(1,len(line_list)):
        triggerlist.append(triggerdict[line_list[i]])
    print(triggerlist)
    return triggerlist
    


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("COVID")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        #triggerlist = [t1]

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

        t = "Google Top News(not yahoo)" 
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
            #stories.extend(process("http://news.yahoo.com/rss/topstories"))

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

