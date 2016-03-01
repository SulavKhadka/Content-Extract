from easygui import * 
import string
import re
import datetime
from textblob import TextBlob
from dateutil.parser import parse


def time_date_ext(sentence):
    ''' Find Dates and Times '''
    datetime_keyword_lst =(':','today','tomorrow','yesterday','am','a.m','a.m.','pm','p.m','p.m.','january','february','march','april','may','june','july','august','september','october','november','december')
    try:
        for keyword in datetime_keyword_lst:
            if keyword in sentence:
                p = parse(sentence, fuzzy=True)
                td_lst =  str(p).split(" ")
                date_lst = td_lst[0].split("-")
                time_lst = td_lst[1].split(":")
                if "tomorrow" in sentence:
                    date_lst[2] = int(date_lst[2]) + 1
                elif "yesterday" in sentence:
                    date_lst[2] = int(date_lst[2]) - 1

                dt = datetime.datetime(int(date_lst[0]),int(date_lst[1]),int(date_lst[2]),int(time_lst[0]),int(time_lst[1]),int(time_lst[2]))
                p = [str(dt.year) + "-" + str(dt.month) + "-" + str(dt.day) +
                     " " + str(dt.hour) + ":" + str(dt.minute) + ":" + str(dt.second)]
                break
            else:
                p = "None"
        return p
    
    except ValueError:
        return "None"

def email_ext(sentence):
    ''' Find Email Adresses '''
    expression = re.compile(r"(\S+)@(\S+)")
    result = expression.findall(sentence)
    if result != []:
        return result    
    else:
        return "None"
    
def phone_num_ext(sentence):
    ''' Find Phone Numbers '''
    reg = re.compile(".*?(\(?\d{3}\D{0,3}\d{3}\D{0,3}\d{4}).*?", re.S)
    num = reg.findall(sentence)
    parsed_phnumbers = []
    for ph_numbers in num:
        all=string.maketrans('','')
        nodigs=all.translate(all, string.digits)
        ph_numbers = ph_numbers.translate(all, nodigs)
        if ph_numbers != '':
            parsed_phnumbers.append(ph_numbers)
    if parsed_phnumbers != []:
        return parsed_phnumbers   
    else:
        return "None"

def names_ext(sentence):
    ''' Extracts Names using first_name_search and last_name_search '''
    sentence = TextBlob(sentence)
    possible_names = sentence.noun_phrases
    print "NOUN PHRASES: ", possible_names
    sentence = sentence.ngrams(n=2)
    names = []
    female_first = open('./Names_db/Females_Firsts.txt').read().strip().split("\n")
    male_first = open('./Names_db/Males_Firsts.txt').read().strip().split("\n")
    all_last = open('./Names_db/Last_Namess.txt').read().strip().split("\n")

    for phrases in sentence:
        female_names = first_name_search(phrases[0],female_first)
        male_names = first_name_search(phrases[0],male_first)
        last_names = last_name_search(phrases[1],all_last)
        if female_names and male_names and last_names != "None":
            print female_names
            print male_names
            print last_names, "\n"
    return "None"

def first_name_search(name_candidate, name_list):
    ''' Looks for the first name in the name list '''
    return name_candidate.lower() in name_list

def last_name_search(name_candidate, name_list):
    ''' Looks for the last name in the name list '''
    last_names = []
    for name in name_list:
        if name_candidate.lower() == name.strip().lower():
            last_names.append(name_candidate)
    if last_names != []:
        return last_names
    else:
        return "None"

def main():
    ''' Extract Data from a given body of text '''
    sentence = enterbox("Please enter a sentence to parse").lower()
    SKtime_date = time_date_ext(sentence)
    if SKtime_date != "None":
        SKdate = SKtime_date[0]
        SKtime = SKtime_date[1]
    else:
        SKdate = "None"
        SKtime = "None"

    SKemail = email_ext(sentence)
    if SKemail != "None":
        SKemail = SKemail[0][0] + "@" + SKemail[0][1]

    SKnames = names_ext(sentence)
    Names = "None"
    if SKnames!= "None":
        Names = SKnames[0] + ", "
        for name in SKnames[1:]:
            if name != SKnames[-1]:
                Names += name + ", "
            else:
                Names += name

    SKphonenumbers = phone_num_ext(sentence)
    phonenumbers = "None"
    if SKphonenumbers != "None":
        phonenumbers = SKphonenumbers[0] + ", "
        for number in SKphonenumbers[1:]:
            if number != SKphonenumbers[-1]:
                phonenumbers += number + ", "
            else:
                phonenumbers += number


    msgbox("Time: " + SKtime + "\n"
           + "Date: " + SKdate + "\n"
           + "Email: " + SKemail + "\n"
           + "Phone: " + phonenumbers + "\n"
           + "Names: " + Names)
