# -*- coding: utf-8 -*-

import csv
import SETTINGS
from faker import Faker
from random import choice
    
def generatedb():

    fake = Faker(['pl_PL'])
    random_list = [0]*4+[1] # 80%/20%
    
    with open('database.csv','w',newline='\n') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=";", quotechar='|')
    
        for row in range(SETTINGS.FAKE_DATABASE_RECORDS):
            fake_name = fake.company()
            if SETTINGS.TEST_MODE == True:
                fake_mail = SETTINGS.TEST_MAIL
            else:
                fake_mail = fake.company_email()
            fake_date = fake.date_between(start_date='-2y6m', end_date='-1d')
            fake_years = choice(random_list)+1
            spamwriter.writerow([fake_name,fake_mail,fake_date,fake_years])
            
    print("Fake database succesfully created.")
            
if __name__ == "__main__":
    generatedb()