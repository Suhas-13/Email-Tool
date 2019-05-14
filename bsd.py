from bs4 import BeautifulSoup
import requests
import multiprocessing
import sys

sess=requests.Session()
x=sess.get("https://www.freebsd.org/doc/en_US.ISO8859-1/books/handbook/eresources-mail.html")
soup=BeautifulSoup(x.text,'html.parser')
listofurls=[]
for i in soup.find_all("a",href=True):
	if "mailman" in i['href']:
		if len(i['href'].split("listinfo/")) > 1:
			listofurls.append(i['href'].split("listinfo/")[1])
global emails
emails=sys.argv[1]
print(sys.argv[1])
def email(i):
        try:
                auth=sess.get('https://lists.freebsd.org/mailman/listinfo/' + i)
                auth=auth.text[auth.text.find("sub_form_token"):auth.text.find("sub_form_token")+300].split('"')[2]
                b=sess.post('https://lists.freebsd.org/mailman/subscribe/'+i,data={"sub_form_token":auth,"email":emails,"digest":"0","email-button":"Subscribe"})
                print(b)
        except Exception as e:
                print(e)
if __name__ == '__main__':
        with multiprocessing.Pool(processes=len(listofurls)) as pool:
                results = pool.map(email, listofurls)
 
