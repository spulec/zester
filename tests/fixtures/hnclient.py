from zester import MultipleClient, Attribute


class HNClient(MultipleClient):
    url = "http://news.ycombinator.com/"
    title = Attribute(selector="$('.title a')", modifier="$(el).html()")
    link = Attribute(selector="$('.title a')", modifier="$(el).attr('href')")
    points = Attribute(selector="$('.subtext span')",
                            modifier="$(el).html().replace(' points', '')")
