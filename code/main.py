import numpy as np
import json
import pickle
from extern.jobsuche_api import api_example as api
import itertools
from collections import Counter

def process_one_job(refnr, jwt):
    job_detail = api.job_details(jwt["access_token"], refnr)
    if "stellenbeschreibung" in job_detail:
        return job_detail["stellenbeschreibung"]
    else:
        print(job_detail)
        print(refnr)
        return ""


def process_one_page(result, jwt):
    page_stellen=[]
    untill= len(result['stellenangebote'])
    for i in range(0,untill):
        cur_refnr = result['stellenangebote'][i]["refnr"]
        print("Processing job ", i,  "with ref nr ", cur_refnr)
        cur_stellenbeschreibung = process_one_job(cur_refnr, result, jwt)
        page_stellen.append(cur_stellenbeschreibung)
    return page_stellen

def process_whole(beruf):
    jwt = api.get_jwt()
    alle_stellen=[]
    for i in range(1,101):
        print("Processing page: ", i)
        result_page_i = api.custom_search(jwt["access_token"], beruf, page=i)
        if "messages" in result_page_i or "stellenangebote" not in result_page_i:
            print("EMPTY")
            break
        page_stellen = process_one_page(result_page_i, jwt)
        alle_stellen.insert(-1,page_stellen)
    flat_list = list(itertools.chain(*alle_stellen))
    with open('data/'+str(beruf)+'/'+str(beruf)+'_1_100.pkl', 'wb') as f:
        pickle.dump(flat_list, f)



def arbeitsortAnalyse(beruf):
    jwt = api.get_jwt()
    regions = []
    for page in range(1, 101):
        result_page_i = api.custom_search(jwt["access_token"], beruf, page=page)
        if "messages" in result_page_i or "stellenangebote" not in result_page_i:
            print("EMPTY")
            break
        for entry in result_page_i['stellenangebote']:
            if 'region' in entry['arbeitsort']:
                cur_reg = entry['arbeitsort']['region']
            else:
                cur_reg = "Missing"
            regions.append(cur_reg)
    print(len(regions))
    counts = Counter(regions)
    print(counts)

def manual():
    jwt = api.get_jwt()
    result_page_i = api.custom_search(jwt["access_token"], "Metallbauer/in", page=1)
    tarifvertrag=[]
    fertigkeiten=[]
    staerken=[]
    sonstigesAusbildung=[]
    if "messages" in result_page_i or "stellenangebote" not in result_page_i:
        print("EMPTY")
    for entry in result_page_i['stellenangebote'][0:100]:
        cur_ref = entry["refnr"]
        job_detail = api.job_details(jwt["access_token"], cur_ref)
        #for k, v in job_detail.items():
        #    print(k, v)
        if "tarifvertrag" in job_detail:
            tarifvertrag.append(job_detail["tarifvertrag"])
        if "fertigkeiten" in job_detail:
            fertigkeiten.append(job_detail["fertigkeiten"])
        if "staerken" in job_detail:
            staerken.append(job_detail["staerken"])
        if "sonstigesAusbildung" in job_detail:
            sonstigesAusbildung.append(job_detail["sonstigesAusbildung"])

    # job_detail = api.job_details(jwt["access_token"], result['stellenangebote'][0]["refnr"])
    # print(json.dumps(job_detail, indent=4, sort_keys=False))
    counts = Counter(tarifvertrag)
    print(counts)
    #counts = Counter(fertigkeiten)
    print(fertigkeiten)
    #counts = Counter(staerken)
    print(staerken)
    counts = Counter(sonstigesAusbildung)
    print(counts)




if __name__ == "__main__":
    #manual()
    process_whole(beruf="Metallbauer/in")
    #process_one_page(0,result)
    #print(result['stellenangebote'][0]["refnr"])
    #process_one_job(result['stellenangebote'][0]["refnr"])
    #job_detail=api.job_details(jwt["access_token"], result['stellenangebote'][0]["refnr"])
    #print(json.dumps(job_detail, indent=4, sort_keys=False))

    #print(len(result['stellenangebote']))
    #print(result['stellenangebote'][0])