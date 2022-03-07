from sql_alchemy import banco

class SiteModel(banco.Model):
    __tablename__ = 'site_tb'
    site_id = banco.Column(banco.Integer, primary_key=True)
    url = banco.Column(banco.String(80))
    nome = banco.Column(banco.String(80))
    hoteis = banco.relationship('HotelModel')

    def __init__(self, url) :
        self.url = url


    def json(self):
        return {
        'site_id': self.site_id,
        'url': self.url,
        'hoteis':[hotel.json() for hotel in self.hoteis]
        }

    @classmethod
    def find_site(cls, url):
        site = cls.query.filter_by(url=url).first()
        #.first #Select * from hoteis where Site_id = Site_id passado limit one
        if site:
            return site
        return None

    def save_site(self):
        banco.session.add(self)
        banco.session.commit()

    def update_site(self, url, nome):
        self.url = url

    def delete_site(self, url):
        banco.session.delete(self)
        banco.session.commit()
