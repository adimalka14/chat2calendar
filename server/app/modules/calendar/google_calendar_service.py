"""
Google Calendar service for handling Google Calendar API integration.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import httpx
from app.config import settings
from datetime import timezone


def _rfc3339(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


class GoogleCalendarService:
    """Service for handling Google Calendar API integration."""
    
    def __init__(self):
        self.base_url = "https://www.googleapis.com/calendar/v3"
        self.scopes = settings.google_calendar_scopes
    
    async def get_calendars(self, access_token: str) -> List[Dict[str, Any]]:
        """
        Get user's calendars from Google Calendar API.
        
        Args:
            access_token: Google access token
            
        Returns:
            List[Dict[str, Any]]: List of calendars
        """
        url = f"{self.base_url}/users/me/calendarList"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()
                return data.get("items", [])
            except httpx.HTTPError:
                return []
    
    async def get_events(
        self,
        access_token: str,
        calendar_id: str = "primary",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        max_results: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get events from Google Calendar API.
        
        Args:
            access_token: Google access token
            calendar_id: Calendar ID (default: primary)
            start_date: Optional start date filter
            end_date: Optional end date filter
            max_results: Maximum number of events to return
            
        Returns:
            List[Dict[str, Any]]: List of events
        """
        url = f"{self.base_url}/calendars/{calendar_id}/events"
        headers = {"Authorization": f"Bearer {access_token}"}

        params = {"maxResults": max_results}
        if start_date:
            params["timeMin"] = _rfc3339(start_date)
        if end_date:
            params["timeMax"] = _rfc3339(end_date)
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers, params=params)

                response.raise_for_status()
                data = response.json()
                return data.get("items", [])
            except httpx.HTTPError:
                return []
    
    async def create_event(
        self,
        access_token: str,
        calendar_id: str,
        event_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Create an event in Google Calendar.
        
        Args:
            access_token: Google access token
            calendar_id: Calendar ID
            event_data: Event data
            
        Returns:
            Optional[Dict[str, Any]]: Created event if successful, None otherwise
        """
        url = f"{self.base_url}/calendars/{calendar_id}/events"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, headers=headers, json=event_data)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError:
                return None
    
    async def get_event(
        self,
        access_token: str,
        calendar_id: str,
        event_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get a specific event from Google Calendar.
        
        Args:
            access_token: Google access token
            calendar_id: Calendar ID
            event_id: Event ID
            
        Returns:
            Optional[Dict[str, Any]]: Event if found, None otherwise
        """
        url = f"{self.base_url}/calendars/{calendar_id}/events/{event_id}"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError:
                return None
    
    async def update_event(
        self,
        access_token: str,
        calendar_id: str,
        event_id: str,
        event_data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Update an event in Google Calendar.
        
        Args:
            access_token: Google access token
            calendar_id: Calendar ID
            event_id: Event ID
            event_data: Updated event data
            
        Returns:
            Optional[Dict[str, Any]]: Updated event if successful, None otherwise
        """
        url = f"{self.base_url}/calendars/{calendar_id}/events/{event_id}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.put(url, headers=headers, json=event_data)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError:
                return None
    
    async def delete_event(
        self,
        access_token: str,
        calendar_id: str,
        event_id: str
    ) -> bool:
        """
        Delete an event from Google Calendar.
        
        Args:
            access_token: Google access token
            calendar_id: Calendar ID
            event_id: Event ID
            
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        url = f"{self.base_url}/calendars/{calendar_id}/events/{event_id}"
        headers = {"Authorization": f"Bearer {access_token}"}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.delete(url, headers=headers)
                print(response)
                response.raise_for_status()
                return True
            except httpx.HTTPError:
                return False
