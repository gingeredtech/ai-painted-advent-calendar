import urllib.request
import config
import requests
import urllib.request
from os.path import exists

def aipaint(description):
    r = requests.post(
        "https://api.deepai.org/api/impressionism-painting-generator",
        data={
            'text': description,
        },
        headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
    )

    ret = r.json()
    return ret

count=1

while count<=25:
    
    # pop off the first image description 
    description=config.descriptions.pop(0)
    # push it back on at end (this ensures we cycle through descriptions and never run out )
    # obviously best is there are 25 descriptions though
    config.descriptions.append(description)
    
    filename='./images/image'+ (f"{count:02d}") +".jpg"
    if(exists(filename)):
        print(filename+" already exists")
    else:
        print("Painting: "+description)
        try:
            painting=aipaint(description)
            if(len(painting)<2):
                if(painting['status']):
                    print("You've probably run out of deepai (free) credits.")
                    print("Status returned "+painting['status'])
            else:
                print("Storing as "+filename)
                urllib.request.urlretrieve(painting['output_url'], filename)
                print("Paint now dried on "+filename)     
        except Exception as ex:
            print("Paint "+filename+" failed")
            print(ex)

    count+=1

print("Paintings complete and paint has dried!")
print("Now run main.py to access the Advent calendar")

