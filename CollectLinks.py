import os
import time
import pandas as pd
from requests_html import HTMLSession
from collections import defaultdict


class LinksScrapy():
    def __init__(self):
        self.exam = []
        self.links = pd.DataFrame()
        self.topics = defaultdict(list)

    def get_links(self,item,examname):
        """
        keyword,examname: str
        rtype: list
        """
        # All the links get from the discussion page
        url = "https://www.examtopics.com/discussions/"+item
        session = HTMLSession()
        kv = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"}
        response = session.get(url, headers = kv)
        discussion_info = response.html.xpath("//*[contains(@class,'pagination-container ml-auto')]/span",first=True).text
        page_number = discussion_info.split()[-1]
        print("The number of discussion pages is {0}".format(page_number))


        # link_list: contain all the discussion links
        # exam_list: contain all the exam related links
        link_list = [url+"/"+str(i) for i in range(1,int(page_number)+1)]
        exam_list = []

        for li in link_list:
            print("In {},".format(li))
            related_links_count  = 0
            li_response = session.get(li,headers=kv)
            # get all the links
            for link in li_response.html.absolute_links:
                if examname in link:
                    related_links_count += 1
                    exam_list.append(link)
                    print(link)
            print("-------------Total related exam links: {}".format(related_links_count)) 
            time.sleep(5)
        
        df = pd.DataFrame(exam_list,columns=["Links"])
        df.to_csv(link_save_path)
        print("Save links to the CSV file successfully!")
        return exam_list

if __name__=="__main__":
    root_path = os.path.dirname(os.path.abspath(__file__))
    link_save_path = root_path + './links.csv'
    dateset_save_path = root_path + './dataset.csv'
    
    a = LinksScrapy()
    """
    get_links: Get all the links from the discussion pages and save these contents into local CSV file.
    Usually run once is enough!
    """
    # Format https://www.examtopics.com/discussions/[google]/view/92468-exam-[professional-cloud-database-engineer]-topic-1-question-7/
    #                                               keyword1                  keyword2
    links = a.get_links("google","professional-cloud-database-engineer") # <-Replace your keyword here! 

