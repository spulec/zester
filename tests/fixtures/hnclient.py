from zester import Client, Attribute


class HNClient(Client):
    title = Attribute(selector="$('.title a')", modifier="$(el).html()")
    link = Attribute(selector="$('.title a')", modifier="$(el).attr('href')")
    points = Attribute(selector="$('.subtext span')",
                            modifier="$(el).html().replace(' points', '')")

    def __init__(self, url="http://news.ycombinator.com/"):
        self.url = url
        super(HNClient, self).__init__()
