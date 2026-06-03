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

    def __eq__(self, other):
        return isinstance(other, Game) and self.id == other.id

    def __hash__(self):
        return hash(self.id)
