from typing import List

from fastapi.encoders import jsonable_encoder
from src.modules.analysis.models.schemas import FlightInfo, FlightPreparedData
from src.shared.utils.date import get_date_difference, get_date_month


async def prepare_data(data: List[FlightInfo]) -> List[FlightPreparedData]:
    # TODO Apply the necessary business logic so that the data can be analysed better
    flights = data
    transformed_flights: List[FlightPreparedData] = []
    for flight in flights:
        transformed_flight = FlightPreparedData(
            supplier=flight.supplier,
            departureStation=flight.departureStation,
            arrivalStation=flight.arrivalStation,
            issueDate=flight.issueDate,
            departureDate=flight.departureDate,
            arrivalDate=flight.arrivalDate,
            requestDate=flight.requestDate,
            daysInAdvance=await get_date_difference(
                flight.requestDate,
                flight.departureDate,
            ),
            daysToIssue=await get_date_difference(
                flight.requestDate,
                flight.issueDate,
            ),
            requestMonth=await get_date_month(flight.requestDate),
            issueMonth=await get_date_month(flight.issueDate),
            flightDuration=flight.flightDuration,
            journeys=flight.journeys,
            timeToApprove=flight.timeToApprove,
            totalAmount=flight.totalAmount,
            lowestPrice=flight.lowestPrice,
            highestPrice=flight.highestPrice,
            isInternational=flight.isInternational,
            policy1=flight.policy1,
            policy2=flight.policy2,
            policy3=flight.policy3,
        )
        transformed_flights.append(transformed_flight)

    return transformed_flights
