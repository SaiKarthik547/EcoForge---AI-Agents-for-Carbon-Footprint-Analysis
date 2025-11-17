import asyncio
from typing import Dict, Any, List
import json
import numpy as np

class SynthesizerAgent:
    """CAPSTONE: Master Synthesis Agent for Multi-Domain Integration"""
    
    def __init__(self):
        self.agent_id = "synthesizer_master_005"
        self.domain_weights = {
            "home": 0.25,
            "transport": 0.35,
            "diet": 0.25,
            "shopping": 0.15
        }
    
    async def synthesize(self, agent_analyses: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """CAPSTONE: Cross-Domain Synthesis and Integration"""
        
        # Calculate total carbon footprint
        total_footprint = self._calculate_total_footprint(agent_analyses)
        
        # Identify synergistic opportunities
        synergies = self._identify_synergies(agent_analyses)
        
        # Prioritize interventions
        prioritized_actions = self._prioritize_interventions(agent_analyses, synergies)
        
        # Calculate potential impact
        impact_analysis = self._analyze_potential_impact(prioritized_actions)
        
        # Generate integrated recommendations
        integrated_plan = self._create_integrated_plan(prioritized_actions, synergies)
        
        # Calculate EcoScore
        eco_score = self._calculate_eco_score(agent_analyses, total_footprint)
        
        return {
            "agent_id": self.agent_id,
            "total_carbon_footprint": total_footprint,
            "domain_breakdown": self._get_domain_breakdown(agent_analyses),
            "synergies": synergies,
            "prioritized_actions": prioritized_actions,
            "impact_analysis": impact_analysis,
            "integrated_plan": integrated_plan,
            "eco_score": eco_score,
            "synthesis_confidence": self._calculate_synthesis_confidence(agent_analyses)
        }
    
    def _calculate_total_footprint(self, agent_analyses: Dict[str, Dict[str, Any]]) -> float:
        """Calculate total carbon footprint across all domains"""
        
        total = 0.0
        
        for domain, analysis in agent_analyses.items():
            footprint = analysis.get("carbon_footprint", 0.0)
            total += footprint
        
        return round(total, 2)
    
    def _get_domain_breakdown(self, agent_analyses: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Get detailed breakdown by domain"""
        
        breakdown = {}
        
        for domain, analysis in agent_analyses.items():
            breakdown[domain] = {
                "carbon_footprint": analysis.get("carbon_footprint", 0.0),
                "efficiency_score": analysis.get("efficiency_score", 0.5),
                "key_findings": analysis.get("key_findings", []),
                "improvement_potential": self._assess_improvement_potential(analysis)
            }
        
        return breakdown
    
    def _assess_improvement_potential(self, analysis: Dict[str, Any]) -> str:
        """Assess improvement potential for a domain"""
        
        efficiency = analysis.get("efficiency_score", 0.5)
        carbon_footprint = analysis.get("carbon_footprint", 0.0)
        
        if efficiency < 0.3 or carbon_footprint > 5:
            return "high"
        elif efficiency < 0.6 or carbon_footprint > 2:
            return "medium"
        else:
            return "low"
    
    def _identify_synergies(self, agent_analyses: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
        """CAPSTONE: Identify cross-domain synergistic opportunities"""
        
        synergies = []
        
        # Home-Transport synergy (EV + Solar)
        home_renewable = agent_analyses.get("home", {}).get("energy_patterns", {}).get("renewable_energy", False)
        transport_type = agent_analyses.get("transport", {}).get("transport_patterns", {}).get("primary_vehicle", "sedan")
        
        if not home_renewable and transport_type in ["sedan", "suv", "luxury_car"]:
            synergies.append({
                "type": "home_transport_ev_solar",
                "domains": ["home", "transport"],
                "description": "Solar panels + Electric vehicle combo",
                "synergy_multiplier": 1.5,
                "combined_impact": "Reduce both home and transport emissions by 80%+",
                "implementation_order": ["home_solar", "transport_ev"]
            })
        
        # Diet-Shopping synergy (Local food + Sustainable shopping)
        diet_local = agent_analyses.get("diet", {}).get("dietary_patterns", {}).get("organic_preference", False)
        shopping_second_hand = agent_analyses.get("shopping", {}).get("shopping_patterns", {}).get("second_hand_preference", False)
        
        if not diet_local or not shopping_second_hand:
            synergies.append({
                "type": "diet_shopping_local_circular",
                "domains": ["diet", "shopping"],
                "description": "Local food sourcing + Circular economy practices",
                "synergy_multiplier": 1.3,
                "combined_impact": "Reduce supply chain emissions across consumption",
                "implementation_order": ["local_food", "circular_shopping"]
            })
        
        # Transport-Shopping synergy (Reduced car dependency)
        transport_efficiency = agent_analyses.get("transport", {}).get("efficiency_score", 0.5)
        shopping_frequency = agent_analyses.get("shopping", {}).get("shopping_patterns", {}).get("shopping_frequency", "weekly")
        
        if transport_efficiency < 0.6 and shopping_frequency == "daily":
            synergies.append({
                "type": "transport_shopping_consolidation",
                "domains": ["transport", "shopping"],
                "description": "Consolidated shopping trips + Alternative transport",
                "synergy_multiplier": 1.4,
                "combined_impact": "Reduce transport needs and optimize shopping patterns",
                "implementation_order": ["consolidate_shopping", "alternative_transport"]
            })
        
        return synergies
    
    def _prioritize_interventions(self, agent_analyses: Dict[str, Dict[str, Any]], 
                                synergies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioritize interventions based on impact and feasibility"""
        
        all_interventions = []
        
        # Collect all recommendations from agents
        for domain, analysis in agent_analyses.items():
            recommendations = analysis.get("recommendations", [])
            
            for rec in recommendations:
                intervention = {
                    "domain": domain,
                    "action": rec.get("action", ""),
                    "impact": rec.get("impact", ""),
                    "priority": rec.get("priority", "medium"),
                    "co2_reduction": rec.get("co2_reduction", "0.5 tons/year"),
                    "cost_impact": rec.get("cost_impact", "Medium"),
                    "feasibility": self._assess_feasibility(rec),
                    "urgency": self._assess_urgency(analysis, rec)
                }
                all_interventions.append(intervention)
        
        # Add synergistic interventions
        for synergy in synergies:
            intervention = {
                "domain": "cross_domain",
                "action": synergy["description"],
                "impact": synergy["combined_impact"],
                "priority": "high",
                "co2_reduction": "5-15 tons/year",
                "cost_impact": "High initial, excellent ROI",
                "feasibility": "medium",
                "urgency": "high",
                "synergy_multiplier": synergy["synergy_multiplier"]
            }
            all_interventions.append(intervention)
        
        # Sort by priority score
        prioritized = sorted(all_interventions, key=self._calculate_priority_score, reverse=True)
        
        return prioritized[:8]  # Top 8 interventions
    
    def _assess_feasibility(self, recommendation: Dict[str, Any]) -> str:
        """Assess feasibility of a recommendation"""
        
        cost = recommendation.get("cost_impact", "Medium").lower()
        
        if "low" in cost or "savings" in cost:
            return "high"
        elif "medium" in cost:
            return "medium"
        else:
            return "low"
    
    def _assess_urgency(self, analysis: Dict[str, Any], recommendation: Dict[str, Any]) -> str:
        """Assess urgency of intervention"""
        
        carbon_footprint = analysis.get("carbon_footprint", 0.0)
        priority = recommendation.get("priority", "medium")
        
        if carbon_footprint > 5 and priority == "high":
            return "critical"
        elif carbon_footprint > 2 or priority == "high":
            return "high"
        else:
            return "medium"
    
    def _calculate_priority_score(self, intervention: Dict[str, Any]) -> float:
        """Calculate priority score for sorting"""
        
        priority_scores = {"critical": 5, "high": 4, "medium": 3, "low": 2}
        feasibility_scores = {"high": 3, "medium": 2, "low": 1}
        urgency_scores = {"critical": 4, "high": 3, "medium": 2, "low": 1}
        
        priority = priority_scores.get(intervention.get("priority", "medium"), 3)
        feasibility = feasibility_scores.get(intervention.get("feasibility", "medium"), 2)
        urgency = urgency_scores.get(intervention.get("urgency", "medium"), 2)
        
        # Synergy bonus
        synergy_bonus = intervention.get("synergy_multiplier", 1.0)
        
        return (priority * 0.4 + feasibility * 0.3 + urgency * 0.3) * synergy_bonus
    
    def _analyze_potential_impact(self, prioritized_actions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze potential impact of interventions"""
        
        total_potential_reduction = 0.0
        implementation_timeline = {}
        
        for i, action in enumerate(prioritized_actions):
            # Extract CO2 reduction (simplified parsing)
            co2_text = action.get("co2_reduction", "0.5 tons/year")
            try:
                # Extract number from text like "2-4 tons/year"
                import re
                numbers = re.findall(r'(\d+(?:\.\d+)?)', co2_text)
                if numbers:
                    reduction = float(numbers[-1])  # Take the higher estimate
                    total_potential_reduction += reduction
            except:
                total_potential_reduction += 1.0  # Default estimate
            
            # Timeline estimation
            urgency = action.get("urgency", "medium")
            timeline_map = {"critical": "0-3 months", "high": "3-6 months", "medium": "6-12 months", "low": "12+ months"}
            implementation_timeline[action["action"]] = timeline_map.get(urgency, "6-12 months")
        
        return {
            "total_potential_reduction": round(total_potential_reduction, 1),
            "implementation_timeline": implementation_timeline,
            "quick_wins": [a for a in prioritized_actions if a.get("feasibility") == "high"][:3],
            "high_impact_projects": [a for a in prioritized_actions if "high" in a.get("co2_reduction", "")][:3]
        }
    
    def _create_integrated_plan(self, prioritized_actions: List[Dict[str, Any]], 
                              synergies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create integrated implementation plan"""
        
        plan = {
            "phase_1_immediate": [],
            "phase_2_short_term": [],
            "phase_3_long_term": [],
            "synergy_clusters": []
        }
        
        # Categorize actions by timeline
        for action in prioritized_actions:
            urgency = action.get("urgency", "medium")
            feasibility = action.get("feasibility", "medium")
            
            if urgency in ["critical", "high"] and feasibility == "high":
                plan["phase_1_immediate"].append(action)
            elif urgency in ["high", "medium"]:
                plan["phase_2_short_term"].append(action)
            else:
                plan["phase_3_long_term"].append(action)
        
        # Group synergistic actions
        for synergy in synergies:
            cluster = {
                "synergy_type": synergy["type"],
                "description": synergy["description"],
                "domains": synergy["domains"],
                "implementation_order": synergy["implementation_order"],
                "combined_impact": synergy["combined_impact"]
            }
            plan["synergy_clusters"].append(cluster)
        
        return plan
    
    def _calculate_eco_score(self, agent_analyses: Dict[str, Dict[str, Any]], 
                           total_footprint: float) -> float:
        """Calculate overall EcoScore (0-100)"""
        
        # Base score from carbon footprint (inverted)
        global_average_footprint = 4.8  # tons CO2/year
        footprint_score = max(0, 100 - (total_footprint / global_average_footprint * 50))
        
        # Efficiency scores from each domain
        efficiency_scores = []
        for domain, analysis in agent_analyses.items():
            efficiency = analysis.get("efficiency_score", 0.5)
            weight = self.domain_weights.get(domain, 0.25)
            efficiency_scores.append(efficiency * weight * 100)
        
        avg_efficiency_score = sum(efficiency_scores)
        
        # Combine scores (60% efficiency, 40% absolute footprint)
        eco_score = (avg_efficiency_score * 0.6) + (footprint_score * 0.4)
        
        return round(min(100, max(0, eco_score)), 1)
    
    def _calculate_synthesis_confidence(self, agent_analyses: Dict[str, Dict[str, Any]]) -> float:
        """Calculate confidence in synthesis quality"""
        
        confidence_factors = []
        
        # Data completeness
        complete_analyses = len([a for a in agent_analyses.values() if a.get("carbon_footprint", 0) > 0])
        completeness_score = complete_analyses / 4.0  # 4 domains
        confidence_factors.append(completeness_score)
        
        # Consistency across domains
        efficiency_scores = [a.get("efficiency_score", 0.5) for a in agent_analyses.values()]
        consistency_score = 1.0 - (np.std(efficiency_scores) if len(efficiency_scores) > 1 else 0)
        confidence_factors.append(consistency_score)
        
        # Key findings availability
        findings_score = len([a for a in agent_analyses.values() if a.get("key_findings")]) / 4.0
        confidence_factors.append(findings_score)
        
        return round(sum(confidence_factors) / len(confidence_factors), 2)