"""
Developer: Nikhil Nageshwar Inturi (inturinikhilnageshwar@gmail.com) GitHub: @unikill066
Date: 2025-07-14

PlaceExplorerTool is a tool that provides place exploration for a given city/place based on attractions, restaurants, activities, etc.
"""

# imports
from dotenv import load_dotenv
load_dotenv()
import os, sys
sys.path.append("../../")
from tralogger import get_logger
logger = get_logger(__name__)
from typing import List

from langchain.tools import tool
from src.utils.places import GooglePlaces, TavilyPlaces

__all__ = [
    "PlaceExplorerTool",
]

class PlaceExplorerTool:
    """
    PlaceExplorerTool is a tool that provides place exploration for a given city/place based on attractions, restaurants, activities, etc.
    """
    logger.info("PlaceExplorerTool initialized")
    def __init__(self):
        """
        --- Initializes the PlaceExplorerTool ---

         - Initializes the GooglePlaces and TavilyPlaces objects.
         - Initializes the place search tool list.
        """
        self.google_search_places = GooglePlaces()
        self.tavily_search_places = TavilyPlaces()
        self.place_search_tool_list = self._setup_tools()
        
    def _setup_tools(self) -> List[tool]:
        """
        --- Initializes the place search tools ---

        Initializes the place search tools.

        Returns
        -------
            List[tool]
                The place search tools.
        """
        @tool
        def fetch_attractions(city: str) -> dict:
            """
            Fetches the top attractive places in and around the given city.
            city : str
                The city to fetch the top attractive places for.

            Returns
            -------
                dict
                    The top attractive places in and around the given city.
            """
            try:
                attractions = self.google_search_places.fetch_places(city)
                if attractions:
                    logger.info(f"Google search attractions for {city}: {attractions}")
                    return f"Following are the attractions of {city} based on Google search: {attractions}"
            
            except Exception as e:
                attractions = self.tavily_search_places.fetch_places(city)
                if attractions:
                    logger.info(f"Tavily search attractions for {city}: {attractions}")
                    return f"Google search failed to fetch attractions with exception {e}. Following are the attractions of {city} based on Tavily search: {attractions}"
            
            finally:
                logger.info("PlaceExplorerTool.fetch_attractions() finished")

        @tool
        def search_restaurants(city: str) -> dict:
            """
            Fetches the top 10 restaurants and eateries in and around the given city.
            city : str
                The city to fetch the top 10 restaurants and eateries for.

            Returns
            -------
                dict
                    The top 10 restaurants and eateries in and around the given city.
            """
            try:
                restaurants = self.google_search_places.fetch_restaurants(city)
                if restaurants:
                    logger.info(f"Google search restaurants for {city}: {restaurants}")
                    return f"Following are the restaurants of {city} based on Google search: {restaurants}"
            except Exception as e:
                restaurants = self.tavily_search_places.fetch_restaurants(city)
                if restaurants:
                    logger.info(f"Tavily search restaurants for {city}: {restaurants}")
                    return f"Google search failed to fetch restaurants with exception {e}. Following are the restaurants of {city} based on Tavily search: {restaurants}"
            finally:
                logger.info("PlaceExplorerTool.search_restaurants() finished")

        @tool
        def search_activities(city: str) -> dict:
            """
            Fetches the different modes of transportations available in the given city.
            city : str
                The city to fetch the different modes of transportations for.

            Returns
            -------
                dict
                    The different modes of transportations available in the given city.
            """
            try:
                activities = self.google_search_places.fetch_activity(city)
                if activities:
                    logger.info(f"Google search activities for {city}: {activities}")
                    return f"Following are the activities of {city} based on Google search: {activities}"
            except Exception as e:
                activities = self.tavily_search_places.fetch_activity(city)
                if activities:
                    logger.info(f"Tavily search activities for {city}: {activities}")
                    return f"Google search failed to fetch activities with exception {e}. Following are the activities of {city} based on Tavily search: {activities}"
            finally:
                logger.info("PlaceExplorerTool.search_activities() finished")
                
        @tool
        def search_transport(city: str) -> dict:
            """
            Fetches the different modes of transportations available in the given city.
            city : str
                The city to fetch the different modes of transportations for.

            Returns
            -------
                dict
                    The different modes of transportations available in the given city.
            """
            try:
                transport = self.google_search_places.fetch_transport(city)
                if transport:
                    logger.info(f"Google search transport for {city}: {transport}")
                    return f"Following are the transport options of {city} based on Google search: {transport}"
            except Exception as e:
                transport = self.tavily_search_places.fetch_transport(city)
                if transport:
                    logger.info(f"Tavily search transport for {city}: {transport}")
                    return f"Google search failed to fetch transport with exception {e}. Following are the transport options of {city} based on Tavily search: {transport}"
            finally:
                logger.info("PlaceExplorerTool.search_transport() finished")
                
        logger.info("PlaceExplorerTool._setup_tools() finished")
        return [fetch_attractions, search_restaurants, search_activities, search_transport]