import os

def Output(content,filename):
    if(os.path.isfile("Scraped/"+filename)):
        os.remove("Scraped/"+filename)

    with open("Scraped/"+filename, "a") as f:
                        print(content,file=f)

def AppendOutput(content,filename):
        with open("Scraped/"+filename,"a") as f:
                print(content,file=f)