const weatherMap = {
    1000: { description: "Clear", icon: "/static/weather-code-symbols/clear_day.svg" },
    1100: { description: "Mostly Clear", icon: "/static/weather-code-symbols/mostly_clear_day.svg" },
    1101: { description: "Partly Cloudy", icon: "/static/weather-code-symbols/partly_cloudy_day.svg" },
    1102: { description: "Mostly Cloudy", icon: "/static/weather-code-symbols/mostly_cloudy.svg" },
    1001: { description: "Cloudy", icon: "/static/weather-code-symbols/cloudy.svg" },
    2000: { description: "Fog", icon: "/static/weather-code-symbols/fog.svg" },
    2100: { description: "Light Fog", icon: "/static/weather-code-symbols/fog_light.svg" },
    4000: { description: "Drizzle", icon: "/static/weather-code-symbols/drizzle.svg" },
    4001: { description: "Rain", icon: "/static/weather-code-symbols/rain.svg" },
    4200: { description: "Light Rain", icon: "/static/weather-code-symbols/rain_light.svg" },
    4201: { description: "Heavy Rain", icon: "/static/weather-code-symbols/rain_heavy.svg" },
    5000: { description: "Snow", icon: "/static/weather-code-symbols/snow.svg" },
    5001: { description: "Flurries", icon: "/static/weather-code-symbols/flurries.svg" },
    5100: { description: "Light Snow", icon: "/static/weather-code-symbols/snow_light.svg" },
    5101: { description: "Heavy Snow", icon: "/static/weather-code-symbols/snow_heavy.svg" },
    6000: { description: "Freezing Drizzle", icon: "/static/weather-code-symbols/freezing_drizzle.svg" },
    6001: { description: "Freezing Rain", icon: "/static/weather-code-symbols/freezing_rain.svg" },
    6200: { description: "Light Freezing Rain", icon: "/static/weather-code-symbols/freezing_rain_light.svg" },
    6201: { description: "Heavy Freezing Rain", icon: "/static/weather-code-symbols/freezing_rain_heavy.svg" },
    7000: { description: "Ice Pellets", icon: "/static/weather-code-symbols/ice_pellets.svg" },
    7101: { description: "Heavy Ice Pellets", icon: "/static/weather-code-symbols/ice_pellets_heavy.svg" },
    7102: { description: "Light Ice Pellets", icon: "/static/weather-code-symbols/ice_pellets_light.svg" },
    8000: { description: "Thunderstorm", icon: "/static/weather-code-symbols/tstorm.svg" }
};

export default weatherMap;