from dataclasses import dataclass


@dataclass 
class Point:
    lat: float
    lng: float

@dataclass
class City:
    name: str
    location: Point