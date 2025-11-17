import asyncio
from typing import Dict, Any, List
import json

class RefinerLoopAgent:
    """CAPSTONE: Iterative Refinement Loop Agent with Quality Optimization"""
    
    def __init__(self):
        self.agent_id = "refiner_loop_006"
        self.refinement_criteria = [
            "feasibility_optimization",
            "cost_effectiveness",
            "implementation_sequencing",
            "user_preference_alignment",
            "impact_maximization"
        ]
    
    async def refine_plan(self, synthesis: Dict[str, Any], 
                         previous_refinements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """CAPSTONE: Iterative Plan Refinement with Learning"""
        
        iteration_number = len(previous_refinements) + 1
        
        # Analyze current plan quality
        quality_assessment = self._assess_plan_quality(synthesis)
        
        # Identify refinement opportunities
        refinement_opportunities = self._identify_refinement_opportunities(
            synthesis, previous_refinements, quality_assessment
        )
        
        # Apply refinements
        refined_plan = self._apply_refinements(synthesis, refinement_opportunities)
        
        # Validate improvements
        improvement_validation = self._validate_improvements(synthesis, refined_plan)
        
        # Learn from previous iterations
        learning_insights = self._extract_learning_insights(previous_refinements, refined_plan)
        
        return {
            "iteration": iteration_number,
            "quality_assessment": quality_assessment,
            "refinement_opportunities": refinement_opportunities,
            "refined_plan": refined_plan,
            "improvement_validation": improvement_validation,
            "learning_insights": learning_insights,
            "quality_score": self._calculate_quality_score(refined_plan),
            "refinement_confidence": self._calculate_refinement_confidence(improvement_validation)
        }
    
    def _assess_plan_quality(self, synthesis: Dict[str, Any]) -> Dict[str, Any]:
        """Assess current plan quality across multiple dimensions"""
        
        assessment = {
            "feasibility_score": 0.0,
            "impact_score": 0.0,
            "cost_effectiveness": 0.0,
            "implementation_clarity": 0.0,
            "user_alignment": 0.0
        }
        
        prioritized_actions = synthesis.get("prioritized_actions", [])
        
        if prioritized_actions:
            # Feasibility assessment
            feasibility_scores = {"high": 1.0, "medium": 0.6, "low": 0.3}
            feasibilities = [feasibility_scores.get(action.get("feasibility", "medium"), 0.6) 
                           for action in prioritized_actions]
            assessment["feasibility_score"] = sum(feasibilities) / len(feasibilities)
            
            # Impact assessment
            high_impact_count = len([a for a in prioritized_actions if "high" in a.get("co2_reduction", "")])
            assessment["impact_score"] = min(1.0, high_impact_count / max(len(prioritized_actions), 1))
            
            # Cost effectiveness
            cost_effective_count = len([a for a in prioritized_actions 
                                     if "savings" in a.get("cost_impact", "").lower() or 
                                        "low" in a.get("cost_impact", "").lower()])
            assessment["cost_effectiveness"] = cost_effective_count / max(len(prioritized_actions), 1)
            
            # Implementation clarity
            clear_actions = len([a for a in prioritized_actions if len(a.get("action", "")) > 20])
            assessment["implementation_clarity"] = clear_actions / max(len(prioritized_actions), 1)
            
            # User alignment (based on urgency and feasibility balance)
            balanced_actions = len([a for a in prioritized_actions 
                                  if a.get("feasibility") == "high" and a.get("urgency") != "low"])
            assessment["user_alignment"] = balanced_actions / max(len(prioritized_actions), 1)
        
        return assessment
    
    def _identify_refinement_opportunities(self, synthesis: Dict[str, Any], 
                                         previous_refinements: List[Dict[str, Any]],
                                         quality_assessment: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify specific refinement opportunities"""
        
        opportunities = []
        
        # Low feasibility refinement
        if quality_assessment["feasibility_score"] < 0.7:
            opportunities.append({
                "type": "feasibility_improvement",
                "description": "Increase feasibility by breaking down complex actions",
                "target_actions": self._find_low_feasibility_actions(synthesis),
                "refinement_strategy": "decomposition_and_phasing"
            })
        
        # Cost optimization
        if quality_assessment["cost_effectiveness"] < 0.6:
            opportunities.append({
                "type": "cost_optimization",
                "description": "Prioritize cost-effective interventions",
                "target_actions": self._find_high_cost_actions(synthesis),
                "refinement_strategy": "cost_benefit_reordering"
            })
        
        # Implementation sequencing
        if quality_assessment["implementation_clarity"] < 0.8:
            opportunities.append({
                "type": "sequencing_optimization",
                "description": "Improve implementation sequencing and dependencies",
                "target_actions": synthesis.get("prioritized_actions", []),
                "refinement_strategy": "dependency_analysis"
            })
        
        # Impact maximization
        if quality_assessment["impact_score"] < 0.5:
            opportunities.append({
                "type": "impact_maximization",
                "description": "Focus on highest-impact interventions first",
                "target_actions": self._find_low_impact_actions(synthesis),
                "refinement_strategy": "impact_prioritization"
            })
        
        # Learn from previous iterations
        if previous_refinements:
            recurring_issues = self._identify_recurring_issues(previous_refinements)
            for issue in recurring_issues:
                opportunities.append({
                    "type": "recurring_issue_resolution",
                    "description": f"Address recurring issue: {issue}",
                    "target_actions": [],
                    "refinement_strategy": "adaptive_learning"
                })
        
        return opportunities
    
    def _find_low_feasibility_actions(self, synthesis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find actions with low feasibility scores"""
        
        actions = synthesis.get("prioritized_actions", [])
        return [action for action in actions if action.get("feasibility") == "low"]
    
    def _find_high_cost_actions(self, synthesis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find actions with high cost impact"""
        
        actions = synthesis.get("prioritized_actions", [])
        return [action for action in actions if "high" in action.get("cost_impact", "").lower()]
    
    def _find_low_impact_actions(self, synthesis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find actions with low carbon impact"""
        
        actions = synthesis.get("prioritized_actions", [])
        return [action for action in actions if not any(char.isdigit() for char in action.get("co2_reduction", ""))]
    
    def _identify_recurring_issues(self, previous_refinements: List[Dict[str, Any]]) -> List[str]:
        """Identify issues that keep appearing across iterations"""
        
        issue_counts = {}
        
        for refinement in previous_refinements:
            opportunities = refinement.get("refinement_opportunities", [])
            for opp in opportunities:
                issue_type = opp.get("type", "unknown")
                issue_counts[issue_type] = issue_counts.get(issue_type, 0) + 1
        
        # Return issues that appear in multiple iterations
        recurring = [issue for issue, count in issue_counts.items() if count > 1]
        return recurring
    
    def _apply_refinements(self, synthesis: Dict[str, Any], 
                          refinement_opportunities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Apply identified refinements to the plan"""
        
        refined_plan = synthesis.copy()
        
        for opportunity in refinement_opportunities:
            strategy = opportunity.get("refinement_strategy", "")
            
            if strategy == "decomposition_and_phasing":
                refined_plan = self._apply_decomposition_refinement(refined_plan, opportunity)
            
            elif strategy == "cost_benefit_reordering":
                refined_plan = self._apply_cost_optimization_refinement(refined_plan, opportunity)
            
            elif strategy == "dependency_analysis":
                refined_plan = self._apply_sequencing_refinement(refined_plan, opportunity)
            
            elif strategy == "impact_prioritization":
                refined_plan = self._apply_impact_refinement(refined_plan, opportunity)
            
            elif strategy == "adaptive_learning":
                refined_plan = self._apply_learning_refinement(refined_plan, opportunity)
        
        return refined_plan
    
    def _apply_decomposition_refinement(self, plan: Dict[str, Any], 
                                      opportunity: Dict[str, Any]) -> Dict[str, Any]:
        """Break down complex actions into smaller, more feasible steps"""
        
        target_actions = opportunity.get("target_actions", [])
        refined_actions = []
        
        for action in plan.get("prioritized_actions", []):
            if action in target_actions:
                # Decompose complex action
                sub_actions = self._decompose_action(action)
                refined_actions.extend(sub_actions)
            else:
                refined_actions.append(action)
        
        plan["prioritized_actions"] = refined_actions
        return plan
    
    def _decompose_action(self, action: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Decompose a complex action into sub-actions"""
        
        main_action = action.get("action", "")
        
        # Simple decomposition logic
        if "solar panels" in main_action.lower():
            return [
                {**action, "action": "Get solar panel quotes and assessments", "feasibility": "high"},
                {**action, "action": "Apply for solar installation permits", "feasibility": "high"},
                {**action, "action": "Install solar panel system", "feasibility": "medium"}
            ]
        elif "electric vehicle" in main_action.lower():
            return [
                {**action, "action": "Research EV models and test drive", "feasibility": "high"},
                {**action, "action": "Install home charging station", "feasibility": "medium"},
                {**action, "action": "Purchase electric vehicle", "feasibility": "medium"}
            ]
        else:
            # Default: split into planning and execution
            return [
                {**action, "action": f"Plan: {main_action}", "feasibility": "high"},
                {**action, "action": f"Execute: {main_action}", "feasibility": action.get("feasibility", "medium")}
            ]
    
    def _apply_cost_optimization_refinement(self, plan: Dict[str, Any], 
                                          opportunity: Dict[str, Any]) -> Dict[str, Any]:
        """Reorder actions based on cost-effectiveness"""
        
        actions = plan.get("prioritized_actions", [])
        
        # Sort by cost-effectiveness (prioritize low cost, high impact)
        def cost_effectiveness_score(action):
            cost = action.get("cost_impact", "medium").lower()
            co2_reduction = action.get("co2_reduction", "0.5")
            
            cost_score = {"low": 3, "medium": 2, "high": 1, "savings": 4}.get(
                next((k for k in ["low", "medium", "high", "savings"] if k in cost), "medium"), 2
            )
            
            # Extract impact number
            try:
                import re
                numbers = re.findall(r'(\d+(?:\.\d+)?)', co2_reduction)
                impact_score = float(numbers[-1]) if numbers else 1.0
            except:
                impact_score = 1.0
            
            return cost_score * impact_score
        
        sorted_actions = sorted(actions, key=cost_effectiveness_score, reverse=True)
        plan["prioritized_actions"] = sorted_actions
        
        return plan
    
    def _apply_sequencing_refinement(self, plan: Dict[str, Any], 
                                   opportunity: Dict[str, Any]) -> Dict[str, Any]:
        """Improve implementation sequencing based on dependencies"""
        
        actions = plan.get("prioritized_actions", [])
        
        # Simple dependency logic
        sequenced_actions = []
        
        # Foundation actions first (home improvements, basic changes)
        foundation_keywords = ["insulation", "led", "thermostat", "bike", "walk"]
        foundation_actions = [a for a in actions if any(kw in a.get("action", "").lower() for kw in foundation_keywords)]
        
        # Major investments second (solar, EV, heat pump)
        major_keywords = ["solar", "electric vehicle", "heat pump", "ev"]
        major_actions = [a for a in actions if any(kw in a.get("action", "").lower() for kw in major_keywords)]
        
        # Lifestyle changes third (diet, shopping)
        lifestyle_keywords = ["meat", "diet", "shopping", "local", "second"]
        lifestyle_actions = [a for a in actions if any(kw in a.get("action", "").lower() for kw in lifestyle_keywords)]
        
        # Other actions
        other_actions = [a for a in actions if a not in foundation_actions + major_actions + lifestyle_actions]
        
        sequenced_actions = foundation_actions + major_actions + lifestyle_actions + other_actions
        plan["prioritized_actions"] = sequenced_actions
        
        return plan
    
    def _apply_impact_refinement(self, plan: Dict[str, Any], 
                               opportunity: Dict[str, Any]) -> Dict[str, Any]:
        """Prioritize highest-impact interventions"""
        
        actions = plan.get("prioritized_actions", [])
        
        # Sort by CO2 reduction potential
        def impact_score(action):
            co2_text = action.get("co2_reduction", "0.5")
            try:
                import re
                numbers = re.findall(r'(\d+(?:\.\d+)?)', co2_text)
                return float(numbers[-1]) if numbers else 0.5
            except:
                return 0.5
        
        sorted_actions = sorted(actions, key=impact_score, reverse=True)
        plan["prioritized_actions"] = sorted_actions[:6]  # Keep top 6 highest impact
        
        return plan
    
    def _apply_learning_refinement(self, plan: Dict[str, Any], 
                                 opportunity: Dict[str, Any]) -> Dict[str, Any]:
        """Apply learning from previous iterations"""
        
        # Adaptive refinement based on recurring issues
        # This is a simplified implementation
        
        actions = plan.get("prioritized_actions", [])
        
        # Add implementation tips based on learning
        for action in actions:
            if not action.get("implementation_tips"):
                action["implementation_tips"] = self._generate_implementation_tips(action)
        
        plan["prioritized_actions"] = actions
        return plan
    
    def _generate_implementation_tips(self, action: Dict[str, Any]) -> List[str]:
        """Generate implementation tips for an action"""
        
        action_text = action.get("action", "").lower()
        tips = []
        
        if "solar" in action_text:
            tips = [
                "Get multiple quotes from certified installers",
                "Check local incentives and tax credits",
                "Ensure roof condition is suitable for installation"
            ]
        elif "electric" in action_text:
            tips = [
                "Test drive multiple EV models",
                "Plan charging infrastructure first",
                "Consider total cost of ownership"
            ]
        elif "diet" in action_text or "meat" in action_text:
            tips = [
                "Start with one plant-based day per week",
                "Find tasty plant-based recipes",
                "Ensure nutritional balance"
            ]
        else:
            tips = [
                "Start with small, manageable steps",
                "Track progress regularly",
                "Celebrate small wins"
            ]
        
        return tips
    
    def _validate_improvements(self, original: Dict[str, Any], 
                             refined: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that refinements actually improve the plan"""
        
        original_quality = self._assess_plan_quality(original)
        refined_quality = self._assess_plan_quality(refined)
        
        improvements = {}
        for metric, refined_score in refined_quality.items():
            original_score = original_quality.get(metric, 0.0)
            improvement = refined_score - original_score
            improvements[metric] = {
                "original": original_score,
                "refined": refined_score,
                "improvement": improvement,
                "improved": improvement > 0
            }
        
        overall_improvement = sum(imp["improvement"] for imp in improvements.values()) / len(improvements)
        
        return {
            "metric_improvements": improvements,
            "overall_improvement": overall_improvement,
            "validation_passed": overall_improvement > 0,
            "significant_improvement": overall_improvement > 0.1
        }
    
    def _extract_learning_insights(self, previous_refinements: List[Dict[str, Any]], 
                                 current_refinement: Dict[str, Any]) -> List[str]:
        """Extract learning insights from refinement history"""
        
        insights = []
        
        # Analyze improvement trends
        if len(previous_refinements) >= 2:
            recent_improvements = [r.get("improvement_validation", {}).get("overall_improvement", 0) 
                                 for r in previous_refinements[-2:]]
            
            if all(imp > 0 for imp in recent_improvements):
                insights.append("Consistent improvement pattern - refinement strategy is effective")
            elif all(imp <= 0 for imp in recent_improvements):
                insights.append("Diminishing returns - consider alternative refinement approaches")
        
        # Identify successful strategies
        current_improvement = current_refinement.get("improvement_validation", {}).get("overall_improvement", 0)
        if current_improvement > 0.1:
            opportunities = current_refinement.get("refinement_opportunities", [])
            successful_strategies = [opp.get("refinement_strategy") for opp in opportunities]
            insights.append(f"Successful strategies: {', '.join(successful_strategies)}")
        
        # Quality threshold insights
        quality_score = current_refinement.get("quality_score", 0.5)
        if quality_score > 0.8:
            insights.append("High quality plan achieved - minimal further refinement needed")
        elif quality_score < 0.5:
            insights.append("Plan quality below threshold - significant refinement still needed")
        
        return insights
    
    def _calculate_quality_score(self, plan: Dict[str, Any]) -> float:
        """Calculate overall quality score for the plan"""
        
        quality_assessment = self._assess_plan_quality(plan)
        
        # Weighted average of quality metrics
        weights = {
            "feasibility_score": 0.25,
            "impact_score": 0.30,
            "cost_effectiveness": 0.20,
            "implementation_clarity": 0.15,
            "user_alignment": 0.10
        }
        
        weighted_score = sum(quality_assessment.get(metric, 0.5) * weight 
                           for metric, weight in weights.items())
        
        return round(weighted_score, 3)
    
    def _calculate_refinement_confidence(self, improvement_validation: Dict[str, Any]) -> float:
        """Calculate confidence in refinement quality"""
        
        if not improvement_validation.get("validation_passed", False):
            return 0.3  # Low confidence if validation failed
        
        overall_improvement = improvement_validation.get("overall_improvement", 0.0)
        
        if overall_improvement > 0.2:
            return 0.9  # High confidence for significant improvement
        elif overall_improvement > 0.1:
            return 0.7  # Medium-high confidence
        elif overall_improvement > 0.0:
            return 0.5  # Medium confidence
        else:
            return 0.3  # Low confidence