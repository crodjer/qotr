from .base import Base

# pylint: disable=W0223, W0221
class Home(Base):

    def get(self, _=None):
        self.render('../../dist/index.html')
