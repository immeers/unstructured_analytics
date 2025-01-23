import pandas as pd
import requests

# The first thing that I have to do is to get an access token
# and a secret key.
kroger_k = "udatest-24326124303424544a614c676f52496b616a4942433763535243542f2e33393963717a514f564754384d396a616c2f49426c6f383264686f6b746d654242563327751119650"
kroger_s = "32z9D9vTt3iznG34FqQdpo9Zhi5_QJGMPvcJpXIk"

auth_request = requests.post("https://api.kroger.com/v1/connect/oauth2/token",
                                headers = {"Content-Type": "application/x-www-form-urlencoded"},
                                data = {"grant_type": "client_credentials",
                                        "scope": "product.compact"},
                                auth = (kroger_k, kroger_s))


access_token = auth_request.json()["access_token"]

location_link = "https://api.kroger.com/v1/locations?filter.zipCode.near=46545"

location_request = requests.get(location_link, headers = {"Authorization": f"Bearer {access_token}"})

location_request.json()

location_id = location_request.json()["data"][0]["locationId"]

search_term = "pumpkin%20cookies"

product_link = f"https://api.kroger.com/v1/products?filter.term={search_term}&filter.locationId={location_id}"

product_request = requests.get(product_link, headers =
                                    {"Authorization": f"Bearer {access_token}",
                                     "Cache-Control": "no-cache",
                                     "Content-Type": "application/json; charset=utf-8"})

product_data = product_request.json()

product_data["data"][0]["description"]

product_data["data"][0]["aisleLocations"]


link = "https://www.indiegogo.com/private_api/graph/query?operation_id=discoverables_query"

request_body = {
  "variables": {
    "category_main": None,
    "category_top_level": None,
    "feature_variant": "none",
    "page_num": 1,
    "per_page": 12,
    "project_timing": "all",
    "product_stage": "all",
    "ended_campaigns_included": False,
    "project_type": "campaign",
    "q": "friday the 13th",
    "sort": "trending",
    "tags": []
  }
}

headers = {
    "Host": "www.indiegogo.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
    "Accept": "application/json",
    "Accept-Language":  "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Content-Type": "application/json",
    "X-CSRF-Token": "3WLX7F/CjQ79KVcukV69x5o0gukO9EQ/IomprHM+1fgMBifZBzIuUpTudUMiiPnNo0oeRsdxWhUwETUT/zAnWQ==",
    "Content-Length": '268',
    "Origin": "https://www.indiegogo.com",
    "DNT": "1",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    "Referer": "https://www.indiegogo.com/explore/all?project_timing=all&product_stage=all&ended_campaigns_included=false&sort=trending&q=friday%20the%2013th",
    "Cookie":  "romref=shr-pies; romref_referer_host=www.indiegogo.com; cohort=www.indiegogo.com%7Csch-goog%7Cshr-pies; visitor_id=8b5ed3085419f43d45622aad67c29e21a4561a011450d70f6c20e80d3437c355; recent_project_ids=2974369; _session_id=39f1b783ac0353f4a7325325fd554d81; x-spec-id=61e63a039946b8e1e54c52e5d10c648c; localCurrencyIsoCode=USD; __stripe_mid=35aa65f7-acb6-4a87-a628-4bda68a1d246aa5edd; __stripe_sid=ad0a0ade-1732-46ff-b4fe-ebaad3bb3dc1a01af6; analytics_session_id=d2b40c0481a31ccb58b44895bfff9797c6cc72ca07a5c43c7de8d85930b17f49; accessibilityNoticeRenderedOnce=true; confidence_page_tracking_session_id=9f37bd09-f325-4c8b-a9fb-28ea7baf0cc6",
    "Sec-Fetch-Dest":  "empty",
    "Sec-Fetch-Mode":  "cors",
    "Sec-Fetch-Site":  "same-origin",
    "TE":  "trailers"
}

f13_fan_films = requests.post(link, headers = headers, json = request_body)

f13_fan_films.json()
f13_fan_films.json()["data"]["discoverables"]

pd.json_normalize(f13_fan_films.json()["data"]["discoverables"])