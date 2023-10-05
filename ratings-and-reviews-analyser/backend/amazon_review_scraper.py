import requests
import re
from backend.product_id_grabber import get_amazon_product_id


def get_amazon_reviews(link, pages=1):
    product_id = get_amazon_product_id(link)

    base_url = "https://www.amazon.co.uk/hz/reviews-render/ajax/reviews/get/ref=cm_cr_getr_d_paging_btm_next_3"

    # headers
    headers = {
        "authority": "www.amazon.co.uk",
        "accept": "text/html,*/*",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8",
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
        "device-memory": "8",
        "downlink": "10",
        "dpr": "1",
        "ect": "4g",
        "origin": "https://www.amazon.co.uk",
        "referer": f"https://www.amazon.co.uk/Oust-Odour-Eliminator-Outdoor-Scent/product-reviews/B000MV4C1U/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&pageNumber=1&sortBy=recent",
        "rtt": "50",
        "sec-ch-device-memory": "8",
        "sec-ch-dpr": "1",
        "sec-ch-ua": '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua-platform-version": '"14.0.0"',
        "sec-ch-viewport-width": "1061",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81",
        "viewport-width": "1061",
        "x-requested-with": "XMLHttpRequest",
    }

    # list to store all reviews
    all_reviews = []

    # iterate through the specified number of pages
    for page_number in range(1, pages + 1):
        # set the 'pageNumber' parameter to the current page number
        data = {
            "sortBy": "recent",
            "reviewerType": "all_reviews",
            "formatType": "",
            "mediaType": "",
            "filterByStar": "",
            "filterByAge": "",
            "pageNumber": str(page_number),  # Update the page number for each iteration
            "filterByLanguage": "",
            "filterByKeyword": "",
            "shouldAppend": "undefined",
            "deviceType": "desktop",
            "canShowIntHeader": "undefined",
            "reftag": f"cm_cr_getr_d_paging_btm_next_{page_number}",
            "pageSize": "10",
            "asin": str(product_id),
            "scope": "reviewsAjax3",
        }

        # send a POST request
        response = requests.post(base_url, data=data, headers=headers)

        # data mining
        raw_data = response.text
        pattern = r"<span[^>]*>([^<]+)</span>"
        matches = re.findall(pattern, raw_data)

        # add reviews to dict
        reviews = []
        keys = [
            "name",
            "rating",
            "title",
            "date",
            "verified",
            "review text",
            "dummy(ignore)",
        ]

        for i in range(0, len(matches), len(keys)):
            if i + len(keys) <= len(matches):
                review_data = {
                    keys[j]: matches[i + j].strip() for j in range(len(keys) - 1)
                }
                reviews.append(review_data)

        # add the reviews from this page to the list of all reviews
        all_reviews.extend(reviews)

    # create reviews dict
    reviews_dict = {"reviews": all_reviews}
    return reviews_dict


if __name__ == "__main__":
    reviews = get_amazon_reviews(link=input("amazon product link: "), pages=1)
    print(reviews)
