# pypi-packages
Python util functions

`pip3 install aggdirect-route-estimation-calculator` to install packages


## What is it

Support for coolmap path,estimated_time and estimated distance.
This module provides the path co-ordinate, estimated distance and estimated
time to cover the distance based on there pick-up and delivery latitude and longitude.


    CoolmapRoutePath(<mapbox_api_response>)






## Usage/Examples

```python
from aggdirect_route_estimation_calculator import CoolmapRoutePath

cool_obj = CoolmapRoutePath(<map_box_reponse>)

```
## Method to get the estimated time

```python
cool_obj.estimated_time(required_unit='m')
```
     
        "m" - Return the estimated time in Minuted
        "h" - Return the estimated time in Hour
        "s" - Reeturn the estimated time in Second


Example:
    
    Input:

    >>cool_obj.estimated_time('s')

    Output:

    >>'6656.05 Second'


## Method to get the estimated distance

```python
cool_obj.estimated_distance(required_unit='m')
```
     
        "m" - REturn the distance time in Miles
        "k" - Return the distance time in Kilometer
        "t" - Reeturn the distance time in Meter


Example:
    
    Input:

    >>cool_obj.estimated_distance('t')

    Output:

    >>'144062.0 Meter'


## Method to get the path

```python
cool_obj.get_path()
```


Example:
    
    Input:

    >>cool_obj.get_path()

    Output:

    >>'38.242287,-76.56314400000001;38.242289,-76.563149;...'
