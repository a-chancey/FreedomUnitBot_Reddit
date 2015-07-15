import time
import pint
from pint import UnitRegistry
import praw
import re
import string
import os
import math

    
def matcher(match, splitter, metric, imperial):
    i = 0
    while i < length -1:
        #print(match.groups())
        results = match.group(i)
                            
        if results is not None:
            results = results.split(' ')
            results_nil = re.findall(r"\d", results[0])

            if results[0] is not None and len(results_nil) >= 1:
                if len(results) <= 1:
                    results = results[0].lower().split(splitter)
                    unit = Q_(float(results[0]), metric)
                else:
                    unit = Q_(float(results[0]), metric)
                
                converted = '{:.02fP}'.format((unit.to(imperial)))
                output = '%s is roughly equal to %s' % (unit, converted)
                reply.append(output)
        i += 1


ureg = UnitRegistry()
Q_ = ureg.Quantity
posts_replied = []

r = praw.Reddit('FreedomUnitBot 0.2 by /u/abchiptop')
r.login('[USERNAME]', '[PASSWORD]')

keep_on = True
while (keep_on):
    try:
               
        reply = []
        mentions = r.get_mentions('FreedomUnitBot')
        
        for mention in mentions:
            reply_id = 'replace'
            comment = r.get_info(thing_id=mention.parent_id)

            
            if reply_id == 'replace':
                reply_id = mention.name
                reply_to = r.get_info(thing_id=mention.name)
           
            if not os.path.isfile("posts_replied_to.txt"):
                posts_replied_to = []
            else:
                with open("posts_replied_to.txt", "r") as f:
                   posts_replied_to = f.read()
                   posts_replied_to = posts_replied_to.split("\n")
                   posts_replied_to = filter(None, posts_replied_to)
               
            if reply_id not in posts_replied_to:
                print('havent replied here yet!')
                
                for match in re.finditer(r"(?i)\d*\.?\d+\s*((meter)(s?)|(m\s?))", comment.body):
                    
                    length = len(match.groups())
                    if length is not 0:
                        matcher(match, 'm', 'meter', 'foot')

                for match in re.finditer(r"(?i)\d*\.?\d+\s*((centimeter)(s?)|(cm\s?))", comment.body):
                    
                    length = len(match.groups())
                    if length is not 0:
                        matcher(match, 'c', 'centimeter', 'inch')
                        
                for match in re.finditer(r"(?i)\d*\.?\d+\s*((millimeter)(s?)|(mm\s?))", comment.body):
                    
                    length = len(match.groups())
                    if length is not 0:
                        matcher(match, 'm', 'millimeter', 'inch')
                        
                
                for match in re.finditer(r"(?i)\d*\.?\d+\s*((kilometer)(s?)|(km\s?))", comment.body):
                
                    length = len(match.groups())
                    if length is not 0:
                        matcher(match, 'k', 'kilometer', 'mile')
                        
            
                for match in re.finditer(r"(?i)\d*\.?\d+\s*((gram)(s?)|(g\s?))", comment.body):

                    length = len(match.groups())
                    if length is not 0:
                        matcher(match, 'g', 'gram', 'ounce')
                        
                
               # print('matching milligrams')
                for match in re.finditer(r"(?i)\d*\.?\d+\s*((milligram)(s?)|(mg\s?))", comment.body):
                    #print('match is valid')
                    length = len(match.groups())
                    if length is not 0:
                       matcher(match, 'm', 'milligram', 'ounce')
                       
                for match in re.finditer(r"(?i)\d*\.?\d+\s*((kilogram)(s?)|(kg\s?))", comment.body):
                    
                    length = len(match.groups())
                    if length is not 0:
                        matcher(match, 'k', 'kilogram', 'pound')
                        
                for match in re.finditer(r"(?i)\d*\.?\d+\s*((centigram)(s?)|(cg\s?))", comment.body):
                    #print('match is valid')
                    length = len(match.groups())
                    if length is not 0:
                        matcher(match, 'c', 'centigram', 'ounce')
                       
                for match in re.finditer(r"(?i)\d*\.?\d+\s*((liter|litre)(s?)|(l\s?))", comment.body):
                    #print('match is valid')
                    length = len(match.groups())
                    if length is not 0:
                        matcher(match, 'l', 'liter', 'gallon')
                       
                for match in re.finditer(r"(?i)\d*\.?\d+\s*((milliliter|millilitre)(s?)|(ml\s?))", comment.body):
                    #print('match is valid')
                    length = len(match.groups())
                    if length is not 0:
                        matcher(match, 'm', 'milliliter', 'floz')
                       
                #print('matching temp')
                for match in re.finditer(r"(?i)\d+\s?(centigrade)\s|\d+\s?(celsius)\s|\d+\s?(c)\s", comment.body):
                    #print('match is valid')
                    length = len(match.groups())
                    if length is not 0:
                        matcher(match, 'c', 'degC', 'degF')
                        
                
                print( "Bot replying to : %s" % (reply_id))
                if reply is None:
                    reply.append("There doesn't seem to be any values that need freed."
                                 " We don't handle currency, because if it can't be bought with American money, "
                                 "it isn't worth owning. \n\n")
                reply.append('This is the FreedomUnit Converter Bot v0.2. If you have any questions, contact /u/abchiptop\n\n'
                
                             'I wish I knew plurals :(')
                reply_out = '\n\n'.join(reply)
                mention.reply(reply_out)
                #print(reply_out)
                posts_replied.append(reply_id)
                with open("posts_replied_to.txt", "a") as f:
                    for post_id in posts_replied:
                       f.write(post_id + "\n")
                print('sleep')
                reply_out = []
                reply_id = []
                posts_replied = []
                time.sleep(30)
            else:
                print('no new messages')
                print('sleep for 30')
                time.sleep(30)
            time.sleep(30)
        
    except praw.errors.RateLimitExceeded as err:
        print ("you're commenting too often")
        time.sleep(600)
        reply_out = []
        reply_id = []
        break
    
