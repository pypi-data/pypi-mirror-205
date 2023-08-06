import polyline

class CoolmapRoutePath:
    
    def __init__(self, response):
        self.__response = response
    
    
    def estimated_time(self, required_unit="M"):
        required_unit =  required_unit.upper()
        unit = {"M":[0.0166667, "Minutes"], "H":[0.000277778,"Hours"], "S":[1,"Seconds"]}
        return f"{str(round((self.__response['routes'][0]['duration'] * unit.get(required_unit)[0]), 2))} {unit.get(required_unit)[1]}"


    def estimated_distance(self, required_unit="M"):
        required_unit = required_unit.upper()
        unit = {"M":[0.000621371, "Miles"], "K":[0.001,"Kilometer"], "T":[1, "Meter"]}
        return f"{str(round(self.__response['routes'][0]['distance'] * unit.get(required_unit)[0], 2))} {unit.get(required_unit)[1]}"
    
    
    def get_path(self):
        return ";".join([f'{l[0]},{l[1]}' for l in polyline.decode(self.__response['routes'][0]['geometry'])])