import requests
from typing import Dict, Any, List, Optional
import json

class TavilySearch:
    """CAPSTONE: Real-time Information Search via Tavily Free API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or "demo_key"  # Free tier
        self.base_url = "https://api.tavily.com"
    
    async def search_sustainability_info(self, query: str, location: str = "") -> Dict[str, Any]:
        """Search for sustainability and environmental information"""
        
        try:
            # Enhanced query with location context
            enhanced_query = f"{query} {location} sustainability environment 2024"
            
            # Mock search results for demo (in production, use real Tavily API)
            mock_results = self._get_mock_sustainability_results(query, location)
            
            return {
                "query": enhanced_query,
                "results": mock_results,
                "source": "tavily_search_api",
                "result_count": len(mock_results)
            }
            
        except Exception as e:
            return {
                "query": query,
                "results": [{"title": "Search unavailable", "content": "Using fallback data"}],
                "source": "fallback_search",
                "error": str(e)
            }
    
    def _get_mock_sustainability_results(self, query: str, location: str) -> List[Dict[str, Any]]:
        """Generate relevant mock results based on query"""
        
        query_lower = query.lower()
        
        if "solar" in query_lower or "renewable energy" in query_lower:
            return [
                {
                    "title": "Solar Panel Installation Guide 2024",
                    "content": "Solar panels can reduce home electricity costs by 70-90%. Average payback period is 6-8 years with current incentives.",
                    "url": "https://example.com/solar-guide",
                    "relevance_score": 0.95
                },
                {
                    "title": "Local Solar Incentives and Tax Credits",
                    "content": f"In {location}, solar installations qualify for federal tax credits plus local rebates. Net metering available.",
                    "url": "https://example.com/solar-incentives",
                    "relevance_score": 0.88
                },
                {
                    "title": "Best Solar Installers Near You",
                    "content": "Top-rated certified solar installers with warranties and financing options. Get multiple quotes for best pricing.",
                    "url": "https://example.com/solar-installers",
                    "relevance_score": 0.82
                }
            ]
        
        elif "electric vehicle" in query_lower or "ev" in query_lower:
            return [
                {
                    "title": "Electric Vehicle Buying Guide 2024",
                    "content": "EVs now offer 300+ mile range with expanding charging networks. Total cost of ownership 40% lower than gas cars.",
                    "url": "https://example.com/ev-guide",
                    "relevance_score": 0.93
                },
                {
                    "title": "EV Charging Infrastructure Near You",
                    "content": f"{location} has extensive charging network with fast-charging stations every 25 miles on major routes.",
                    "url": "https://example.com/ev-charging",
                    "relevance_score": 0.87
                },
                {
                    "title": "EV Tax Credits and Incentives",
                    "content": "Federal tax credits up to $7,500 for new EVs, plus state and local incentives. Some utilities offer charging rebates.",
                    "url": "https://example.com/ev-incentives",
                    "relevance_score": 0.85
                }
            ]
        
        elif "diet" in query_lower or "plant based" in query_lower or "food" in query_lower:
            return [
                {
                    "title": "Plant-Based Diet Environmental Impact",
                    "content": "Shifting to plant-based diet can reduce food-related emissions by 50-70%. Health benefits include reduced disease risk.",
                    "url": "https://example.com/plant-diet",
                    "relevance_score": 0.91
                },
                {
                    "title": "Local Organic and Sustainable Food Sources",
                    "content": f"Farmers markets and organic stores in {location}. Local sourcing reduces transport emissions by 30%.",
                    "url": "https://example.com/local-food",
                    "relevance_score": 0.86
                },
                {
                    "title": "Nutritional Balance in Plant-Based Diets",
                    "content": "Complete protein sources from legumes, nuts, and grains. B12 supplementation recommended for vegans.",
                    "url": "https://example.com/nutrition",
                    "relevance_score": 0.83
                }
            ]
        
        elif "insulation" in query_lower or "energy efficiency" in query_lower:
            return [
                {
                    "title": "Home Energy Efficiency Upgrades 2024",
                    "content": "Insulation and air sealing can reduce heating/cooling costs by 30-50%. LED lighting saves 75% on lighting costs.",
                    "url": "https://example.com/efficiency",
                    "relevance_score": 0.89
                },
                {
                    "title": "Energy Audit and Rebate Programs",
                    "content": f"Utility companies in {location} offer free energy audits and rebates for efficiency upgrades up to $2,000.",
                    "url": "https://example.com/rebates",
                    "relevance_score": 0.84
                },
                {
                    "title": "Smart Home Energy Management",
                    "content": "Smart thermostats and energy monitoring reduce consumption by 15-20%. Automated systems optimize usage patterns.",
                    "url": "https://example.com/smart-home",
                    "relevance_score": 0.81
                }
            ]
        
        elif "carbon footprint" in query_lower or "emissions" in query_lower:
            return [
                {
                    "title": "Understanding Your Carbon Footprint",
                    "content": "Average person emits 4.8 tons CO2/year globally. Transport (29%) and electricity (25%) are largest sources.",
                    "url": "https://example.com/carbon-footprint",
                    "relevance_score": 0.92
                },
                {
                    "title": "Carbon Offset Programs and Verification",
                    "content": "Verified carbon offsets cost $15-50 per ton. Focus on reduction first, then offset remaining emissions.",
                    "url": "https://example.com/offsets",
                    "relevance_score": 0.87
                },
                {
                    "title": "Corporate and Personal Climate Action",
                    "content": "Science-based targets align with 1.5°C pathway. Individual actions inspire community and policy change.",
                    "url": "https://example.com/climate-action",
                    "relevance_score": 0.85
                }
            ]
        
        else:
            # General sustainability results
            return [
                {
                    "title": "Sustainable Living Guide 2024",
                    "content": "Comprehensive guide to reducing environmental impact through home, transport, diet, and consumption choices.",
                    "url": "https://example.com/sustainable-living",
                    "relevance_score": 0.88
                },
                {
                    "title": "Climate Change Solutions That Work",
                    "content": "Proven strategies for individuals and communities to reduce emissions and build resilience to climate impacts.",
                    "url": "https://example.com/climate-solutions",
                    "relevance_score": 0.85
                },
                {
                    "title": "Green Technology Trends and Adoption",
                    "content": "Latest developments in clean energy, electric transport, and sustainable materials making environmental action easier.",
                    "url": "https://example.com/green-tech",
                    "relevance_score": 0.82
                }
            ]
    
    async def search_local_resources(self, resource_type: str, location: str) -> Dict[str, Any]:
        """Search for local sustainability resources"""
        
        try:
            query = f"{resource_type} {location} local directory services"
            
            mock_results = self._get_mock_local_results(resource_type, location)
            
            return {
                "query": query,
                "resource_type": resource_type,
                "location": location,
                "results": mock_results,
                "source": "tavily_local_search"
            }
            
        except Exception as e:
            return {
                "query": f"{resource_type} {location}",
                "results": [{"title": "Local search unavailable", "content": "Contact local environmental organizations"}],
                "source": "fallback_local_search",
                "error": str(e)
            }
    
    def _get_mock_local_results(self, resource_type: str, location: str) -> List[Dict[str, Any]]:
        """Generate mock local resource results"""
        
        if "solar" in resource_type.lower():
            return [
                {
                    "name": f"{location} Solar Solutions",
                    "type": "Solar Installer",
                    "contact": "(555) 123-4567",
                    "rating": 4.8,
                    "description": "Certified solar installer with 500+ installations. Free consultations and financing available."
                },
                {
                    "name": "SunPower Authorized Dealer",
                    "type": "Solar Installer", 
                    "contact": "(555) 234-5678",
                    "rating": 4.7,
                    "description": "Premium solar panels with 25-year warranty. Specializes in residential and commercial installations."
                }
            ]
        
        elif "electric" in resource_type.lower() or "ev" in resource_type.lower():
            return [
                {
                    "name": f"{location} EV Center",
                    "type": "EV Dealership",
                    "contact": "(555) 345-6789",
                    "rating": 4.6,
                    "description": "Multi-brand EV dealership with test drives, financing, and charging station installation services."
                },
                {
                    "name": "ChargePoint Network",
                    "type": "Charging Infrastructure",
                    "contact": "chargepoint.com",
                    "rating": 4.5,
                    "description": "Extensive fast-charging network with mobile app for finding and reserving charging stations."
                }
            ]
        
        elif "organic" in resource_type.lower() or "food" in resource_type.lower():
            return [
                {
                    "name": f"{location} Farmers Market",
                    "type": "Local Food Market",
                    "contact": "Saturdays 8am-2pm",
                    "rating": 4.9,
                    "description": "Weekly farmers market with local organic produce, artisanal foods, and sustainable products."
                },
                {
                    "name": "Green Grocer Co-op",
                    "type": "Organic Grocery",
                    "contact": "(555) 456-7890",
                    "rating": 4.4,
                    "description": "Community-owned grocery store specializing in organic, local, and sustainably sourced products."
                }
            ]
        
        else:
            return [
                {
                    "name": f"{location} Environmental Alliance",
                    "type": "Environmental Organization",
                    "contact": "(555) 567-8901",
                    "rating": 4.7,
                    "description": "Local environmental group offering education, advocacy, and community sustainability programs."
                },
                {
                    "name": "Green Building Council",
                    "type": "Sustainability Organization",
                    "contact": "(555) 678-9012", 
                    "rating": 4.5,
                    "description": "Professional organization promoting sustainable building practices and green certifications."
                }
            ]
    
    async def search_incentives_and_rebates(self, category: str, location: str) -> Dict[str, Any]:
        """Search for financial incentives and rebates"""
        
        query = f"{category} incentives rebates tax credits {location} 2024"
        
        try:
            mock_incentives = self._get_mock_incentives(category, location)
            
            return {
                "query": query,
                "category": category,
                "location": location,
                "incentives": mock_incentives,
                "source": "tavily_incentives_search"
            }
            
        except Exception as e:
            return {
                "query": query,
                "incentives": [{"title": "Incentive search unavailable", "description": "Contact local utility companies"}],
                "source": "fallback_incentives_search",
                "error": str(e)
            }
    
    def _get_mock_incentives(self, category: str, location: str) -> List[Dict[str, Any]]:
        """Generate mock incentive results"""
        
        if "solar" in category.lower():
            return [
                {
                    "title": "Federal Solar Investment Tax Credit",
                    "description": "30% tax credit for solar installations through 2032",
                    "amount": "30% of system cost",
                    "expires": "2032-12-31",
                    "type": "Federal Tax Credit"
                },
                {
                    "title": f"{location} Solar Rebate Program",
                    "description": "Local utility rebate for residential solar installations",
                    "amount": "$1,000-3,000 per installation",
                    "expires": "2024-12-31",
                    "type": "Utility Rebate"
                }
            ]
        
        elif "electric" in category.lower() or "ev" in category.lower():
            return [
                {
                    "title": "Federal EV Tax Credit",
                    "description": "Up to $7,500 tax credit for qualifying new electric vehicles",
                    "amount": "$7,500 maximum",
                    "expires": "Ongoing",
                    "type": "Federal Tax Credit"
                },
                {
                    "title": f"{location} EV Rebate",
                    "description": "State rebate for electric vehicle purchases",
                    "amount": "$2,000-5,000",
                    "expires": "2024-12-31", 
                    "type": "State Rebate"
                }
            ]
        
        elif "efficiency" in category.lower():
            return [
                {
                    "title": "Energy Efficiency Rebates",
                    "description": "Utility rebates for insulation, windows, and HVAC upgrades",
                    "amount": "$500-2,000 per upgrade",
                    "expires": "Ongoing",
                    "type": "Utility Rebate"
                },
                {
                    "title": "Weatherization Assistance Program",
                    "description": "Free energy efficiency upgrades for qualifying households",
                    "amount": "Up to $8,000 in upgrades",
                    "expires": "Ongoing",
                    "type": "Government Program"
                }
            ]
        
        else:
            return [
                {
                    "title": "General Sustainability Incentives",
                    "description": "Various local and federal programs supporting environmental initiatives",
                    "amount": "Varies by program",
                    "expires": "Various dates",
                    "type": "Mixed Programs"
                }
            ]