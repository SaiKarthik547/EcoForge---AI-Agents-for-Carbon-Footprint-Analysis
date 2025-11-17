import asyncio
import requests
from typing import Dict, Any, List
import json

class DietExpertAgent:
    """CAPSTONE: Dietary Carbon Impact Expert with Nutritional Intelligence"""
    
    def __init__(self):
        self.agent_id = "diet_shaman_003"
        self.specializations = [
            "food_carbon_footprint",
            "nutritional_optimization",
            "local_sourcing",
            "seasonal_eating"
        ]
        self.food_emissions = {
            # kg CO2 per kg of food
            "beef": 60.0,
            "lamb": 24.0,
            "cheese": 21.0,
            "pork": 7.2,
            "chicken": 6.9,
            "fish": 6.1,
            "eggs": 4.2,
            "rice": 2.7,
            "milk": 3.2,
            "wheat": 1.4,
            "vegetables": 0.4,
            "fruits": 0.3,
            "legumes": 0.7,
            "nuts": 0.3
        }
    
    async def analyze(self, user_input: str, location: Dict[str, Any]) -> Dict[str, Any]:
        """CAPSTONE: Comprehensive Dietary Carbon Analysis"""
        
        # Extract dietary patterns
        dietary_patterns = self._analyze_dietary_patterns(user_input)
        
        # Get local food sourcing data
        local_sourcing = await self._get_local_food_data(location)
        
        # Calculate carbon footprint
        carbon_footprint = self._calculate_diet_carbon_footprint(dietary_patterns)
        
        # Analyze nutritional balance
        nutritional_analysis = self._analyze_nutritional_balance(dietary_patterns)
        
        # Generate dietary recommendations
        recommendations = self._generate_dietary_recommendations(
            dietary_patterns, local_sourcing, nutritional_analysis
        )
        
        return {
            "agent_id": self.agent_id,
            "carbon_footprint": carbon_footprint,
            "dietary_patterns": dietary_patterns,
            "local_sourcing": local_sourcing,
            "nutritional_analysis": nutritional_analysis,
            "recommendations": recommendations,
            "efficiency_score": self._calculate_diet_efficiency(dietary_patterns),
            "key_findings": self._extract_key_findings(dietary_patterns, carbon_footprint)
        }
    
    def _analyze_dietary_patterns(self, user_input: str) -> Dict[str, Any]:
        """Extract dietary patterns from user description"""
        
        patterns = {
            "diet_type": "omnivore",
            "meat_frequency": "daily",
            "meat_types": [],
            "dairy_consumption": "medium",
            "local_food": "low",
            "organic_preference": False,
            "meal_frequency": 3,
            "luxury_foods": False
        }
        
        # Diet type detection
        diet_keywords = {
            "vegan": ["vegan", "plant-based", "no animal products"],
            "vegetarian": ["vegetarian", "no meat", "plant diet"],
            "pescatarian": ["pescatarian", "fish only", "no meat except fish"],
            "omnivore": ["meat", "everything", "omnivore"]
        }
        
        for diet_type, keywords in diet_keywords.items():
            if any(keyword in user_input.lower() for keyword in keywords):
                patterns["diet_type"] = diet_type
                break
        
        # Meat consumption analysis
        meat_keywords = {
            "beef": ["beef", "steak", "wagyu", "hamburger", "burger"],
            "pork": ["pork", "bacon", "ham", "sausage"],
            "chicken": ["chicken", "poultry", "turkey"],
            "lamb": ["lamb", "mutton"],
            "fish": ["fish", "salmon", "tuna", "seafood"]
        }
        
        for meat_type, keywords in meat_keywords.items():
            if any(keyword in user_input.lower() for keyword in keywords):
                patterns["meat_types"].append(meat_type)
        
        # Frequency analysis
        frequency_keywords = {
            "daily": ["daily", "every day", "each day"],
            "weekly": ["weekly", "few times a week", "several times"],
            "monthly": ["monthly", "rarely", "occasionally"]
        }
        
        for freq, keywords in frequency_keywords.items():
            if any(keyword in user_input.lower() for keyword in keywords):
                patterns["meat_frequency"] = freq
                break
        
        # Luxury food detection
        luxury_keywords = ["wagyu", "caviar", "truffle", "premium", "expensive", "fine dining"]
        patterns["luxury_foods"] = any(keyword in user_input.lower() for keyword in luxury_keywords)
        
        # Local/organic detection
        local_keywords = ["local", "organic", "farm-to-table", "sustainable", "farmers market"]
        patterns["organic_preference"] = any(keyword in user_input.lower() for keyword in local_keywords)
        
        return patterns
    
    async def _get_local_food_data(self, location: Dict[str, Any]) -> Dict[str, Any]:
        """Get local food sourcing and seasonal data"""
        
        city = location.get("city", "Tokyo")
        
        # Mock local food data (in production, use agricultural APIs)
        local_data = {
            "Tokyo": {
                "local_produce_availability": 0.6,
                "seasonal_variety": ["rice", "vegetables", "fish"],
                "food_miles_average": 800,
                "organic_market_share": 0.15
            },
            "New York": {
                "local_produce_availability": 0.4,
                "seasonal_variety": ["apples", "vegetables", "dairy"],
                "food_miles_average": 1200,
                "organic_market_share": 0.25
            },
            "London": {
                "local_produce_availability": 0.5,
                "seasonal_variety": ["vegetables", "dairy", "grains"],
                "food_miles_average": 900,
                "organic_market_share": 0.20
            }
        }
        
        return local_data.get(city, {
            "local_produce_availability": 0.5,
            "seasonal_variety": ["vegetables", "grains"],
            "food_miles_average": 1000,
            "organic_market_share": 0.18
        })
    
    def _calculate_diet_carbon_footprint(self, dietary_patterns: Dict[str, Any]) -> float:
        """Calculate dietary carbon footprint in tons CO2/year"""
        
        annual_emissions = 0.0
        
        # Base consumption patterns (kg per year)
        base_consumption = {
            "beef": 0 if dietary_patterns["diet_type"] in ["vegan", "vegetarian", "pescatarian"] else 20,
            "pork": 0 if dietary_patterns["diet_type"] in ["vegan", "vegetarian", "pescatarian"] else 15,
            "chicken": 0 if dietary_patterns["diet_type"] in ["vegan", "vegetarian", "pescatarian"] else 25,
            "fish": 0 if dietary_patterns["diet_type"] == "vegan" else 15,
            "dairy": 0 if dietary_patterns["diet_type"] == "vegan" else 100,
            "vegetables": 150,
            "fruits": 80,
            "grains": 120
        }
        
        # Adjust for meat frequency
        frequency_multipliers = {
            "daily": 1.5,
            "weekly": 1.0,
            "monthly": 0.3
        }
        
        meat_multiplier = frequency_multipliers.get(dietary_patterns["meat_frequency"], 1.0)
        
        # Calculate emissions for each food category
        for food_type in ["beef", "pork", "chicken"]:
            if food_type in dietary_patterns["meat_types"]:
                consumption = base_consumption[food_type] * meat_multiplier
                if dietary_patterns["luxury_foods"] and food_type == "beef":
                    consumption *= 2  # Luxury beef consumption
                
                emission_factor = self.food_emissions.get(food_type, 6.0)
                annual_emissions += consumption * emission_factor
        
        # Fish consumption
        if dietary_patterns["diet_type"] != "vegan":
            fish_consumption = base_consumption["fish"]
            if "fish" in dietary_patterns["meat_types"]:
                fish_consumption *= 1.5
            annual_emissions += fish_consumption * self.food_emissions["fish"]
        
        # Dairy consumption
        if dietary_patterns["diet_type"] != "vegan":
            dairy_consumption = base_consumption["dairy"]
            annual_emissions += dairy_consumption * self.food_emissions["milk"]
        
        # Plant-based foods
        for food_type in ["vegetables", "fruits"]:
            consumption = base_consumption[food_type]
            if dietary_patterns["organic_preference"]:
                consumption *= 0.8  # Organic typically has lower transport emissions
            annual_emissions += consumption * self.food_emissions[food_type]
        
        # Grains
        grain_consumption = base_consumption["grains"]
        annual_emissions += grain_consumption * self.food_emissions["wheat"]
        
        return round(annual_emissions / 1000, 2)  # Convert to tons
    
    def _analyze_nutritional_balance(self, dietary_patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze nutritional balance of current diet"""
        
        nutrition_score = 0.5  # Base score
        
        # Diet type nutritional assessment
        diet_nutrition = {
            "vegan": {"protein": 0.7, "b12": 0.3, "iron": 0.6, "omega3": 0.4},
            "vegetarian": {"protein": 0.8, "b12": 0.7, "iron": 0.7, "omega3": 0.5},
            "pescatarian": {"protein": 0.9, "b12": 0.9, "iron": 0.8, "omega3": 0.9},
            "omnivore": {"protein": 0.9, "b12": 0.9, "iron": 0.9, "omega3": 0.7}
        }
        
        diet_type = dietary_patterns["diet_type"]
        nutrition_profile = diet_nutrition.get(diet_type, diet_nutrition["omnivore"])
        
        # Calculate overall nutrition score
        avg_nutrition = sum(nutrition_profile.values()) / len(nutrition_profile)
        
        return {
            "overall_score": avg_nutrition,
            "protein_adequacy": nutrition_profile["protein"],
            "b12_status": nutrition_profile["b12"],
            "iron_status": nutrition_profile["iron"],
            "omega3_status": nutrition_profile["omega3"],
            "recommendations": self._get_nutrition_recommendations(nutrition_profile)
        }
    
    def _get_nutrition_recommendations(self, nutrition_profile: Dict[str, float]) -> List[str]:
        """Generate nutritional recommendations"""
        
        recommendations = []
        
        if nutrition_profile["protein"] < 0.8:
            recommendations.append("Consider adding legumes, nuts, or plant-based protein sources")
        
        if nutrition_profile["b12"] < 0.7:
            recommendations.append("Consider B12 supplementation or fortified foods")
        
        if nutrition_profile["iron"] < 0.7:
            recommendations.append("Include iron-rich foods like spinach, lentils, or lean meats")
        
        if nutrition_profile["omega3"] < 0.6:
            recommendations.append("Add omega-3 sources like fish, walnuts, or flax seeds")
        
        return recommendations
    
    def _generate_dietary_recommendations(self, dietary_patterns: Dict[str, Any],
                                        local_sourcing: Dict[str, Any],
                                        nutritional_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate personalized dietary recommendations"""
        
        recommendations = []
        
        # Meat reduction recommendations
        if dietary_patterns["diet_type"] == "omnivore" and dietary_patterns["meat_frequency"] == "daily":
            recommendations.append({
                "action": "Reduce meat consumption to 3-4 times per week",
                "impact": "Reduce diet emissions by 30-40%",
                "nutrition_impact": "Maintain protein with legumes and fish",
                "priority": "high",
                "co2_reduction": "1-2 tons/year"
            })
        
        # Beef-specific recommendation
        if "beef" in dietary_patterns["meat_types"]:
            recommendations.append({
                "action": "Replace beef with chicken or plant proteins",
                "impact": "Reduce diet emissions by 50-70%",
                "nutrition_impact": "Similar protein content, lower saturated fat",
                "priority": "high",
                "co2_reduction": "2-4 tons/year"
            })
        
        # Local sourcing recommendation
        if not dietary_patterns["organic_preference"]:
            recommendations.append({
                "action": "Choose local and seasonal produce",
                "impact": "Reduce transport emissions by 20-30%",
                "nutrition_impact": "Fresher nutrients, seasonal variety",
                "priority": "medium",
                "co2_reduction": "0.3-0.8 tons/year"
            })
        
        # Plant-based meal recommendation
        recommendations.append({
            "action": "Implement 2-3 plant-based days per week",
            "impact": "Reduce weekly diet emissions by 25-35%",
            "nutrition_impact": "Increase fiber and antioxidants",
            "priority": "medium",
            "co2_reduction": "0.8-1.5 tons/year"
        })
        
        return recommendations
    
    def _calculate_diet_efficiency(self, dietary_patterns: Dict[str, Any]) -> float:
        """Calculate dietary efficiency score (0-1)"""
        
        # Base scores by diet type
        diet_scores = {
            "vegan": 0.9,
            "vegetarian": 0.7,
            "pescatarian": 0.6,
            "omnivore": 0.3
        }
        
        score = diet_scores.get(dietary_patterns["diet_type"], 0.3)
        
        # Adjust for meat frequency
        if dietary_patterns["diet_type"] == "omnivore":
            frequency_adjustments = {
                "daily": 0.0,
                "weekly": 0.2,
                "monthly": 0.4
            }
            score += frequency_adjustments.get(dietary_patterns["meat_frequency"], 0.0)
        
        # Bonus for local/organic
        if dietary_patterns["organic_preference"]:
            score += 0.1
        
        # Penalty for luxury foods
        if dietary_patterns["luxury_foods"]:
            score -= 0.2
        
        return max(0.0, min(1.0, score))
    
    def _extract_key_findings(self, dietary_patterns: Dict[str, Any], carbon_footprint: float) -> List[str]:
        """Extract key findings for agent communication"""
        
        findings = []
        
        if carbon_footprint > 4:
            findings.append("High-impact diet with significant reduction potential")
        
        if "beef" in dietary_patterns["meat_types"] and dietary_patterns["meat_frequency"] == "daily":
            findings.append("Daily beef consumption is primary diet emission source")
        
        if dietary_patterns["luxury_foods"]:
            findings.append("Luxury food choices significantly increase carbon impact")
        
        if dietary_patterns["diet_type"] in ["vegan", "vegetarian"]:
            findings.append("Plant-based diet provides excellent carbon efficiency")
        
        return findings
    
    async def communicate_with_shopping_expert(self, shopping_data: Dict[str, Any]) -> Dict[str, Any]:
        """CAPSTONE: A2A Communication with Shopping Expert"""
        
        # Share insights about food purchasing patterns
        food_shopping_insights = {
            "organic_food_priority": True,
            "local_sourcing_importance": "high",
            "bulk_buying_foods": ["grains", "legumes", "nuts"],
            "seasonal_shopping_calendar": ["spring_vegetables", "summer_fruits", "winter_roots"]
        }
        
        return {
            "message_type": "food_shopping_optimization",
            "sender": self.agent_id,
            "recipient": "shopping_expert",
            "data": food_shopping_insights
        }