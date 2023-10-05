import re


def get_amazon_product_id(url):
    """
    Get product ID from the Amazon URL
    >>> url = "https://www.amazon.co.uk/Notebook-Refillable-Travelers-Professionals-Organizer/dp/B01N24BYQ7/ref=sr_1_1_sspa?crid"
    >>> get_amazon_product_id(url)
    'B01N24BYQ7'
    >>> url = "https://www.amazon.co.uk/gp/product/B0B9H5DWW9/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1"
    >>> get_amazon_product_id(url)
    'B0B9H5DWW9'
    """
    url = str(url)
    regex = r"/([A-Z0-9]{10})/"
    product_id_match = re.search(regex, url)

    if product_id_match:
        return product_id_match.group(1)
    else:
        return None


if __name__ == "__main__":
    import doctest

    doctest.testmod()
