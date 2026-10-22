from cdsetool.query import query_features
from cdsetool.download import download_features
from cdsetool.credentials import Credentials

import click
import configparser
#from click import command, option, Option, UsageError

#import os,sys

#replicate this CLI query in python on CDSE

#cdsetool query search SENTINEL-3 --search-term contentDateStartGe=2026-09-04 --search-term contentDateStartLe=2026-09-05 \
# --search-term productType=SL_1_RBT___ --search-term name="S3B" 

#adding in ceda specific args, fudge for dev - need to sort this for CLI

@click.command()
@click.option('-e', '--endpoint', 'endpoint', type=str, required=False, help='Endpoint base name (omit odata/v1).  Defaults to cdse')
@click.option('-c', '--collection', 'collection', type=str, default='',required=False, help='Collection used on endpoint (if any)')
@click.option('-C', '--credentials', 'creds_file', type=str,required=False, help='Credentials file (.netrc format)')
@click.option('-S', '--start-date', 'start_date', type=str, required=False, help='start date')
@click.option('-E', '--end-date', 'end_date', type=str, required=False, help='end date')
@click.option('-P', '--product-type', 'product_type', type=str, required=False, help='product type i.e. "SL_1_RBT___"')
@click.option('-N', '--product-name', 'product_name', type=str, required=False, help='product name i.e. "S3A"')
@click.option('-p', '--paging', 'override_paging', type=str, required=False, help='Override default paging (100)')
def main(endpoint:str, collection:str, start_date:str, end_date:str, product_type:str, product_name:str, creds_file:str, override_paging:str):

    paging = 100 #set skip value

    if override_paging is not None:
        paging = override_paging

    #are credentials supplied?
    credentials = None
    if creds_file is not None:
        config = configparser.ConfigParser()
        config.read(creds_file)

        username=config['default']['user']
        password=config['default']['password']
        openid_configuration_endpoint=config['default']['openidConfiguration']
        clientid=config['default']['clientId']

 
    search_terms = {"top":paging,
        "contentDateStartGe": start_date,
        "contentDateStartLe": end_date,
        "productType": product_type,
        "name":product_name,
        }

    # wait for all batch requests to complete, returning list
    #features = list(query_features(collection, search_terms, options={'endpoint':endpoint, 'credentials':creds_file}))

    features = query_features(collection, search_terms, options={'endpoint':endpoint, 'username':username, 'password':password, \
                                                                      'openid_configuration_endpoint':openid_configuration_endpoint, 'clientid':clientid})

    print (f"found {len(list(features))}")
    

    # download first scene
    credentials = Credentials(username=config['default']['user'], \
                                      password=config['default']['password'], openid_configuration_endpoint=config['default']['openidConfiguration'], \
                                        clientid=config['default']['clientId'])
   
    downloads = download_features(features, "C://Downloads", {"credentials": credentials, "concurrency": 1,'endpoint':endpoint})

    for id in downloads:
        print(f"feature {id} downloaded")
    

    # wait for a single batch to finish, yield results immediately
    #scenes = query_features(collection, search_terms, endpoint)

    #print (f"found {len(scenes)} scenes")
    #cnt = 0
    #for feature in query_features(collection, search_terms):
    #    # do something with feature
    #    print (f"{feature['Id']}")
    #    cnt += 1
    #print (cnt)

    #set up credentials for using CEDA DHR
   
    # manually iterate
    #iterator = query_features(collection, search_terms)

    #featureA = next(iterator)
    #featureB = next(iterator)
    # ...

if __name__ == '__main__':
    main()

