# Information from web
import urllib.request
import bs4 as bs
import pickle


# Writing into file from wikipedia
def wiki(crm):
    cm = crm[0].upper()
    for i in range(1, len(crm)):
        if crm[i] == " ":
            cm += "_"
        else:
            cm += crm[i]
    cm.capitalize()

    # Main
    with open("Crime.dat", 'ab+') as file:
        source = urllib.request.urlopen(f"https://en.wikipedia.org/wiki/{cm}")
        soup = bs.BeautifulSoup(source, 'lxml')
        body = soup.body
        n = body.find_all('p', limit=2)
        info = ''
        temp = ''
        for i in n:
            temp += str(i.text)
        for i in temp:
            if i.isdigit() == True or i in ['[', ']']:
                info += ''
            else:
                info += i

        d = {f"{crm}": info}
        pickle.dump(d, file)


crime = input("Enter crime: ")
wiki(crime)

