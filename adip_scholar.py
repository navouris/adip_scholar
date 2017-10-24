'''
adip_scholar v 0.9 Nikos Avouris - October 2017
# python3 script tested with python 3.6
input: αρχείο researchers_url.csv με δύο στήλες, όνομα ερευνητή και url προφιλ στο Google scholar
πχ.
"Einstein Albert","https://scholar.google.gr/citations?user=qc6CJjYAAAAJ&hl=el&oi=ao"
Παράγει στην έξοδο αρχείο citations_[year].csv
'''

from bs4 import BeautifulSoup
import os.path
import datetime
import urllib.request
import urllib.parse
import os
import shutil


class Researcher():
    theResearchers = {}

    def __init__(self, name, url):
        self.name = name.strip('"')
        self.url = url.strip('"')
        self.cash_url_file()
        self.citations = {}
        self.cashed_file = ''
        if self.cash_url_file(): self.find_citations()
        Researcher.theResearchers[name] = self

    def __str__(self):
        out = self.name+';'
        for x in self.citations:
            out += str(x)+':'+ str(self.citations[x])+';'
        if out[-1] == ';': out = out[:-1]
        return out

    def cash_url_file(self):
        # create dir if it does not exist
        if not os.path.exists("html_cash_" + str(Report.Year)):
            os.makedirs("html_cash_" + str(Report.Year))
        cashed_file = self.name + ".html"
        try:
            cashed_filename = os.path.join('html_cash_' + str(Report.Year), cashed_file)
            if not os.path.isfile(cashed_filename) :
                with urllib.request.urlopen(self.url) as response:
                    with open(cashed_filename, 'wb') as fout:
                        shutil.copyfileobj(response, fout)
            self.cashed_file = cashed_filename
            return True
        except:
            print('error in cashfile creation')
            return False

    def find_citations(self):
        if not os.path.isfile(self.cashed_file): return False
        try:
            with open(self.cashed_file, 'rb') as file:
                html = file.read()
        except: return False

        list_years = []
        citation_count = []
        soup = BeautifulSoup(html, "lxml")
        citation_years = soup.find(id="gsc_g_x")  ### it returns none!!! (2016 version)
        print(citation_years)
        if citation_years:
            # this is the table of citation chart years
            ly = citation_years.findAll("span", {"class": "gsc_g_t"})
            for l in ly:
                list_years.append(l.get_text())
            print('list_years', list_years)
        ly = soup.findAll("span", {"class": "gsc_g_t"})
        for l in ly:
            list_years.append(l.get_text())
        print('list_years', list_years, len(list_years))
        citations_per_year = soup.findAll("span", {"class": "gsc_g_al"})
        for cit in citations_per_year:
            citation_count.append(cit.get_text())
        print('citation_count', citation_count, len(citation_count))
        ########## store citations
        if len(citation_count) <= len(list_years):
            for i in range(len(citation_count)):
                _j = len(list_years) - len(citation_count) + i
                self.citations[list_years[_j]] = citation_count[i]
        print(self.citations)

        citations_table = soup.find('table', {'id': "gsc_rsb_st"})
        if citations_table:
            datah = citations_table.findAll('th')
            data = citations_table.findAll('td')

            if len(datah) == 3 and len(data) % len(datah) == 0:
                headers = [x.get_text() for x in datah]
                values = [x.get_text() for x in data]
                for v in headers:
                    print(v)
                for v in values:
                    print(v)
                key1 = ''
                i = 0
                for v in values:
                    if i % 3 == 0:
                        key1 = v
                    elif i % 3 == 1:
                        self.citations[key1 + headers[1]] = int(v)
                    elif i % 3 == 2:
                        self.citations[key1 + headers[2]] = int(v)
                    i += 1
        print(self.citations)


    @staticmethod
    def load_researchers_data():
        # loads and caches web pages
        with open('researchers_url.csv', 'r', encoding='utf-8') as fin:
            for line in fin:
                print(line)
                line = line.split(",")
                name = line[0].strip()
                if len(line)> 1 and 'http' in line[1]:
                    url = line[1].strip().replace('=el', '=en')
                    print(url)
                    r = Researcher(name, url)


class Report():
    # Reporting class, for Year, if none given, runs for current year - 1
    Year = int(datetime.datetime.today().strftime("%Y")) - 1

    @staticmethod
    def set_year():
        in_y = input('Ανάκτηση αναφορών από το Google Scholar \nΈτος αναφοράς[{}]:'.format(Report.Year))
        if in_y.isdigit() and Report.Year > int(in_y) >= 2010 :
            Report.Year = int(in_y)
        print('έναρξη ανάκτησης δεδομένων από  Scholar για το {} ....'.format(Report.Year))

    @staticmethod
    def prepare_report():
        out = 'Researcher Name;h-index;Citations;'
        for x in range(5): out += str(Report.Year - 4 + x) + ';'
        if out[-1] == ';': out = out[:-1]
        for res_name in Researcher.theResearchers:
            r = Researcher.theResearchers[res_name]
            #print(res_name, r.citations)
            out += '\n' + r.name+';'
            if 'h-indexΌλα' in r.citations.keys():
                try:
                    out += str(r.citations['h-indexΌλα']) + ';' + str(r.citations['ΠαραθέσειςΌλα']) + ';'
                except: pass
            else:
                try:
                    out += str(r.citations['h-indexAll']) + ';' + str(r.citations['CitationsAll']) + ';'
                except:
                    print('BIG MISTAKE!!')
                    pass
            try:
                for y in range(5):
                    key = str(Report.Year - 4 + y)
                    out += r.citations[key]+';'
            except: pass
            if out[-1] == ';': out = out[:-1]

        with open(os.path.join('html_cash_'+ str(Report.Year), 'citations_' + str(Report.Year) + '.csv'), 'w', encoding='utf-8') as fout:
            fout.write(out)
        print(out)


def main():

    Report.set_year()  # decide year, if none given, runs for current year - 1
    Researcher.load_researchers_data()  # load data from urls based on file researchers_url.csv
    Report.prepare_report() # file report
    for r in Researcher.theResearchers:
        print(Researcher.theResearchers[r])


if __name__ == '__main__': main()
