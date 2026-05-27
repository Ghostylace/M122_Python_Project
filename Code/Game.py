class Game:
    
    def __init__(self, id, slug, title, type, mature, isFree, price, cut, url, expiry):
        self.id = id
        self.slug = slug
        self.title = title
        self.type = type
        self.mature = mature
        self.isFree = isFree
        self.price = price
        self.cut = cut
        self.url = url
        self.expiry = expiry