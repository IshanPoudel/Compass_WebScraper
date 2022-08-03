import mysql.connector
from random import randint
import xlrd
import pandas as pd
import config


def export_to_excel():


    db = mysql.connector.connect(host="localhost",
                                 user=config.user,
                                 passwd=config.password,
                                 db='real_estate'

                                 )

    mycursor = db.cursor()


    #fetch
    query = "select * from final_agent order by agent_id desc "
    mycursor.execute(query)
    rows = mycursor.fetchall()

    first_name_last_name= []
    for values in rows:

        print(values)
        first_name_last_name = values[2].split(" " , 1)
        print(first_name_last_name[0])
        print(first_name_last_name[1])


    df = pd.DataFrame(rows , columns= ('Agent_ID' , 'TexasRealEstateAgentID' , 'Name' , 'Phone' , 'email' , 'Agent_Address' , 'House_Address' , 'House_Link'))



    df.to_excel(r'Final_Excel.xlsx' , index=False)
