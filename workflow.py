import asyncio
from typing import Dict, Any, List
import json
from datetime import datetime

# Import configuration and agents
from config import Config
from agents.supervisor import SupervisorAgent
from agents.home_expert import HomeExpertAgent
from agents.transport_expert import TransportExpertAgent
from agents.diet_expert import DietExpertAgent
from agents.shopping_expert import ShoppingExpertAgent
from agents.synthesizer import SynthesizerAgent
from agents.refiner_loop import RefinerLoopAgent
from agents.evaluator import EvaluatorAgent

class EcoForgeWorkflow:
    """CAPSTONE: Complete EcoForge AI Agent Workflow Orchestration"""
    
    def __init__(self):
        self.config = Config()
        
        # Initialize all agents
        self.supervisor = SupervisorAgent()
        self.home_expert = HomeExpertAgent()
        self.transport_expert = TransportExpertAgent()
        self.diet_expert = DietExpertAgent()
        self.shopping_expert = ShoppingExpertAgent()
        self.synthesizer = SynthesizerAgent()
        self.refiner = RefinerLoopAgent()
        self.evaluator = EvaluatorAgent()
        
        # Workflow state
        self.workflow_state = {
            "session_id": None,
            "user_input": None,
            "supervisor_analysis": None,
            "domain_analyses": {},
            "synthesis_result": None,
            "refinement_history": [],
            "final_evaluation": None,
            "workflow_complete": False
        }
    
    async def run_complete_analysis(self, user_input: str) -> Dict[str, Any]:
        """CAPSTONE: Run the complete multi-agent analysis workflow"""
        
        # Initialize workflow
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.workflow_state["session_id"] = session_id
        self.workflow_state["user_input"] = user_input
        
        try:
            # Step 1: Supervisor Analysis
            supervisor_result = await self._run_supervisor_analysis(user_input)
            self.workflow_state["supervisor_analysis"] = supervisor_result
            
            # Step 2: Parallel Domain Expert Analysis
            domain_results = await self._run_parallel_domain_analysis(supervisor_result)
            self.workflow_state["domain_analyses"] = domain_results
            
            # Step 3: Cross-Domain Synthesis
            synthesis_result = await self._run_synthesis(domain_results)
            self.workflow_state["synthesis_result"] = synthesis_result
            
            # Step 4: Iterative Refinement (Optional)
            if self._should_refine(synthesis_result):
                refinement_result = await self._run_refinement_loop(synthesis_result)
                self.workflow_state["refinement_history"].append(refinement_result)
                synthesis_result = refinement_result.get("refined_plan", synthesis_result)
            
            # Step 5: Final Evaluation and Plan Generation
            final_result = await self._run_final_evaluation(synthesis_result, user_input)
            self.workflow_state["final_evaluation"] = final_result
            self.workflow_state["workflow_complete"] = True
            
            # Return comprehensive results
            return self._compile_final_results()
            
        except Exception as e:
            return {
                "error": f"Workflow failed: {str(e)}",
                "partial_results": self.workflow_state,
                "eco_score": 25,  # Default low score for errors
                "total_carbon_footprint": 12.5,
                "prioritized_actions": [
                    {
                        "action": "Start with energy-efficient LED lighting",
                        "co2_reduction": "0.5 tons/year",
                        "feasibility": "high",
                        "cost_impact": "Low cost, immediate savings",
                        "domain": "home"
                    }
                ]
            }
    
    async def _run_supervisor_analysis(self, user_input: str) -> Dict[str, Any]:
        """Step 1: Supervisor agent analyzes user input and coordinates workflow"""
        
        if Config.USE_MOCK_DATA:
            # Mock supervisor analysis for demo
            return {
                "agent_id": "supervisor_001",
                "user_profile": {
                    "location": "Tokyo, Japan",
                    "lifestyle_category": "urban_professional",
                    "income_level": "high",
                    "environmental_awareness": "medium"
                },
                "domain_priorities": {
                    "transport": 0.35,  # High priority - luxury SUV
                    "home": 0.25,      # Medium priority - apartment
                    "diet": 0.25,      # Medium priority - wagyu consumption
                    "shopping": 0.15   # Lower priority - designer items
                },
                "analysis_strategy": "comprehensive_assessment",
                "estimated_footprint_category": "very_high",
                "coordination_plan": {
                    "parallel_domains": ["home", "transport", "diet", "shopping"],
                    "sequential_steps": ["synthesis", "refinement", "evaluation"],
                    "expected_duration": "45 seconds"
                }
            }
        else:
            # Real supervisor analysis would go here
            return await self.supervisor.analyze_and_coordinate(user_input)
    
    async def _run_parallel_domain_analysis(self, supervisor_result: Dict[str, Any]) -> Dict[str, Any]:
        """Step 2: Run domain expert agents in parallel"""
        
        # Create parallel tasks for domain experts
        tasks = []
        
        # Home analysis task
        tasks.append(self._run_home_analysis(supervisor_result))
        
        # Transport analysis task  
        tasks.append(self._run_transport_analysis(supervisor_result))
        
        # Diet analysis task
        tasks.append(self._run_diet_analysis(supervisor_result))
        
        # Shopping analysis task
        tasks.append(self._run_shopping_analysis(supervisor_result))
        
        # Execute all domain analyses in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Compile results
        domain_results = {
            "home": results[0] if not isinstance(results[0], Exception) else self._get_fallback_home_analysis(),
            "transport": results[1] if not isinstance(results[1], Exception) else self._get_fallback_transport_analysis(),
            "diet": results[2] if not isinstance(results[2], Exception) else self._get_fallback_diet_analysis(),
            "shopping": results[3] if not isinstance(results[3], Exception) else self._get_fallback_shopping_analysis()
        }
        
        return domain_results
    
    async def _run_home_analysis(self, supervisor_result: Dict[str, Any]) -> Dict[str, Any]:
        """Home domain expert analysis"""
        
        if Config.USE_MOCK_DATA:
            return {
                "agent_id": "home_expert_002",
                "carbon_footprint": 3.2,  # tons CO2/year
                "efficiency_score": 0.4,  # 40% efficient
                "energy_patterns": {
                    "electricity_usage": "high",
                    "heating_cooling": "moderate", 
                    "renewable_energy": False,
                    "smart_systems": False
                },
                "key_findings": [
                    "High electricity consumption in urban apartment",
                    "No renewable energy sources",
                    "Inefficient heating/cooling systems",
                    "Potential for smart home upgrades"
                ],
                "recommendations": [
                    {
                        "action": "Install solar panels or subscribe to renewable energy",
                        "impact": "Reduce home emissions by 60-80%",
                        "priority": "high",
                        "co2_reduction": "2.0 tons/year",
                        "cost_impact": "High initial, excellent long-term savings"
                    },
                    {
                        "action": "Upgrade to smart thermostat and LED lighting",
                        "impact": "Reduce energy consumption by 15-25%",
                        "priority": "medium",
                        "co2_reduction": "0.5 tons/year", 
                        "cost_impact": "Medium cost, quick payback"
                    },
                    {
                        "action": "Improve insulation and air sealing",
                        "impact": "Reduce heating/cooling needs by 30%",
                        "priority": "medium",
                        "co2_reduction": "0.8 tons/year",
                        "cost_impact": "Medium cost, long-term savings"
                    }
                ]
            }
        else:
            return await self.home_expert.analyze(supervisor_result['user_input'], supervisor_result['location'])
    
    async def _run_transport_analysis(self, supervisor_result: Dict[str, Any]) -> Dict[str, Any]:
        """Transport domain expert analysis"""
        
        if Config.USE_MOCK_DATA:
            return {
                "agent_id": "transport_expert_003",
                "carbon_footprint": 5.8,  # tons CO2/year
                "efficiency_score": 0.2,  # 20% efficient - very poor
                "transport_patterns": {
                    "primary_vehicle": "luxury_suv",
                    "daily_distance": 20,  # km
                    "fuel_efficiency": "poor",
                    "public_transport_usage": "minimal",
                    "flight_frequency": "high"
                },
                "key_findings": [
                    "Luxury SUV with very high emissions",
                    "Daily commuting in urban area",
                    "Minimal use of public transportation",
                    "Frequent air travel compounds impact"
                ],
                "recommendations": [
                    {
                        "action": "Switch to electric vehicle (Tesla Model Y or similar)",
                        "impact": "Reduce transport emissions by 70-80%",
                        "priority": "high",
                        "co2_reduction": "4.2 tons/year",
                        "cost_impact": "High initial, significant fuel savings"
                    },
                    {
                        "action": "Use public transport for 50% of trips",
                        "impact": "Reduce daily commute emissions by 60%",
                        "priority": "high",
                        "co2_reduction": "1.8 tons/year",
                        "cost_impact": "Cost savings immediately"
                    },
                    {
                        "action": "Optimize flight travel and purchase carbon offsets",
                        "impact": "Reduce flight-related emissions",
                        "priority": "medium",
                        "co2_reduction": "1.0 tons/year",
                        "cost_impact": "Medium cost for offsets"
                    }
                ]
            }
        else:
            return await self.transport_expert.analyze(supervisor_result['user_input'], supervisor_result['location'])
    
    async def _run_diet_analysis(self, supervisor_result: Dict[str, Any]) -> Dict[str, Any]:
        """Diet domain expert analysis"""
        
        if Config.USE_MOCK_DATA:
            return {
                "agent_id": "diet_expert_004",
                "carbon_footprint": 2.8,  # tons CO2/year
                "efficiency_score": 0.3,  # 30% efficient
                "dietary_patterns": {
                    "meat_consumption": "very_high",
                    "beef_frequency": "daily",
                    "local_sourcing": False,
                    "organic_preference": False,
                    "food_waste": "moderate"
                },
                "key_findings": [
                    "Very high beef consumption (wagyu daily)",
                    "Minimal plant-based meals",
                    "Limited local/organic food sourcing",
                    "Moderate food waste levels"
                ],
                "recommendations": [
                    {
                        "action": "Reduce beef consumption to 2-3 times per week",
                        "impact": "Reduce diet emissions by 40-50%",
                        "priority": "high",
                        "co2_reduction": "1.2 tons/year",
                        "cost_impact": "Potential cost savings"
                    },
                    {
                        "action": "Introduce 2 plant-based days per week",
                        "impact": "Further reduce diet emissions by 20%",
                        "priority": "medium",
                        "co2_reduction": "0.6 tons/year",
                        "cost_impact": "Cost savings on protein"
                    },
                    {
                        "action": "Source locally and reduce food waste",
                        "impact": "Reduce supply chain and waste emissions",
                        "priority": "medium",
                        "co2_reduction": "0.4 tons/year",
                        "cost_impact": "Neutral to slight savings"
                    }
                ]
            }
        else:
            return await self.diet_expert.analyze(supervisor_result['user_input'], supervisor_result['location'])
    
    async def _run_shopping_analysis(self, supervisor_result: Dict[str, Any]) -> Dict[str, Any]:
        """Shopping domain expert analysis"""
        
        if Config.USE_MOCK_DATA:
            return {
                "agent_id": "shopping_expert_005",
                "carbon_footprint": 1.2,  # tons CO2/year
                "efficiency_score": 0.4,  # 40% efficient
                "shopping_patterns": {
                    "luxury_items": True,
                    "fast_fashion": False,
                    "second_hand_preference": False,
                    "local_shopping": True,
                    "shopping_frequency": "monthly"
                },
                "key_findings": [
                    "High-quality luxury purchases (better longevity)",
                    "Monthly shopping frequency is reasonable",
                    "Limited second-hand or sustainable options",
                    "Local shopping reduces transport emissions"
                ],
                "recommendations": [
                    {
                        "action": "Incorporate 30% second-hand luxury items",
                        "impact": "Reduce shopping emissions by 25%",
                        "priority": "medium",
                        "co2_reduction": "0.3 tons/year",
                        "cost_impact": "Significant cost savings"
                    },
                    {
                        "action": "Choose sustainable luxury brands",
                        "impact": "Support circular economy",
                        "priority": "medium",
                        "co2_reduction": "0.2 tons/year",
                        "cost_impact": "Similar cost, better impact"
                    },
                    {
                        "action": "Extend product lifecycles through care",
                        "impact": "Reduce replacement frequency",
                        "priority": "low",
                        "co2_reduction": "0.1 tons/year",
                        "cost_impact": "Cost savings long-term"
                    }
                ]
            }
        else:
            return await self.shopping_expert.analyze(supervisor_result['user_input'], supervisor_result['location'])
    
    async def _run_synthesis(self, domain_results: Dict[str, Any]) -> Dict[str, Any]:
        """Step 3: Cross-domain synthesis"""
        
        if Config.USE_MOCK_DATA:
            # Calculate totals from domain analyses
            total_footprint = sum([
                domain_results["home"]["carbon_footprint"],
                domain_results["transport"]["carbon_footprint"], 
                domain_results["diet"]["carbon_footprint"],
                domain_results["shopping"]["carbon_footprint"]
            ])
            
            # Collect all recommendations
            all_recommendations = []
            for domain, analysis in domain_results.items():
                for rec in analysis["recommendations"]:
                    rec["domain"] = domain
                    all_recommendations.append(rec)
            
            # Mock synthesis result
            return {
                "agent_id": "synthesizer_master_005",
                "total_carbon_footprint": total_footprint,
                "domain_breakdown": {
                    domain: {
                        "carbon_footprint": analysis["carbon_footprint"],
                        "efficiency_score": analysis["efficiency_score"],
                        "key_findings": analysis["key_findings"],
                        "improvement_potential": "high" if analysis["efficiency_score"] < 0.4 else "medium"
                    }
                    for domain, analysis in domain_results.items()
                },
                "synergies": [
                    {
                        "type": "home_transport_ev_solar",
                        "domains": ["home", "transport"],
                        "description": "Solar panels + Electric vehicle combo",
                        "synergy_multiplier": 1.5,
                        "combined_impact": "Reduce both home and transport emissions by 80%+",
                        "implementation_order": ["home_solar", "transport_ev"]
                    }
                ],
                "prioritized_actions": sorted(all_recommendations, 
                                            key=lambda x: self._calculate_priority_score(x), 
                                            reverse=True)[:8],
                "impact_analysis": {
                    "total_potential_reduction": 8.5,  # tons CO2/year
                    "quick_wins": [r for r in all_recommendations if r.get("priority") == "high"][:3],
                    "high_impact_projects": [r for r in all_recommendations if "4." in r.get("co2_reduction", "")][:2]
                },
                "eco_score": max(25, min(100, 100 - (total_footprint / 4.8) * 40)),  # Based on global average
                "synthesis_confidence": 0.85
            }
        else:
            return await self.synthesizer.synthesize(domain_results)
    
    def _calculate_priority_score(self, recommendation: Dict[str, Any]) -> float:
        """Calculate priority score for recommendation sorting"""
        priority_scores = {"high": 3, "medium": 2, "low": 1}
        priority = priority_scores.get(recommendation.get("priority", "medium"), 2)
        
        # Extract CO2 reduction number
        co2_text = recommendation.get("co2_reduction", "0.5")
        try:
            import re
            numbers = re.findall(r'(\d+(?:\.\d+)?)', co2_text)
            impact = float(numbers[-1]) if numbers else 0.5
        except:
            impact = 0.5
        
        return priority * impact
    
    async def _run_refinement_loop(self, synthesis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Step 4: Iterative refinement (optional)"""
        
        if Config.USE_MOCK_DATA:
            return {
                "iteration": 1,
                "quality_assessment": {
                    "feasibility_score": 0.75,
                    "impact_score": 0.80,
                    "cost_effectiveness": 0.70,
                    "implementation_clarity": 0.85,
                    "user_alignment": 0.75
                },
                "refinement_opportunities": [
                    {
                        "type": "sequencing_optimization",
                        "description": "Improve implementation sequencing and dependencies",
                        "refinement_strategy": "dependency_analysis"
                    }
                ],
                "refined_plan": synthesis_result,  # In demo, return original
                "improvement_validation": {
                    "overall_improvement": 0.05,
                    "validation_passed": True
                },
                "quality_score": 0.77,
                "refinement_confidence": 0.8
            }
        else:
            return await self.refiner.refine_plan(synthesis_result, self.workflow_state["refinement_history"])
    
    async def _run_final_evaluation(self, synthesis_result: Dict[str, Any], user_input: str) -> Dict[str, Any]:
        """Step 5: Final evaluation and plan generation"""
        
        evaluation_input = {
            "synthesis": synthesis_result,
            "refinements": self.workflow_state["refinement_history"],
            "user_input": user_input
        }
        
        if Config.USE_MOCK_DATA:
            return {
                "agent_id": "evaluator_final_007",
                "evaluation_results": {
                    "carbon_impact": {
                        "current_footprint": synthesis_result.get("total_carbon_footprint", 13.0),
                        "potential_reduction": 8.5,
                        "reduction_percentage": 65.4,
                        "impact_score": 0.93,
                        "impact_category": "substantial"
                    },
                    "feasibility": {
                        "feasibility_score": 0.75,
                        "feasibility_category": "moderately_feasible"
                    },
                    "overall_score": 0.84
                },
                "final_plan": {
                    "final_actions": synthesis_result.get("prioritized_actions", [])[:6],
                    "implementation_timeline": {
                        "immediate": ["Upgrade to LED lighting", "Use public transport"],
                        "short_term": ["Install smart thermostat", "Reduce beef consumption"],
                        "medium_term": ["Install solar panels", "Purchase electric vehicle"],
                        "long_term": []
                    },
                    "expected_outcomes": {
                        "carbon_impact": {
                            "total_reduction": "8.5 tons CO2/year",
                            "percentage_reduction": "65%",
                            "global_impact": "Equivalent to planting 200 trees annually"
                        }
                    }
                },
                "final_eco_score": 72.5,
                "implementation_confidence": 0.8
            }
        else:
            return await self.evaluator.evaluate_and_finalize(evaluation_input)
    
    def _should_refine(self, synthesis_result: Dict[str, Any]) -> bool:
        """Determine if refinement is needed"""
        
        # Simple logic: refine if eco_score is below 60 or confidence is low
        eco_score = synthesis_result.get("eco_score", 50)
        confidence = synthesis_result.get("synthesis_confidence", 0.5)
        
        return eco_score < 60 or confidence < 0.7
    
    def _compile_final_results(self) -> Dict[str, Any]:
        """Compile final comprehensive results"""
        
        synthesis = self.workflow_state["synthesis_result"]
        evaluation = self.workflow_state["final_evaluation"]
        
        if not synthesis or not evaluation:
            return self._get_fallback_results()
        
        return {
            # Core metrics
            "eco_score": evaluation.get("final_eco_score", synthesis.get("eco_score", 25)),
            "total_carbon_footprint": synthesis.get("total_carbon_footprint", 13.0),
            "potential_reduction": evaluation.get("evaluation_results", {}).get("carbon_impact", {}).get("potential_reduction", 8.5),
            
            # Domain breakdown
            "domain_breakdown": synthesis.get("domain_breakdown", {}),
            
            # Action plan
            "prioritized_actions": evaluation.get("final_plan", {}).get("final_actions", synthesis.get("prioritized_actions", [])),
            "implementation_timeline": evaluation.get("final_plan", {}).get("implementation_timeline", {}),
            
            # Analysis details
            "synergies": synthesis.get("synergies", []),
            "impact_analysis": synthesis.get("impact_analysis", {}),
            
            # Workflow metadata
            "workflow_state": self.workflow_state,
            "analysis_timestamp": datetime.now().isoformat(),
            "session_id": self.workflow_state["session_id"]
        }
    
    def _get_fallback_results(self) -> Dict[str, Any]:
        """Fallback results if workflow fails"""
        
        return {
            "eco_score": 25,
            "total_carbon_footprint": 12.5,
            "potential_reduction": 6.0,
            "domain_breakdown": {
                "home": {"carbon_footprint": 3.0, "efficiency_score": 0.4},
                "transport": {"carbon_footprint": 5.5, "efficiency_score": 0.2},
                "diet": {"carbon_footprint": 2.5, "efficiency_score": 0.3},
                "shopping": {"carbon_footprint": 1.5, "efficiency_score": 0.4}
            },
            "prioritized_actions": [
                {
                    "action": "Switch to LED lighting throughout home",
                    "co2_reduction": "0.5 tons/year",
                    "feasibility": "high",
                    "cost_impact": "Low cost, immediate savings",
                    "domain": "home"
                },
                {
                    "action": "Use public transportation for daily commute",
                    "co2_reduction": "2.0 tons/year", 
                    "feasibility": "high",
                    "cost_impact": "Cost savings immediately",
                    "domain": "transport"
                },
                {
                    "action": "Reduce meat consumption by 50%",
                    "co2_reduction": "1.0 tons/year",
                    "feasibility": "medium",
                    "cost_impact": "Cost savings on groceries",
                    "domain": "diet"
                }
            ],
            "implementation_timeline": {
                "immediate": ["Switch to LED lighting"],
                "short_term": ["Use public transportation", "Reduce meat consumption"],
                "medium_term": [],
                "long_term": []
            },
            "workflow_state": self.workflow_state,
            "analysis_timestamp": datetime.now().isoformat(),
            "error": "Using fallback results due to workflow failure"
        }
    
    # Fallback analysis methods
    def _get_fallback_home_analysis(self) -> Dict[str, Any]:
        return {
            "agent_id": "home_expert_fallback",
            "carbon_footprint": 3.0,
            "efficiency_score": 0.4,
            "recommendations": [
                {
                    "action": "Install LED lighting",
                    "co2_reduction": "0.5 tons/year",
                    "priority": "high",
                    "cost_impact": "Low cost, quick savings"
                }
            ]
        }
    
    def _get_fallback_transport_analysis(self) -> Dict[str, Any]:
        return {
            "agent_id": "transport_expert_fallback", 
            "carbon_footprint": 5.5,
            "efficiency_score": 0.2,
            "recommendations": [
                {
                    "action": "Use public transportation",
                    "co2_reduction": "2.0 tons/year",
                    "priority": "high",
                    "cost_impact": "Cost savings"
                }
            ]
        }
    
    def _get_fallback_diet_analysis(self) -> Dict[str, Any]:
        return {
            "agent_id": "diet_expert_fallback",
            "carbon_footprint": 2.5,
            "efficiency_score": 0.3,
            "recommendations": [
                {
                    "action": "Reduce meat consumption",
                    "co2_reduction": "1.0 tons/year", 
                    "priority": "medium",
                    "cost_impact": "Cost savings"
                }
            ]
        }
    
    def _get_fallback_shopping_analysis(self) -> Dict[str, Any]:
        return {
            "agent_id": "shopping_expert_fallback",
            "carbon_footprint": 1.5,
            "efficiency_score": 0.4,
            "recommendations": [
                {
                    "action": "Buy second-hand items",
                    "co2_reduction": "0.3 tons/year",
                    "priority": "low", 
                    "cost_impact": "Cost savings"
                }
            ]
        }