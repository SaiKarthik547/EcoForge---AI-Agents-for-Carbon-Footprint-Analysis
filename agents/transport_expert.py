import asyncio
import requests
from typing import Dict, Any, List
import json
import re

class TransportExpertAgent:
    """CAPSTONE: Transportation Carbon Expert with Real-time Analysis"""
    
    def __init__(self):
        self.agent_id = "transport_racer_002"
        self.specializations = [
            "vehicle_emissions",
            "alternative_transport",
            "route_optimization",
            "carbon_offsetting"
        ]
        self.emission_factors = {
            # kg CO2 per km
            "private_jet": 2.5,
            "helicopter": 1.8,
            "luxury_car": 0.35,
            "suv": 0.25,
            "sedan": 0.18,
            "hybrid": 0.12,
            "electric": 0.05,
            "motorcycle": 0.15,
            "bus": 0.08,
            "train": 0.04,
            "bike": 0.0,
            "walk": 0.0
        }
    
    async def analyze(self, user_input: str, location: Dict[str, Any]) -> Dict[str, Any]:
        """CAPSTONE: Comprehensive Transportation Analysis"""
        
        # Extract transportation patterns
        transport_patterns = self._analyze_transport_patterns(user_input)
        
        # Get local transport options
        local_options = await self._get_local_transport_options(location)
        
        # Calculate carbon footprint
        carbon_footprint = self._calculate_transport_carbon_footprint(transport_patterns)
        
        # Generate route optimizations
        route_optimizations = self._generate_route_optimizations(transport_patterns, local_options)
        
        # Create alternative transport recommendations
        alternatives = self._recommend_alternatives(transport_patterns, local_options)
        
        return {
            "agent_id": self.agent_id,
            "carbon_footprint": carbon_footprint,
            "transport_patterns": transport_patterns,
            "local_options": local_options,
            "route_optimizations": route_optimizations,
            "alternatives": alternatives,
            "efficiency_score": self._calculate_transport_efficiency(transport_patterns),
            "key_findings": self._extract_key_findings(transport_patterns, carbon_footprint)
        }
    
    def _analyze_transport_patterns(self, user_input: str) -> Dict[str, Any]:
        """Extract transportation patterns from user description"""
        
        patterns = {
            "primary_vehicle": "sedan",
            "daily_distance": 30,  # km
            "weekly_flights": 0,
            "flight_distance": 0,  # km per flight
            "public_transport_usage": "low",
            "walking_biking": "low",
            "luxury_transport": False
        }
        
        # Vehicle type detection
        vehicle_keywords = {
            "private_jet": ["private jet", "jet", "private plane"],
            "helicopter": ["helicopter", "chopper"],
            "luxury_car": ["luxury car", "ferrari", "lamborghini", "porsche", "bentley", "rolls royce"],
            "suv": ["suv", "v8", "v12", "truck", "pickup"],
            "hybrid": ["hybrid", "prius", "camry hybrid"],
            "electric": ["tesla", "electric car", "ev", "electric vehicle"],
            "motorcycle": ["motorcycle", "bike", "motorbike"],
            "sedan": ["car", "sedan", "drive"]
        }
        
        for vehicle_type, keywords in vehicle_keywords.items():
            if any(keyword in user_input.lower() for keyword in keywords):
                patterns["primary_vehicle"] = vehicle_type
                break
        
        # Flight pattern detection
        flight_keywords = ["fly", "flight", "airplane", "plane", "travel"]
        if any(keyword in user_input.lower() for keyword in flight_keywords):
            if "daily" in user_input.lower():
                patterns["weekly_flights"] = 7
                patterns["flight_distance"] = 1000
            elif "weekly" in user_input.lower():
                patterns["weekly_flights"] = 1
                patterns["flight_distance"] = 2000
            elif "private jet" in user_input.lower():
                patterns["weekly_flights"] = 2
                patterns["flight_distance"] = 3000
        
        # Distance estimation
        distance_patterns = re.findall(r'(\d+)\s*(km|mile|miles)', user_input.lower())
        if distance_patterns:
            distance, unit = distance_patterns[0]
            distance = int(distance)
            if unit in ["mile", "miles"]:
                distance *= 1.6  # Convert to km
            patterns["daily_distance"] = distance
        
        # Luxury transport detection
        luxury_keywords = ["luxury", "private", "exclusive", "premium", "first class"]
        patterns["luxury_transport"] = any(keyword in user_input.lower() for keyword in luxury_keywords)
        
        return patterns
    
    async def _get_local_transport_options(self, location: Dict[str, Any]) -> Dict[str, Any]:
        """Get local transportation options and infrastructure"""
        
        # Mock data based on city (in production, use real APIs)
        city = location.get("city", "Tokyo")
        
        transport_infrastructure = {
            "Tokyo": {
                "public_transport_quality": "excellent",
                "bike_infrastructure": "good",
                "ev_charging_stations": 5000,
                "car_sharing": True,
                "ride_sharing": True
            },
            "New York": {
                "public_transport_quality": "good",
                "bike_infrastructure": "excellent",
                "ev_charging_stations": 3000,
                "car_sharing": True,
                "ride_sharing": True
            },
            "London": {
                "public_transport_quality": "excellent",
                "bike_infrastructure": "good",
                "ev_charging_stations": 4000,
                "car_sharing": True,
                "ride_sharing": True
            }
        }
        
        return transport_infrastructure.get(city, {
            "public_transport_quality": "average",
            "bike_infrastructure": "average",
            "ev_charging_stations": 1000,
            "car_sharing": False,
            "ride_sharing": True
        })
    
    def _calculate_transport_carbon_footprint(self, transport_patterns: Dict[str, Any]) -> float:
        """Calculate transportation carbon footprint in tons CO2/year"""
        
        # Daily vehicle emissions
        primary_vehicle = transport_patterns["primary_vehicle"]
        daily_distance = transport_patterns["daily_distance"]
        emission_factor = self.emission_factors.get(primary_vehicle, 0.18)
        
        daily_emissions = daily_distance * emission_factor  # kg CO2/day
        annual_vehicle_emissions = daily_emissions * 365 / 1000  # tons CO2/year
        
        # Flight emissions
        weekly_flights = transport_patterns["weekly_flights"]
        flight_distance = transport_patterns["flight_distance"]
        flight_emission_factor = 0.25  # kg CO2/km for commercial flights
        
        if transport_patterns["primary_vehicle"] == "private_jet":
            flight_emission_factor = 2.5  # Much higher for private jets
        
        annual_flight_emissions = (weekly_flights * flight_distance * flight_emission_factor * 52) / 1000
        
        total_emissions = annual_vehicle_emissions + annual_flight_emissions
        
        return round(total_emissions, 2)
    
    def _generate_route_optimizations(self, transport_patterns: Dict[str, Any], 
                                    local_options: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate route and transport optimizations"""
        
        optimizations = []
        
        # Route efficiency
        if transport_patterns["daily_distance"] > 50:
            optimizations.append({
                "type": "route_optimization",
                "suggestion": "Combine trips and optimize routes",
                "potential_reduction": "15-25%",
                "implementation": "Use route planning apps, combine errands"
            })
        
        # Public transport integration
        if local_options.get("public_transport_quality") in ["good", "excellent"]:
            optimizations.append({
                "type": "modal_shift",
                "suggestion": "Integrate public transport for longer distances",
                "potential_reduction": "40-60%",
                "implementation": "Use public transport for commuting, car for specific needs"
            })
        
        # EV charging optimization
        if local_options.get("ev_charging_stations", 0) > 1000:
            optimizations.append({
                "type": "electrification",
                "suggestion": "Switch to electric vehicle",
                "potential_reduction": "70-90%",
                "implementation": "Abundant charging infrastructure available"
            })
        
        return optimizations
    
    def _recommend_alternatives(self, transport_patterns: Dict[str, Any],
                              local_options: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recommend alternative transportation methods"""
        
        alternatives = []
        current_vehicle = transport_patterns["primary_vehicle"]
        
        # Electric vehicle recommendation
        if current_vehicle in ["luxury_car", "suv", "sedan"]:
            alternatives.append({
                "alternative": "Electric Vehicle",
                "emission_reduction": "70-90%",
                "cost_impact": "Higher upfront, lower operating costs",
                "feasibility": "high" if local_options.get("ev_charging_stations", 0) > 500 else "medium",
                "annual_savings": "3-8 tons CO2"
            })
        
        # Public transport recommendation
        if local_options.get("public_transport_quality") in ["good", "excellent"]:
            alternatives.append({
                "alternative": "Public Transport + Car Sharing",
                "emission_reduction": "60-80%",
                "cost_impact": "Significant cost savings",
                "feasibility": "high",
                "annual_savings": "4-10 tons CO2"
            })
        
        # Bike + public transport
        if local_options.get("bike_infrastructure") in ["good", "excellent"]:
            alternatives.append({
                "alternative": "Bike + Public Transport Combo",
                "emission_reduction": "80-95%",
                "cost_impact": "Major cost savings",
                "feasibility": "medium",
                "annual_savings": "6-12 tons CO2"
            })
        
        # Flight alternatives
        if transport_patterns["weekly_flights"] > 0:
            alternatives.append({
                "alternative": "High-speed rail for regional travel",
                "emission_reduction": "85-95%",
                "cost_impact": "Often comparable to flights",
                "feasibility": "depends on routes",
                "annual_savings": "10-50 tons CO2"
            })
        
        return alternatives
    
    def _calculate_transport_efficiency(self, transport_patterns: Dict[str, Any]) -> float:
        """Calculate transportation efficiency score (0-1)"""
        
        score = 0.5  # Base score
        
        # Vehicle efficiency
        vehicle_scores = {
            "walk": 1.0, "bike": 1.0, "electric": 0.9, "hybrid": 0.7,
            "train": 0.8, "bus": 0.6, "sedan": 0.4, "suv": 0.2,
            "luxury_car": 0.1, "private_jet": 0.0, "helicopter": 0.0
        }
        
        primary_vehicle = transport_patterns["primary_vehicle"]
        score = vehicle_scores.get(primary_vehicle, 0.4)
        
        # Distance penalty
        daily_distance = transport_patterns["daily_distance"]
        if daily_distance > 100:
            score *= 0.5
        elif daily_distance > 50:
            score *= 0.7
        
        # Flight penalty
        if transport_patterns["weekly_flights"] > 0:
            score *= 0.3
        
        return max(0.0, min(1.0, score))
    
    def _extract_key_findings(self, transport_patterns: Dict[str, Any], carbon_footprint: float) -> List[str]:
        """Extract key findings for agent communication"""
        
        findings = []
        
        if carbon_footprint > 10:
            findings.append("Extremely high transport emissions detected")
        elif carbon_footprint > 5:
            findings.append("High transport emissions - major improvement potential")
        
        if transport_patterns["primary_vehicle"] in ["private_jet", "helicopter"]:
            findings.append("Ultra-luxury transport with massive carbon impact")
        
        if transport_patterns["weekly_flights"] > 1:
            findings.append("Frequent flying is primary emissions source")
        
        if transport_patterns["daily_distance"] > 100:
            findings.append("Excessive daily travel distance")
        
        return findings
    
    async def communicate_with_home_expert(self, home_data: Dict[str, Any]) -> Dict[str, Any]:
        """CAPSTONE: A2A Communication with Home Expert"""
        
        # Share insights about EV charging potential
        ev_potential = {
            "home_charging_feasible": home_data.get("renewable_energy", False),
            "solar_ev_synergy": home_data.get("renewable_energy", False),
            "charging_cost_estimate": "Very low" if home_data.get("renewable_energy") else "Medium"
        }
        
        return {
            "message_type": "ev_integration_analysis",
            "sender": self.agent_id,
            "recipient": "home_expert",
            "data": ev_potential
        }