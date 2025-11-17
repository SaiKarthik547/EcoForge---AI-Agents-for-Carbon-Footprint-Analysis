import asyncio
from typing import Dict, Any, List
import json
import requests
from geopy.geocoders import Nominatim

class SupervisorAgent:
    """CAPSTONE: Master Supervisor Agent with Location Intelligence"""
    
    def __init__(self):
        self.geolocator = Nominatim(user_agent="ecoforge_supervisor")
        self.agent_roster = [
            "home_expert",
            "transport_expert", 
            "diet_expert",
            "shopping_expert"
        ]
    
    async def analyze_and_coordinate(self, user_input: str) -> Dict[str, Any]:
        """CAPSTONE: Combined analysis and coordination method"""
        # First analyze the input
        analysis_result = await self.analyze_input(user_input)
        
        # Then coordinate agents based on the analysis
        coordination_result = await self.coordinate_agents(
            analysis_result["coordination_plan"], 
            user_input
        )
        
        # Combine results
        return {
            "analysis": analysis_result,
            "coordination": coordination_result
        }
    
    async def analyze_input(self, user_input: str) -> Dict[str, Any]:
        """CAPSTONE: Input Analysis and Agent Coordination"""
        
        # Extract location information
        location_data = await self._extract_location(user_input)
        
        # Analyze lifestyle patterns
        lifestyle_analysis = self._analyze_lifestyle_patterns(user_input)
        
        # Determine agent priorities
        agent_priorities = self._determine_agent_priorities(lifestyle_analysis)
        
        return {
            "location": location_data,
            "lifestyle_patterns": lifestyle_analysis,
            "agent_priorities": agent_priorities,
            "coordination_plan": self._create_coordination_plan(agent_priorities)
        }
    
    async def _extract_location(self, user_input: str) -> Dict[str, Any]:
        """Extract and geocode location from user input"""
        
        # Simple location extraction (in production, use NLP)
        location_keywords = [
            "Tokyo", "New York", "London", "Paris", "Berlin", "Sydney",
            "San Francisco", "Los Angeles", "Chicago", "Boston", "Seattle"
        ]
        
        detected_location = None
        for keyword in location_keywords:
            if keyword.lower() in user_input.lower():
                detected_location = keyword
                break
        
        if detected_location:
            try:
                # Use run_in_executor for synchronous geocode call
                loop = asyncio.get_event_loop()
                location = await loop.run_in_executor(None, self.geolocator.geocode, detected_location)
                if location:
                    # Handle typing issue with linter
                    lat = getattr(location, 'latitude', None)
                    lon = getattr(location, 'longitude', None)
                    address = getattr(location, 'address', None)
                    if lat is not None and lon is not None:
                        return {
                            "city": detected_location,
                            "lat": lat,
                            "lon": lon,
                            "country": address.split(", ")[-1] if address else "Unknown"
                        }
            except:
                pass
        
        # Default to Tokyo for demo
        return {
            "city": "Tokyo",
            "lat": 35.6762,
            "lon": 139.6503,
            "country": "Japan"
        }
    
    def _analyze_lifestyle_patterns(self, user_input: str) -> Dict[str, Any]:
        """Analyze lifestyle patterns from user description"""
        
        patterns = {
            "transport_intensity": "low",
            "diet_type": "mixed",
            "home_energy": "medium",
            "shopping_frequency": "medium",
            "luxury_level": "low"
        }
        
        # Transport analysis
        transport_keywords = {
            "high": ["private jet", "helicopter", "luxury car", "v8", "v12", "sports car"],
            "medium": ["car", "drive", "suv", "truck", "motorcycle"],
            "low": ["bike", "walk", "public transport", "train", "bus"]
        }
        
        for level, keywords in transport_keywords.items():
            if any(keyword in user_input.lower() for keyword in keywords):
                patterns["transport_intensity"] = level
                break
        
        # Diet analysis
        diet_keywords = {
            "meat_heavy": ["wagyu", "steak", "beef", "meat daily", "carnivore"],
            "mixed": ["chicken", "fish", "meat", "omnivore"],
            "plant_based": ["vegan", "vegetarian", "plant-based", "salad"]
        }
        
        for diet_type, keywords in diet_keywords.items():
            if any(keyword in user_input.lower() for keyword in keywords):
                patterns["diet_type"] = diet_type
                break
        
        # Luxury level analysis
        luxury_keywords = ["luxury", "expensive", "premium", "high-end", "private", "exclusive"]
        if any(keyword in user_input.lower() for keyword in luxury_keywords):
            patterns["luxury_level"] = "high"
        
        return patterns
    
    def _determine_agent_priorities(self, lifestyle_analysis: Dict[str, Any]) -> Dict[str, float]:
        """Determine which agents should focus more based on lifestyle"""
        
        priorities = {
            "home_expert": 0.25,
            "transport_expert": 0.25,
            "diet_expert": 0.25,
            "shopping_expert": 0.25
        }
        
        # Adjust priorities based on lifestyle patterns
        if lifestyle_analysis["transport_intensity"] == "high":
            priorities["transport_expert"] = 0.4
            priorities["home_expert"] = 0.2
            priorities["diet_expert"] = 0.2
            priorities["shopping_expert"] = 0.2
        
        if lifestyle_analysis["diet_type"] == "meat_heavy":
            priorities["diet_expert"] = 0.4
            priorities["transport_expert"] = 0.2
            priorities["home_expert"] = 0.2
            priorities["shopping_expert"] = 0.2
        
        if lifestyle_analysis["luxury_level"] == "high":
            priorities["shopping_expert"] = 0.35
            priorities["transport_expert"] = 0.35
            priorities["diet_expert"] = 0.15
            priorities["home_expert"] = 0.15
        
        return priorities
    
    def _create_coordination_plan(self, agent_priorities: Dict[str, float]) -> Dict[str, Any]:
        """Create coordination plan for agent execution"""
        
        # Sort agents by priority
        sorted_agents = sorted(agent_priorities.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "execution_order": [agent[0] for agent in sorted_agents],
            "parallel_groups": [
                ["home_expert", "transport_expert"],
                ["diet_expert", "shopping_expert"]
            ],
            "communication_matrix": {
                "home_expert": ["transport_expert"],
                "transport_expert": ["home_expert", "shopping_expert"],
                "diet_expert": ["shopping_expert"],
                "shopping_expert": ["diet_expert", "transport_expert"]
            },
            "priority_weights": agent_priorities
        }
    
    async def coordinate_agents(self, coordination_plan: Dict[str, Any], user_input: str) -> Dict[str, Any]:
        """CAPSTONE: Agent Coordination and Communication Management"""
        
        coordination_results = {
            "coordination_success": True,
            "agent_assignments": {},
            "communication_log": [],
            "execution_timeline": []
        }
        
        # Assign tasks to agents based on priorities
        for agent_name in coordination_plan["execution_order"]:
            priority = coordination_plan["priority_weights"][agent_name]
            
            coordination_results["agent_assignments"][agent_name] = {
                "priority_level": priority,
                "focus_areas": self._get_agent_focus_areas(agent_name, priority),
                "expected_duration": self._estimate_execution_time(agent_name, priority)
            }
        
        # Set up communication channels
        for sender, receivers in coordination_plan["communication_matrix"].items():
            for receiver in receivers:
                coordination_results["communication_log"].append({
                    "sender": sender,
                    "receiver": receiver,
                    "channel_status": "active",
                    "message_queue": []
                })
        
        return coordination_results
    
    def _get_agent_focus_areas(self, agent_name: str, priority: float) -> List[str]:
        """Define focus areas for each agent based on priority"""
        
        focus_areas = {
            "home_expert": ["energy_efficiency", "heating_cooling", "appliances", "insulation"],
            "transport_expert": ["vehicle_type", "fuel_efficiency", "travel_patterns", "alternatives"],
            "diet_expert": ["food_sources", "meal_frequency", "dietary_preferences", "waste"],
            "shopping_expert": ["purchase_patterns", "product_lifecycle", "packaging", "sustainability"]
        }
        
        base_areas = focus_areas.get(agent_name, [])
        
        # High priority agents get additional focus areas
        if priority > 0.3:
            additional_areas = {
                "home_expert": ["renewable_energy", "smart_systems"],
                "transport_expert": ["carbon_offsetting", "route_optimization"],
                "diet_expert": ["local_sourcing", "seasonal_eating"],
                "shopping_expert": ["circular_economy", "ethical_sourcing"]
            }
            base_areas.extend(additional_areas.get(agent_name, []))
        
        return base_areas
    
    def _estimate_execution_time(self, agent_name: str, priority: float) -> float:
        """Estimate execution time based on agent and priority"""
        
        base_times = {
            "home_expert": 2.5,
            "transport_expert": 3.0,
            "diet_expert": 2.0,
            "shopping_expert": 1.5
        }
        
        base_time = base_times.get(agent_name, 2.0)
        
        # Higher priority agents get more processing time
        priority_multiplier = 1 + (priority - 0.25) * 2
        
        return base_time * priority_multiplier