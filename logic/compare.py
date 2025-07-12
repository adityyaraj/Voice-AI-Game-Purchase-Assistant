from urllib.parse import urlparse

def choose_best(options):
    def get_price(option):
        if option is None or not isinstance(option, dict):
            return float('inf')

        price = option.get('price')
        if price is None:
            return float('inf')

        if isinstance(price, str):
            price = price.lower()
            if price in ['free', 'n/a', 'unavailable', '']:
                return 0.0
            price = price.replace('$', '').replace('€', '').replace('£', '').replace(',', '').strip()

        try:
            return float(price)
        except (ValueError, TypeError):
            return float('inf')

    def get_site_name(source):
        if not source:
            return "Unknown"
        domain = urlparse(source).netloc
        if "steam" in domain:
            return "Steam"
        elif "gog" in domain:
            return "GOG"
        elif "epicgames" in domain or "epic" in domain:
            return "Epic Games"
        else:
            return "Unknown"

    valid_options = [opt for opt in options if opt is not None]
    if not valid_options:
        return None

    best = min(valid_options, key=get_price)

    best["site_name"] = get_site_name(best.get("source", ""))

    return best
