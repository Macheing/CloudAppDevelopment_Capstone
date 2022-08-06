import requests
import json
import logging
from requests.auth import HTTPBasicAuth
# import related models here
from .models import *

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


def get_request(url, **kwargs):
    '''
     Create a `get_request` to make HTTP GET requests
    '''
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def post_request(url, json_payload, **kwargs):
    '''
     Create a `post_request` to make HTTP POST requests
    '''
    print(kwargs)
    print("POST to {} ".format(url))
    print(json_payload)
    try:
        response = requests.post(url, json=json_payload, params=kwargs)
    except:
        print("Something went wrong")
        return response.status_code
    return response


def get_dealers_from_cf(url, **kwargs):
    '''
     Create a get_dealers_from_cf method to get dealers from a cloud function.
     Call get_request() with specified arguments
     Parse JSON results into a CarDealer object list
    '''
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["entries"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"], state = dealer["state"],
                                   st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)
    return results
'''
# convert to json objects
def dealer_json_to_object(dealer):
    return CarDealer(
                    address=dealer["address"], 
                    city=dealer["city"], 
                    full_name=dealer["full_name"],
                    id=dealer["id"], 
                    lat=dealer["lat"], 
                    long=dealer["long"],
                    short_name=dealer["short_name"],
                    st=dealer["st"], 
                    zip=dealer["zip"],
                    )
# find dealership by state
def get_dealers_by_state(state="CA"):
    try:
        response = service.post_find(db='dealerships',
        selector={"st": state},).get_result()['entries']
        return [dealer_json_to_object(dealer) for dealer in response]
    except:
        print("Something went wrong with get_dealer_by_state()")
'''

def get_dealer_reviews_by_id_from_cf(url, dealerId):
    '''
     Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
     Call get_request() with specified arguments
     Parse JSON results into a DealerView object l
    '''
    results = []
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        reviews = json_result['entries']
        for review in reviews:
            try:
                review_obj = DealerReview(name = review["name"], dealership = review["dealership"], 
                                review = review["review"], purchase=review["purchase"],
                                purchase_date = review["purchase_date"], car_make = review['car_make'],
                                car_model = review['car_model'], car_year= review['car_year'], sentiment= "none")
            except:
                review_obj = DealerReview(name = review["name"], 
                dealership = review["dealership"], review = review["review"], purchase=review["purchase"],
                purchase_date = 'none', car_make = 'none',
                car_model = 'none', car_year= 'none', sentiment= "none")
                
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            print(review_obj.sentiment)
                    
            results.append(review_obj)

    return results

def analyze_review_sentiments(text):
    '''
    Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
    Get the returned sentiment label such as Positive or Negative
    '''
    api_key = "KhdinpCJynzn6cXzvSfHk5a1PfrUAilzYgDzTcDUCXRg"
    url = "https://api.us-south.language-translator.watson.cloud.ibm.com/instances/7702544d-823d-4b52-bec3-a93cfe42ada8"
    texttoanalyze= text
    version = '2020-08-01'
    authenticator = IAMAuthenticator(api_key)
    nlu = NaturalLanguageUnderstandingV1(version='2020-08-01',authenticator=authenticator)
    nlu.set_service_url(url)
    response = nlu.analyze(text=text,
                    features= Features(sentiment= SentimentOptions())).get_result()
    print(json.dumps(response))
    sentiment_score = str(response["sentiment"]["document"]["score"])
    sentiment_label = response["sentiment"]["document"]["label"]
    print(sentiment_score)
    print(sentiment_label)
    sentimentresult = sentiment_label
    
    return sentimentresult


