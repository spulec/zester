from zester import SingleClient, Attribute


class WeatherClient(SingleClient):
    url = "http://forecast.weather.gov/MapClick.php?lat={lat}&lon={lng}"
    temperature = Attribute(selector="$('.myforecast-current-lrg').html()")
    humidity = Attribute(
        selector="$('.current-conditions-detail li').contents()[1]")
    heat_index = Attribute(
        selector="$('.current-conditions-detail li').contents()[11]")

    def __init__(self, lat, lng, *args, **kwargs):
        super(WeatherClient, self).__init__(*args, **kwargs)
        self.url = self.url.format(lat=lat, lng=lng)
