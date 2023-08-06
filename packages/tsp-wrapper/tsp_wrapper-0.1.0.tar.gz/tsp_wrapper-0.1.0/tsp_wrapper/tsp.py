import math

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

from tsp_wrapper.config.settings import OUTBOUND_ROUTING_KEY, OUTBOUND_EXCHANGE_NAME
from tsp_wrapper.middleware.schema import City, Point
import logging


logger = logging.getLogger("root")


def create_data_model(locations: list):
    """Stores the data for the problem."""
    data = {}
    # Locations in block units
    data['locations'] = locations

    data['num_vehicles'] = 1
    data['depot'] = 0
    return data


def compute_euclidean_distance_matrix(locations:list[City]):
    """Creates callback to return distance between points."""
    distances = {}
    for src in locations:
        distances[src.name] = {}
        for dest in locations:
            if src.name == dest.name:
                distances[src.name][dest.name] = 0
            else:
                # Euclidean distance
                distances[src.name][dest.name] = (int(
                    math.hypot((src.location.lat - dest.location.lat),
                               (src.location.lng - dest.location.lng))))
    return distances


def print_solution(manager, routing, solution, data):
    """Prints solution on console."""
    print('Objective: {}'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(data[manager.IndexToNode(index)].name)
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    plan_output += ' {}\n'.format(data[manager.IndexToNode(index)].name)
    print(plan_output)
    plan_output += 'Objective: {}m\n'.format(route_distance)

def return_solution(manager, routing, solution, data):
    """Prints solution on console."""
    result = list()
    index = routing.Start(0)
    route_distance = 0
    while not routing.IsEnd(index):
        result.append(
            data[manager.IndexToNode(index)].name
        )
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        route_distance += routing.GetArcCostForVehicle(previous_index, index, 0)
    return result

def run(locations: list):
    """Entry point of the program."""
    # Instantiate the data problem.
    data = create_data_model(locations)

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['locations']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)

    distance_matrix = compute_euclidean_distance_matrix(data['locations'])

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        # print_solution(manager, routing, solution, locations)
        return return_solution(manager, routing, solution, locations)


def run_tsp(data: list[dict], producer):
    cities = list()
    for city in data:
        cities.append(
            City(
                name=city.get("name"),
                location=Point(lat=city.get("lat"), lng=city.get("lng"))
            )
        )
    body = run(cities)
    logger.info(body)

    producer_data = { "body": body, "exchange_name": OUTBOUND_EXCHANGE_NAME, "routing_key": OUTBOUND_ROUTING_KEY}
    producer._data = producer_data
    producer.run()