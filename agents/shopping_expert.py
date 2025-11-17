import asyncio
import requests
from typing import Dict, Any, List
import json

class ShoppingExpertAgent:
    """CAPSTONE: Sustainable Shopping and Consumption Expert"""
    
    def __init__(self):
        self.agent_id = "shopping_ninja_004"
        self.specializations = [
            "product_lifecycle_analysis",
            "circular_economy",
            "ethical_sourcing",
            "consumption_optimization"
        ]
        self.product_categories = {
            "clothing": {"avg_emissions": 8.0, "lifespan": 2},  # kg CO2, years
            "electronics": {"avg_emissions": 300.0, "lifespan": 5},
            "furniture": {"avg_emissions": 150.0, "lifespan": 10},
            "appliances": {"avg_emissions": 500.0, "lifespan": 12},
            "books": {"avg_emissions": 2.5, "lifespan": 20},
            "cosmetics": {"avg_emissions": 3.0, "lifespan": 1}
        }
    
    async def analyze(self, user_input: str, location: Dict[str, Any]) -> Dict[str, Any]:
        """CAPSTONE: Comprehensive Shopping Pattern Analysis"""
        
        # Extract shopping patterns
        shopping_patterns = self._analyze_shopping_patterns(user_input)
        
        # Get local shopping infrastructure
        local_infrastructure = await self._get_local_shopping_data(location)
        
        # Calculate consumption carbon footprint
        carbon_footprint = self._calculate_shopping_carbon_footprint(shopping_patterns)
        
        # Analyze circular economy opportunities
        circular_opportunities = self._analyze_circular_economy_potential(shopping_patterns)
        
        # Generate sustainable shopping recommendations
        recommendations = self._generate_shopping_recommendations(
            shopping_patterns, local_infrastructure, circular_opportunities
        )
        
        return {
            "agent_id": self.agent_id,
            "carbon_footprint": carbon_footprint,
            "shopping_patterns": shopping_patterns,
            "local_infrastructure": local_infrastructure,
            "circular_opportunities": circular_opportunities,
            "recommendations": recommendations,
            "efficiency_score": self._calculate_shopping_efficiency(shopping_patterns),
            "key_findings": self._extract_key_findings(shopping_patterns, carbon_footprint)
        }
    
    def _analyze_shopping_patterns(self, user_input: str) -> Dict[str, Any]:
        """Extract shopping and consumption patterns from user description"""
        
        patterns = {
            "shopping_frequency": "weekly",
            "luxury_purchases": False,
            "fast_fashion": False,
            "electronics_upgrade_cycle": "3-5 years",
            "second_hand_preference": False,
            "brand_consciousness": "medium",
            "impulse_buying": "medium",
            "bulk_buying": False,
            "online_vs_physical": "mixed"
        }
        
        # Luxury shopping detection
        luxury_keywords = ["luxury", "designer", "premium", "expensive", "high-end", "exclusive"]
        patterns["luxury_purchases"] = any(keyword in user_input.lower() for keyword in luxury_keywords)
        
        # Fast fashion indicators
        fashion_keywords = ["new clothes", "fashion", "shopping spree", "trendy", "latest style"]
        patterns["fast_fashion"] = any(keyword in user_input.lower() for keyword in fashion_keywords)
        
        # Electronics upgrade patterns
        tech_keywords = ["latest phone", "new laptop", "upgrade", "newest model", "tech enthusiast"]
        if any(keyword in user_input.lower() for keyword in tech_keywords):
            patterns["electronics_upgrade_cycle"] = "1-2 years"
        
        # Sustainable shopping indicators
        sustainable_keywords = ["second hand", "thrift", "vintage", "refurbished", "eco-friendly", "sustainable"]
        patterns["second_hand_preference"] = any(keyword in user_input.lower() for keyword in sustainable_keywords)
        
        # Shopping frequency
        frequency_keywords = {
            "daily": ["daily shopping", "shop every day"],
            "weekly": ["weekly", "once a week", "weekend shopping"],
            "monthly": ["monthly", "once a month", "rarely shop"]
        }
        
        for freq, keywords in frequency_keywords.items():
            if any(keyword in user_input.lower() for keyword in keywords):
                patterns["shopping_frequency"] = freq
                break
        
        return patterns
    
    async def _get_local_shopping_data(self, location: Dict[str, Any]) -> Dict[str, Any]:
        """Get local shopping infrastructure and options"""
        
        city = location.get("city", "Tokyo")
        
        # Mock local shopping data
        shopping_infrastructure = {
            "Tokyo": {
                "second_hand_stores": "excellent",
                "repair_services": "good",
                "local_artisans": "excellent",
                "sustainable_brands": "good",
                "recycling_programs": "excellent"
            },
            "New York": {
                "second_hand_stores": "excellent",
                "repair_services": "excellent",
                "local_artisans": "good",
                "sustainable_brands": "excellent",
                "recycling_programs": "good"
            },
            "London": {
                "second_hand_stores": "excellent",
                "repair_services": "good",
                "local_artisans": "good",
                "sustainable_brands": "excellent",
                "recycling_programs": "excellent"
            }
        }
        
        return shopping_infrastructure.get(city, {
            "second_hand_stores": "average",
            "repair_services": "average",
            "local_artisans": "average",
            "sustainable_brands": "average",
            "recycling_programs": "average"
        })
    
    def _calculate_shopping_carbon_footprint(self, shopping_patterns: Dict[str, Any]) -> float:
        """Calculate shopping-related carbon footprint in tons CO2/year"""
        
        annual_emissions = 0.0
        
        # Base consumption by category (items per year)
        base_consumption = {
            "clothing": 20,
            "electronics": 1,
            "furniture": 0.5,
            "appliances": 0.2,
            "books": 10,
            "cosmetics": 12
        }
        
        # Adjust based on shopping patterns
        if shopping_patterns["luxury_purchases"]:
            base_consumption["clothing"] *= 2
            base_consumption["electronics"] *= 1.5
        
        if shopping_patterns["fast_fashion"]:
            base_consumption["clothing"] *= 3
        
        if shopping_patterns["electronics_upgrade_cycle"] == "1-2 years":
            base_consumption["electronics"] *= 2
        
        # Frequency adjustments
        frequency_multipliers = {
            "daily": 2.0,
            "weekly": 1.0,
            "monthly": 0.5
        }
        
        freq_multiplier = frequency_multipliers.get(shopping_patterns["shopping_frequency"], 1.0)
        
        # Calculate emissions for each category
        for category, annual_items in base_consumption.items():
            adjusted_items = annual_items * freq_multiplier
            
            if category == "clothing" and shopping_patterns["second_hand_preference"]:
                adjusted_items *= 0.3  # Second-hand reduces new purchases
            
            category_data = self.product_categories.get(category, {"avg_emissions": 10.0})
            emissions = adjusted_items * category_data["avg_emissions"]
            annual_emissions += emissions
        
        return round(annual_emissions / 1000, 2)  # Convert to tons
    
    def _analyze_circular_economy_potential(self, shopping_patterns: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze opportunities for circular economy practices"""
        
        opportunities = {
            "repair_potential": "medium",
            "resale_potential": "medium",
            "sharing_potential": "low",
            "upcycling_potential": "low",
            "rental_potential": "low"
        }
        
        # High-value items have better resale potential
        if shopping_patterns["luxury_purchases"]:
            opportunities["resale_potential"] = "high"
            opportunities["rental_potential"] = "high"
        
        # Electronics have good repair potential
        if shopping_patterns["electronics_upgrade_cycle"] == "1-2 years":
            opportunities["repair_potential"] = "high"
            opportunities["resale_potential"] = "high"
        
        # Fashion items have upcycling potential
        if shopping_patterns["fast_fashion"]:
            opportunities["upcycling_potential"] = "high"
            opportunities["sharing_potential"] = "medium"
        
        return opportunities
    
    def _generate_shopping_recommendations(self, shopping_patterns: Dict[str, Any],
                                         local_infrastructure: Dict[str, Any],
                                         circular_opportunities: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate sustainable shopping recommendations"""
        
        recommendations = []
        
        # Second-hand shopping recommendation
        if not shopping_patterns["second_hand_preference"] and local_infrastructure.get("second_hand_stores") in ["good", "excellent"]:
            recommendations.append({
                "action": "Adopt 50% second-hand shopping rule",
                "impact": "Reduce shopping emissions by 40-60%",
                "cost_impact": "Significant cost savings",
                "priority": "high",
                "co2_reduction": "0.3-0.8 tons/year"
            })
        
        # Quality over quantity
        if shopping_patterns["fast_fashion"] or shopping_patterns["shopping_frequency"] == "daily":
            recommendations.append({
                "action": "Buy fewer, higher-quality items",
                "impact": "Reduce consumption emissions by 50-70%",
                "cost_impact": "Higher per-item cost, lower total spending",
                "priority": "high",
                "co2_reduction": "0.5-1.2 tons/year"
            })
        
        # Repair and maintenance
        if local_infrastructure.get("repair_services") in ["good", "excellent"]:
            recommendations.append({
                "action": "Repair instead of replace when possible",
                "impact": "Extend product lifespan by 2-5x",
                "cost_impact": "Lower long-term costs",
                "priority": "medium",
                "co2_reduction": "0.2-0.6 tons/year"
            })
        
        # Electronics optimization
        if shopping_patterns["electronics_upgrade_cycle"] == "1-2 years":
            recommendations.append({
                "action": "Extend electronics lifespan to 4-6 years",
                "impact": "Reduce electronics emissions by 60-80%",
                "cost_impact": "Major cost savings",
                "priority": "high",
                "co2_reduction": "0.4-1.0 tons/year"
            })
        
        # Sharing economy
        if circular_opportunities["sharing_potential"] in ["medium", "high"]:
            recommendations.append({
                "action": "Use sharing services for occasional-use items",
                "impact": "Reduce ownership-based emissions by 30-50%",
                "cost_impact": "Lower costs for occasional use",
                "priority": "medium",
                "co2_reduction": "0.1-0.4 tons/year"
            })
        
        return recommendations
    
    def _calculate_shopping_efficiency(self, shopping_patterns: Dict[str, Any]) -> float:
        """Calculate shopping efficiency score (0-1)"""
        
        score = 0.5  # Base score
        
        # Second-hand preference bonus
        if shopping_patterns["second_hand_preference"]:
            score += 0.3
        
        # Frequency efficiency
        frequency_scores = {"monthly": 0.2, "weekly": 0.0, "daily": -0.3}
        score += frequency_scores.get(shopping_patterns["shopping_frequency"], 0.0)
        
        # Fast fashion penalty
        if shopping_patterns["fast_fashion"]:
            score -= 0.4
        
        # Luxury purchases penalty
        if shopping_patterns["luxury_purchases"]:
            score -= 0.2
        
        # Electronics upgrade efficiency
        if shopping_patterns["electronics_upgrade_cycle"] == "1-2 years":
            score -= 0.3
        elif shopping_patterns["electronics_upgrade_cycle"] == "5+ years":
            score += 0.2
        
        return max(0.0, min(1.0, score))
    
    def _extract_key_findings(self, shopping_patterns: Dict[str, Any], carbon_footprint: float) -> List[str]:
        """Extract key findings for agent communication"""
        
        findings = []
        
        if carbon_footprint > 1.5:
            findings.append("High consumption-based emissions detected")
        
        if shopping_patterns["fast_fashion"]:
            findings.append("Fast fashion habits significantly increase carbon impact")
        
        if shopping_patterns["electronics_upgrade_cycle"] == "1-2 years":
            findings.append("Frequent electronics upgrades are major emission source")
        
        if shopping_patterns["luxury_purchases"] and not shopping_patterns["second_hand_preference"]:
            findings.append("Luxury consumption without circular practices")
        
        if shopping_patterns["second_hand_preference"]:
            findings.append("Excellent circular economy practices already in place")
        
        return findings
    
    async def communicate_with_transport_expert(self, transport_data: Dict[str, Any]) -> Dict[str, Any]:
        """CAPSTONE: A2A Communication with Transport Expert"""
        
        # Share insights about shopping-related transport
        shopping_transport_insights = {
            "online_shopping_preference": True,
            "local_shopping_priority": "high",
            "bulk_delivery_optimization": True,
            "car_free_shopping_feasibility": transport_data.get("public_transport_usage", "low") != "low"
        }
        
        return {
            "message_type": "shopping_transport_optimization",
            "sender": self.agent_id,
            "recipient": "transport_expert",
            "data": shopping_transport_insights
        }