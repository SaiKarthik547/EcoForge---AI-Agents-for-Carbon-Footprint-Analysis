import asyncio
from typing import Dict, Any, List
import json

class EvaluatorAgent:
    """CAPSTONE: Final Evaluation and Plan Validation Agent"""
    
    def __init__(self):
        self.agent_id = "evaluator_final_007"
        self.evaluation_criteria = [
            "carbon_impact_potential",
            "implementation_feasibility", 
            "cost_benefit_ratio",
            "user_experience_quality",
            "long_term_sustainability"
        ]
    
    async def evaluate_and_finalize(self, evaluation_input: Dict[str, Any]) -> Dict[str, Any]:
        """CAPSTONE: Comprehensive Final Evaluation and Plan Finalization"""
        
        synthesis = evaluation_input.get("synthesis", {})
        refinements = evaluation_input.get("refinements", [])
        user_input = evaluation_input.get("user_input", "")
        
        # Comprehensive evaluation
        evaluation_results = self._comprehensive_evaluation(synthesis, refinements)
        
        # Plan validation
        validation_results = self._validate_final_plan(synthesis, refinements)
        
        # User alignment assessment
        user_alignment = self._assess_user_alignment(synthesis, user_input)
        
        # Risk assessment
        risk_analysis = self._analyze_implementation_risks(synthesis, refinements)
        
        # Success metrics definition
        success_metrics = self._define_success_metrics(synthesis)
        
        # Final plan generation
        final_plan = self._generate_final_plan(
            synthesis, refinements, evaluation_results, validation_results
        )
        
        # Calculate final EcoScore
        final_eco_score = self._calculate_final_eco_score(
            synthesis, evaluation_results, user_alignment
        )
        
        return {
            "agent_id": self.agent_id,
            "evaluation_results": evaluation_results,
            "validation_results": validation_results,
            "user_alignment": user_alignment,
            "risk_analysis": risk_analysis,
            "success_metrics": success_metrics,
            "final_plan": final_plan,
            "final_eco_score": final_eco_score,
            "implementation_confidence": self._calculate_implementation_confidence(validation_results),
            "recommendations_summary": self._create_recommendations_summary(final_plan)
        }
    
    def _comprehensive_evaluation(self, synthesis: Dict[str, Any], 
                                refinements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform comprehensive evaluation across all criteria"""
        
        evaluation = {}
        
        # Carbon impact evaluation
        evaluation["carbon_impact"] = self._evaluate_carbon_impact(synthesis)
        
        # Feasibility evaluation
        evaluation["feasibility"] = self._evaluate_feasibility(synthesis, refinements)
        
        # Cost-benefit evaluation
        evaluation["cost_benefit"] = self._evaluate_cost_benefit(synthesis)
        
        # User experience evaluation
        evaluation["user_experience"] = self._evaluate_user_experience(synthesis, refinements)
        
        # Sustainability evaluation
        evaluation["sustainability"] = self._evaluate_sustainability(synthesis)
        
        # Overall evaluation score
        evaluation["overall_score"] = self._calculate_overall_evaluation_score(evaluation)
        
        return evaluation
    
    def _evaluate_carbon_impact(self, synthesis: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate potential carbon impact"""
        
        total_footprint = synthesis.get("total_carbon_footprint", 0.0)
        impact_analysis = synthesis.get("impact_analysis", {})
        potential_reduction = impact_analysis.get("total_potential_reduction", 0.0)
        
        # Calculate impact metrics
        reduction_percentage = (potential_reduction / max(total_footprint, 1)) * 100
        
        impact_score = min(1.0, reduction_percentage / 70)  # 70% reduction = perfect score
        
        return {
            "current_footprint": total_footprint,
            "potential_reduction": potential_reduction,
            "reduction_percentage": round(reduction_percentage, 1),
            "impact_score": round(impact_score, 2),
            "impact_category": self._categorize_impact(reduction_percentage),
            "global_comparison": self._compare_to_global_average(total_footprint)
        }
    
    def _categorize_impact(self, reduction_percentage: float) -> str:
        """Categorize impact level"""
        
        if reduction_percentage >= 70:
            return "transformational"
        elif reduction_percentage >= 50:
            return "substantial"
        elif reduction_percentage >= 30:
            return "significant"
        elif reduction_percentage >= 15:
            return "moderate"
        else:
            return "minimal"
    
    def _compare_to_global_average(self, footprint: float) -> Dict[str, Any]:
        """Compare footprint to global averages"""
        
        global_average = 4.8  # tons CO2/year
        paris_target = 2.3    # tons CO2/year for 1.5°C target
        
        return {
            "vs_global_average": round((footprint / global_average - 1) * 100, 1),
            "vs_paris_target": round((footprint / paris_target - 1) * 100, 1),
            "alignment_status": "aligned" if footprint <= paris_target else "above_target"
        }
    
    def _evaluate_feasibility(self, synthesis: Dict[str, Any], 
                            refinements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluate implementation feasibility"""
        
        actions = synthesis.get("prioritized_actions", [])
        
        # Feasibility distribution
        feasibility_counts = {"high": 0, "medium": 0, "low": 0}
        for action in actions:
            feasibility = action.get("feasibility", "medium")
            feasibility_counts[feasibility] += 1
        
        total_actions = len(actions)
        feasibility_score = (
            feasibility_counts["high"] * 1.0 + 
            feasibility_counts["medium"] * 0.6 + 
            feasibility_counts["low"] * 0.2
        ) / max(total_actions, 1)
        
        # Refinement impact on feasibility
        refinement_improvement = 0.0
        if refinements:
            latest_refinement = refinements[-1]
            validation = latest_refinement.get("improvement_validation", {})
            feasibility_improvement = validation.get("metric_improvements", {}).get("feasibility_score", {})
            refinement_improvement = feasibility_improvement.get("improvement", 0.0)
        
        return {
            "feasibility_score": round(feasibility_score, 2),
            "feasibility_distribution": feasibility_counts,
            "refinement_improvement": round(refinement_improvement, 2),
            "implementation_barriers": self._identify_implementation_barriers(actions),
            "feasibility_category": self._categorize_feasibility(feasibility_score)
        }
    
    def _categorize_feasibility(self, score: float) -> str:
        """Categorize feasibility level"""
        
        if score >= 0.8:
            return "highly_feasible"
        elif score >= 0.6:
            return "moderately_feasible"
        elif score >= 0.4:
            return "challenging"
        else:
            return "difficult"
    
    def _identify_implementation_barriers(self, actions: List[Dict[str, Any]]) -> List[str]:
        """Identify potential implementation barriers"""
        
        barriers = []
        
        # High cost barriers
        high_cost_actions = [a for a in actions if "high" in a.get("cost_impact", "").lower()]
        if len(high_cost_actions) > len(actions) * 0.5:
            barriers.append("High upfront costs for majority of interventions")
        
        # Low feasibility barriers
        low_feasibility_actions = [a for a in actions if a.get("feasibility") == "low"]
        if low_feasibility_actions:
            barriers.append(f"{len(low_feasibility_actions)} interventions have low feasibility")
        
        # Complexity barriers
        complex_actions = [a for a in actions if len(a.get("action", "")) > 50]
        if len(complex_actions) > 3:
            barriers.append("Multiple complex interventions may overwhelm implementation")
        
        return barriers
    
    def _evaluate_cost_benefit(self, synthesis: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate cost-benefit ratio"""
        
        actions = synthesis.get("prioritized_actions", [])
        
        # Cost distribution analysis
        cost_categories = {"low": 0, "medium": 0, "high": 0, "savings": 0}
        for action in actions:
            cost_impact = action.get("cost_impact", "medium").lower()
            
            if "savings" in cost_impact or "low" in cost_impact:
                cost_categories["low"] += 1
            elif "high" in cost_impact:
                cost_categories["high"] += 1
            else:
                cost_categories["medium"] += 1
        
        # Cost-benefit score
        total_actions = len(actions)
        cost_benefit_score = (
            cost_categories["low"] * 1.0 + 
            cost_categories["medium"] * 0.6 + 
            cost_categories["high"] * 0.3
        ) / max(total_actions, 1)
        
        # ROI estimation
        roi_estimate = self._estimate_roi(actions)
        
        return {
            "cost_benefit_score": round(cost_benefit_score, 2),
            "cost_distribution": cost_categories,
            "roi_estimate": roi_estimate,
            "payback_period": self._estimate_payback_period(actions),
            "cost_category": self._categorize_cost_benefit(cost_benefit_score)
        }
    
    def _estimate_roi(self, actions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Estimate return on investment"""
        
        # Simplified ROI calculation based on energy savings and carbon pricing
        carbon_price_per_ton = 50  # USD, approximate social cost of carbon
        
        total_co2_reduction = 0.0
        for action in actions:
            co2_text = action.get("co2_reduction", "0.5")
            try:
                import re
                numbers = re.findall(r'(\d+(?:\.\d+)?)', co2_text)
                if numbers:
                    total_co2_reduction += float(numbers[-1])
            except:
                total_co2_reduction += 0.5
        
        annual_carbon_value = total_co2_reduction * carbon_price_per_ton
        
        return {
            "annual_carbon_value": round(annual_carbon_value, 0),
            "ten_year_value": round(annual_carbon_value * 10, 0),
            "roi_category": "positive" if annual_carbon_value > 1000 else "moderate"
        }
    
    def _estimate_payback_period(self, actions: List[Dict[str, Any]]) -> str:
        """Estimate overall payback period"""
        
        high_cost_count = len([a for a in actions if "high" in a.get("cost_impact", "").lower()])
        savings_count = len([a for a in actions if "savings" in a.get("cost_impact", "").lower()])
        
        if savings_count > high_cost_count:
            return "1-3 years"
        elif high_cost_count <= 2:
            return "3-7 years"
        else:
            return "7-15 years"
    
    def _categorize_cost_benefit(self, score: float) -> str:
        """Categorize cost-benefit level"""
        
        if score >= 0.8:
            return "excellent"
        elif score >= 0.6:
            return "good"
        elif score >= 0.4:
            return "fair"
        else:
            return "poor"
    
    def _evaluate_user_experience(self, synthesis: Dict[str, Any], 
                                refinements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Evaluate user experience quality"""
        
        actions = synthesis.get("prioritized_actions", [])
        
        # Complexity assessment
        complexity_score = self._assess_complexity(actions)
        
        # Clarity assessment
        clarity_score = self._assess_clarity(actions, refinements)
        
        # Motivation assessment
        motivation_score = self._assess_motivation_potential(actions)
        
        # Overall UX score
        ux_score = (complexity_score + clarity_score + motivation_score) / 3
        
        return {
            "ux_score": round(ux_score, 2),
            "complexity_score": round(complexity_score, 2),
            "clarity_score": round(clarity_score, 2),
            "motivation_score": round(motivation_score, 2),
            "ux_category": self._categorize_ux(ux_score),
            "user_journey_quality": self._assess_user_journey(actions)
        }
    
    def _assess_complexity(self, actions: List[Dict[str, Any]]) -> float:
        """Assess complexity from user perspective"""
        
        # Simple actions get higher scores
        simple_keywords = ["led", "thermostat", "bike", "walk", "reduce", "choose"]
        complex_keywords = ["install", "upgrade", "system", "panels", "pump"]
        
        simple_count = 0
        complex_count = 0
        
        for action in actions:
            action_text = action.get("action", "").lower()
            if any(kw in action_text for kw in simple_keywords):
                simple_count += 1
            elif any(kw in action_text for kw in complex_keywords):
                complex_count += 1
        
        total_actions = len(actions)
        complexity_score = (simple_count * 1.0 + (total_actions - simple_count - complex_count) * 0.6 + complex_count * 0.3) / max(total_actions, 1)
        
        return complexity_score
    
    def _assess_clarity(self, actions: List[Dict[str, Any]], 
                       refinements: List[Dict[str, Any]]) -> float:
        """Assess clarity of instructions"""
        
        # Check if actions have implementation tips (from refinements)
        actions_with_tips = 0
        clear_actions = 0
        
        for action in actions:
            if action.get("implementation_tips"):
                actions_with_tips += 1
            
            if len(action.get("action", "")) > 20:  # Detailed description
                clear_actions += 1
        
        total_actions = len(actions)
        clarity_score = (actions_with_tips * 0.5 + clear_actions * 0.5) / max(total_actions, 1)
        
        return min(1.0, clarity_score)
    
    def _assess_motivation_potential(self, actions: List[Dict[str, Any]]) -> float:
        """Assess potential to motivate user"""
        
        # Quick wins and high impact actions are more motivating
        quick_wins = len([a for a in actions if a.get("feasibility") == "high"])
        high_impact = len([a for a in actions if "high" in a.get("co2_reduction", "")])
        cost_savings = len([a for a in actions if "savings" in a.get("cost_impact", "")])
        
        total_actions = len(actions)
        motivation_score = (quick_wins * 0.4 + high_impact * 0.4 + cost_savings * 0.2) / max(total_actions, 1)
        
        return min(1.0, motivation_score)
    
    def _categorize_ux(self, score: float) -> str:
        """Categorize user experience quality"""
        
        if score >= 0.8:
            return "excellent"
        elif score >= 0.6:
            return "good"
        elif score >= 0.4:
            return "fair"
        else:
            return "poor"
    
    def _assess_user_journey(self, actions: List[Dict[str, Any]]) -> str:
        """Assess overall user journey quality"""
        
        # Check for good progression from easy to complex
        feasibilities = [a.get("feasibility", "medium") for a in actions[:5]]  # First 5 actions
        
        if feasibilities.count("high") >= 2:
            return "good_onboarding"
        elif feasibilities.count("low") <= 1:
            return "manageable_progression"
        else:
            return "challenging_start"
    
    def _evaluate_sustainability(self, synthesis: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate long-term sustainability"""
        
        actions = synthesis.get("prioritized_actions", [])
        
        # Behavioral vs. technological split
        behavioral_actions = []
        technological_actions = []
        
        behavioral_keywords = ["reduce", "choose", "eat", "walk", "bike", "buy"]
        tech_keywords = ["install", "upgrade", "system", "panels", "vehicle"]
        
        for action in actions:
            action_text = action.get("action", "").lower()
            if any(kw in action_text for kw in behavioral_keywords):
                behavioral_actions.append(action)
            elif any(kw in action_text for kw in tech_keywords):
                technological_actions.append(action)
        
        # Balance assessment
        total_actions = len(actions)
        behavioral_ratio = len(behavioral_actions) / max(total_actions, 1)
        tech_ratio = len(technological_actions) / max(total_actions, 1)
        
        # Sustainability score (balanced approach is better)
        balance_score = 1.0 - abs(behavioral_ratio - tech_ratio)
        
        return {
            "sustainability_score": round(balance_score, 2),
            "behavioral_ratio": round(behavioral_ratio, 2),
            "technological_ratio": round(tech_ratio, 2),
            "sustainability_category": self._categorize_sustainability(balance_score),
            "long_term_viability": self._assess_long_term_viability(actions)
        }
    
    def _categorize_sustainability(self, score: float) -> str:
        """Categorize sustainability level"""
        
        if score >= 0.8:
            return "highly_sustainable"
        elif score >= 0.6:
            return "sustainable"
        elif score >= 0.4:
            return "moderately_sustainable"
        else:
            return "sustainability_concerns"
    
    def _assess_long_term_viability(self, actions: List[Dict[str, Any]]) -> str:
        """Assess long-term viability"""
        
        # Check for actions that create lasting change
        lasting_keywords = ["install", "upgrade", "system", "habit", "routine"]
        lasting_actions = len([a for a in actions if any(kw in a.get("action", "").lower() for kw in lasting_keywords)])
        
        if lasting_actions >= len(actions) * 0.6:
            return "high_lasting_impact"
        elif lasting_actions >= len(actions) * 0.3:
            return "moderate_lasting_impact"
        else:
            return "requires_ongoing_effort"
    
    def _calculate_overall_evaluation_score(self, evaluation: Dict[str, Any]) -> float:
        """Calculate overall evaluation score"""
        
        weights = {
            "carbon_impact": 0.35,
            "feasibility": 0.25,
            "cost_benefit": 0.20,
            "user_experience": 0.15,
            "sustainability": 0.05
        }
        
        total_score = 0.0
        for criterion, weight in weights.items():
            criterion_data = evaluation.get(criterion, {})
            
            if criterion == "carbon_impact":
                score = criterion_data.get("impact_score", 0.5)
            else:
                score_key = f"{criterion.replace('_', '_')}_score"
                score = criterion_data.get(score_key, 0.5)
            
            total_score += score * weight
        
        return round(total_score, 3)
    
    def _validate_final_plan(self, synthesis: Dict[str, Any], 
                           refinements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate final plan completeness and quality"""
        
        validation_checks = {
            "completeness": self._check_completeness(synthesis),
            "consistency": self._check_consistency(synthesis),
            "actionability": self._check_actionability(synthesis),
            "measurability": self._check_measurability(synthesis)
        }
        
        # Overall validation score
        validation_score = sum(check["passed"] for check in validation_checks.values()) / len(validation_checks)
        
        return {
            "validation_checks": validation_checks,
            "validation_score": validation_score,
            "validation_passed": validation_score >= 0.75,
            "critical_issues": self._identify_critical_issues(validation_checks)
        }
    
    def _check_completeness(self, synthesis: Dict[str, Any]) -> Dict[str, Any]:
        """Check if plan covers all major domains"""
        
        actions = synthesis.get("prioritized_actions", [])
        domain_coverage = {"home": False, "transport": False, "diet": False, "shopping": False}
        
        for action in actions:
            domain = action.get("domain", "unknown")
            if domain in domain_coverage:
                domain_coverage[domain] = True
        
        coverage_count = sum(domain_coverage.values())
        
        return {
            "passed": coverage_count >= 3,
            "coverage_count": coverage_count,
            "missing_domains": [d for d, covered in domain_coverage.items() if not covered]
        }
    
    def _check_consistency(self, synthesis: Dict[str, Any]) -> Dict[str, Any]:
        """Check internal consistency of recommendations"""
        
        actions = synthesis.get("prioritized_actions", [])
        
        # Check for conflicting recommendations
        conflicts = []
        
        # Example: recommending both high-cost and cost-savings focused approaches
        high_cost_count = len([a for a in actions if "high" in a.get("cost_impact", "").lower()])
        total_count = len(actions)
        
        if high_cost_count > total_count * 0.7:
            conflicts.append("Too many high-cost interventions may not be feasible")
        
        return {
            "passed": len(conflicts) == 0,
            "conflicts_found": len(conflicts),
            "conflicts": conflicts
        }
    
    def _check_actionability(self, synthesis: Dict[str, Any]) -> Dict[str, Any]:
        """Check if actions are specific and actionable"""
        
        actions = synthesis.get("prioritized_actions", [])
        
        actionable_count = 0
        for action in actions:
            action_text = action.get("action", "")
            
            # Check for specific, actionable language
            if len(action_text) > 15 and any(word in action_text.lower() for word in 
                                           ["install", "switch", "reduce", "choose", "upgrade", "use"]):
                actionable_count += 1
        
        actionability_ratio = actionable_count / max(len(actions), 1)
        
        return {
            "passed": actionability_ratio >= 0.8,
            "actionable_ratio": round(actionability_ratio, 2),
            "actionable_count": actionable_count
        }
    
    def _check_measurability(self, synthesis: Dict[str, Any]) -> Dict[str, Any]:
        """Check if outcomes are measurable"""
        
        actions = synthesis.get("prioritized_actions", [])
        
        measurable_count = 0
        for action in actions:
            co2_reduction = action.get("co2_reduction", "")
            
            # Check if CO2 reduction is quantified
            if any(char.isdigit() for char in co2_reduction):
                measurable_count += 1
        
        measurability_ratio = measurable_count / max(len(actions), 1)
        
        return {
            "passed": measurability_ratio >= 0.7,
            "measurable_ratio": round(measurability_ratio, 2),
            "measurable_count": measurable_count
        }
    
    def _identify_critical_issues(self, validation_checks: Dict[str, Any]) -> List[str]:
        """Identify critical validation issues"""
        
        critical_issues = []
        
        for check_name, check_result in validation_checks.items():
            if not check_result["passed"]:
                if check_name == "completeness":
                    critical_issues.append("Plan does not cover all major emission domains")
                elif check_name == "consistency":
                    critical_issues.append("Internal inconsistencies in recommendations")
                elif check_name == "actionability":
                    critical_issues.append("Recommendations lack specific actionable steps")
                elif check_name == "measurability":
                    critical_issues.append("Outcomes are not sufficiently measurable")
        
        return critical_issues
    
    def _assess_user_alignment(self, synthesis: Dict[str, Any], user_input: str) -> Dict[str, Any]:
        """Assess alignment with user's lifestyle and preferences"""
        
        # Extract user characteristics
        user_characteristics = self._extract_user_characteristics(user_input)
        
        # Assess alignment
        alignment_score = self._calculate_alignment_score(synthesis, user_characteristics)
        
        return {
            "alignment_score": alignment_score,
            "user_characteristics": user_characteristics,
            "alignment_category": self._categorize_alignment(alignment_score),
            "personalization_quality": self._assess_personalization(synthesis, user_characteristics)
        }
    
    def _extract_user_characteristics(self, user_input: str) -> Dict[str, Any]:
        """Extract user characteristics from input"""
        
        characteristics = {
            "luxury_oriented": False,
            "tech_savvy": False,
            "environmentally_conscious": False,
            "budget_conscious": False,
            "convenience_focused": False
        }
        
        # Simple keyword-based extraction
        if any(word in user_input.lower() for word in ["luxury", "expensive", "premium", "high-end"]):
            characteristics["luxury_oriented"] = True
        
        if any(word in user_input.lower() for word in ["tech", "smart", "app", "digital"]):
            characteristics["tech_savvy"] = True
        
        if any(word in user_input.lower() for word in ["eco", "green", "sustainable", "environment"]):
            characteristics["environmentally_conscious"] = True
        
        if any(word in user_input.lower() for word in ["cheap", "affordable", "budget", "save money"]):
            characteristics["budget_conscious"] = True
        
        if any(word in user_input.lower() for word in ["convenient", "easy", "simple", "quick"]):
            characteristics["convenience_focused"] = True
        
        return characteristics
    
    def _calculate_alignment_score(self, synthesis: Dict[str, Any], 
                                 characteristics: Dict[str, Any]) -> float:
        """Calculate alignment score"""
        
        actions = synthesis.get("prioritized_actions", [])
        alignment_points = 0
        total_points = 0
        
        for action in actions:
            total_points += 1
            
            # Check alignment with user characteristics
            if characteristics["budget_conscious"]:
                if "savings" in action.get("cost_impact", "").lower() or "low" in action.get("cost_impact", "").lower():
                    alignment_points += 1
            
            if characteristics["convenience_focused"]:
                if action.get("feasibility") == "high":
                    alignment_points += 1
            
            if characteristics["tech_savvy"]:
                if any(word in action.get("action", "").lower() for word in ["smart", "app", "system", "tech"]):
                    alignment_points += 1
            
            if characteristics["environmentally_conscious"]:
                if any(word in action.get("action", "").lower() for word in ["renewable", "sustainable", "eco", "green"]):
                    alignment_points += 1
        
        return alignment_points / max(total_points, 1)
    
    def _categorize_alignment(self, score: float) -> str:
        """Categorize alignment level"""
        
        if score >= 0.8:
            return "highly_aligned"
        elif score >= 0.6:
            return "well_aligned"
        elif score >= 0.4:
            return "moderately_aligned"
        else:
            return "poorly_aligned"
    
    def _assess_personalization(self, synthesis: Dict[str, Any], 
                              characteristics: Dict[str, Any]) -> str:
        """Assess quality of personalization"""
        
        actions = synthesis.get("prioritized_actions", [])
        
        # Check if high-priority actions match user characteristics
        top_actions = actions[:3]  # Top 3 actions
        
        personalized_count = 0
        for action in top_actions:
            if self._action_matches_user(action, characteristics):
                personalized_count += 1
        
        if personalized_count >= 2:
            return "well_personalized"
        elif personalized_count >= 1:
            return "somewhat_personalized"
        else:
            return "generic_recommendations"
    
    def _action_matches_user(self, action: Dict[str, Any], 
                           characteristics: Dict[str, Any]) -> bool:
        """Check if action matches user characteristics"""
        
        action_text = action.get("action", "").lower()
        cost_impact = action.get("cost_impact", "").lower()
        feasibility = action.get("feasibility", "medium")
        
        # Budget conscious users should get cost-effective actions
        if characteristics["budget_conscious"] and ("savings" in cost_impact or "low" in cost_impact):
            return True
        
        # Convenience focused users should get high-feasibility actions
        if characteristics["convenience_focused"] and feasibility == "high":
            return True
        
        # Tech savvy users should get technology-based solutions
        if characteristics["tech_savvy"] and any(word in action_text for word in ["smart", "app", "system", "electric"]):
            return True
        
        # Luxury oriented users might prefer premium solutions
        if characteristics["luxury_oriented"] and any(word in action_text for word in ["premium", "high-end", "advanced"]):
            return True
        
        return False
    
    def _analyze_implementation_risks(self, synthesis: Dict[str, Any], 
                                    refinements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze implementation risks"""
        
        risks = {
            "financial_risks": self._assess_financial_risks(synthesis),
            "technical_risks": self._assess_technical_risks(synthesis),
            "behavioral_risks": self._assess_behavioral_risks(synthesis),
            "external_risks": self._assess_external_risks(synthesis)
        }
        
        # Overall risk level
        risk_scores = [risk.get("risk_level", 0.5) for risk in risks.values()]
        overall_risk = sum(risk_scores) / len(risk_scores)
        
        return {
            "risk_categories": risks,
            "overall_risk_level": round(overall_risk, 2),
            "risk_category": self._categorize_risk(overall_risk),
            "mitigation_strategies": self._suggest_risk_mitigation(risks)
        }
    
    def _assess_financial_risks(self, synthesis: Dict[str, Any]) -> Dict[str, Any]:
        """Assess financial implementation risks"""
        
        actions = synthesis.get("prioritized_actions", [])
        high_cost_actions = [a for a in actions if "high" in a.get("cost_impact", "").lower()]
        
        risk_level = len(high_cost_actions) / max(len(actions), 1)
        
        return {
            "risk_level": risk_level,
            "high_cost_action_count": len(high_cost_actions),
            "risk_factors": ["High upfront investment required"] if risk_level > 0.5 else []
        }
    
    def _assess_technical_risks(self, synthesis: Dict[str, Any]) -> Dict[str, Any]:
        """Assess technical implementation risks"""
        
        actions = synthesis.get("prioritized_actions", [])
        technical_actions = [a for a in actions if any(word in a.get("action", "").lower() 
                                                     for word in ["install", "system", "upgrade", "technical"])]
        
        risk_level = len(technical_actions) / max(len(actions), 1)
        
        return {
            "risk_level": risk_level,
            "technical_action_count": len(technical_actions),
            "risk_factors": ["Technical expertise required"] if risk_level > 0.4 else []
        }
    
    def _assess_behavioral_risks(self, synthesis: Dict[str, Any]) -> Dict[str, Any]:
        """Assess behavioral change risks"""
        
        actions = synthesis.get("prioritized_actions", [])
        behavioral_actions = [a for a in actions if any(word in a.get("action", "").lower() 
                                                      for word in ["reduce", "change", "habit", "lifestyle"])]
        
        risk_level = len(behavioral_actions) / max(len(actions), 1)
        
        return {
            "risk_level": risk_level,
            "behavioral_action_count": len(behavioral_actions),
            "risk_factors": ["Sustained behavior change required"] if risk_level > 0.5 else []
        }
    
    def _assess_external_risks(self, synthesis: Dict[str, Any]) -> Dict[str, Any]:
        """Assess external implementation risks"""
        
        # Simplified external risk assessment
        risk_level = 0.3  # Base external risk
        
        return {
            "risk_level": risk_level,
            "risk_factors": ["Market conditions", "Policy changes", "Technology availability"]
        }
    
    def _categorize_risk(self, risk_level: float) -> str:
        """Categorize overall risk level"""
        
        if risk_level >= 0.7:
            return "high_risk"
        elif risk_level >= 0.5:
            return "medium_risk"
        elif risk_level >= 0.3:
            return "low_medium_risk"
        else:
            return "low_risk"
    
    def _suggest_risk_mitigation(self, risks: Dict[str, Any]) -> List[str]:
        """Suggest risk mitigation strategies"""
        
        strategies = []
        
        # Financial risk mitigation
        if risks["financial_risks"]["risk_level"] > 0.5:
            strategies.append("Phase high-cost investments over time")
            strategies.append("Explore financing options and incentives")
        
        # Technical risk mitigation
        if risks["technical_risks"]["risk_level"] > 0.4:
            strategies.append("Engage qualified professionals for technical implementations")
            strategies.append("Start with simpler technical solutions")
        
        # Behavioral risk mitigation
        if risks["behavioral_risks"]["risk_level"] > 0.5:
            strategies.append("Implement gradual behavior changes")
            strategies.append("Set up tracking and accountability systems")
        
        return strategies
    
    def _define_success_metrics(self, synthesis: Dict[str, Any]) -> Dict[str, Any]:
        """Define success metrics for the plan"""
        
        total_footprint = synthesis.get("total_carbon_footprint", 0.0)
        impact_analysis = synthesis.get("impact_analysis", {})
        potential_reduction = impact_analysis.get("total_potential_reduction", 0.0)
        
        return {
            "primary_metrics": {
                "carbon_footprint_reduction": {
                    "baseline": total_footprint,
                    "target": max(0, total_footprint - potential_reduction),
                    "measurement": "tons CO2/year"
                },
                "eco_score_improvement": {
                    "baseline": synthesis.get("eco_score", 25),
                    "target": min(100, synthesis.get("eco_score", 25) + 40),
                    "measurement": "EcoScore points (0-100)"
                }
            },
            "secondary_metrics": {
                "implementation_progress": {
                    "measurement": "% of actions completed",
                    "target": 80
                },
                "cost_savings": {
                    "measurement": "USD/year in energy savings",
                    "target": "Variable based on actions"
                }
            },
            "tracking_frequency": {
                "carbon_footprint": "quarterly",
                "eco_score": "monthly",
                "implementation_progress": "weekly"
            }
        }
    
    def _generate_final_plan(self, synthesis: Dict[str, Any], refinements: List[Dict[str, Any]],
                           evaluation_results: Dict[str, Any], validation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the final comprehensive plan"""
        
        # Get the best refined plan or use original synthesis
        if refinements and refinements[-1].get("quality_score", 0) > 0.7:
            base_plan = refinements[-1].get("refined_plan", synthesis)
        else:
            base_plan = synthesis
        
        # Create final action plan
        final_actions = self._finalize_action_list(base_plan, evaluation_results)
        
        # Create implementation timeline
        implementation_timeline = self._create_implementation_timeline(final_actions)
        
        # Create success tracking plan
        tracking_plan = self._create_tracking_plan(final_actions)
        
        return {
            "final_actions": final_actions,
            "implementation_timeline": implementation_timeline,
            "tracking_plan": tracking_plan,
            "expected_outcomes": self._define_expected_outcomes(final_actions),
            "next_steps": self._define_next_steps(final_actions),
            "support_resources": self._identify_support_resources(final_actions)
        }
    
    def _finalize_action_list(self, plan: Dict[str, Any], 
                            evaluation_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Finalize the action list based on evaluation"""
        
        actions = plan.get("prioritized_actions", [])
        
        # Add final touches to each action
        for action in actions:
            # Add success criteria
            action["success_criteria"] = self._define_action_success_criteria(action)
            
            # Add timeline
            action["timeline"] = self._estimate_action_timeline(action)
            
            # Add resources needed
            action["resources_needed"] = self._identify_action_resources(action)
        
        # Keep top 6 actions for focus
        return actions[:6]
    
    def _define_action_success_criteria(self, action: Dict[str, Any]) -> List[str]:
        """Define success criteria for an action"""
        
        action_text = action.get("action", "").lower()
        criteria = []
        
        if "solar" in action_text:
            criteria = ["System installed and operational", "Monthly energy bill reduced", "CO2 emissions tracked"]
        elif "electric" in action_text:
            criteria = ["Vehicle purchased/leased", "Charging setup complete", "Fuel costs eliminated"]
        elif "diet" in action_text or "meat" in action_text:
            criteria = ["Meal planning established", "Plant-based meals tracked", "Nutritional balance maintained"]
        elif "insulation" in action_text or "efficiency" in action_text:
            criteria = ["Installation completed", "Energy usage monitored", "Comfort level maintained"]
        else:
            criteria = ["Action implemented", "Progress tracked", "Results measured"]
        
        return criteria
    
    def _estimate_action_timeline(self, action: Dict[str, Any]) -> str:
        """Estimate timeline for action completion"""
        
        feasibility = action.get("feasibility", "medium")
        cost_impact = action.get("cost_impact", "medium").lower()
        
        if feasibility == "high" and ("low" in cost_impact or "savings" in cost_impact):
            return "1-4 weeks"
        elif feasibility == "high":
            return "1-3 months"
        elif feasibility == "medium":
            return "3-6 months"
        else:
            return "6-12 months"
    
    def _identify_action_resources(self, action: Dict[str, Any]) -> List[str]:
        """Identify resources needed for action"""
        
        action_text = action.get("action", "").lower()
        resources = []
        
        if "install" in action_text:
            resources = ["Professional installer", "Permits/approvals", "Financing"]
        elif "purchase" in action_text or "buy" in action_text:
            resources = ["Research time", "Budget allocation", "Vendor selection"]
        elif "reduce" in action_text or "change" in action_text:
            resources = ["Habit tracking app", "Alternative options research", "Support system"]
        else:
            resources = ["Planning time", "Implementation budget", "Progress tracking"]
        
        return resources
    
    def _create_implementation_timeline(self, actions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create implementation timeline"""
        
        timeline = {
            "immediate": [],  # 0-1 month
            "short_term": [],  # 1-6 months
            "medium_term": [],  # 6-12 months
            "long_term": []  # 12+ months
        }
        
        for action in actions:
            action_timeline = action.get("timeline", "3-6 months")
            
            if "week" in action_timeline or "1-4" in action_timeline:
                timeline["immediate"].append(action["action"])
            elif "1-3 months" in action_timeline:
                timeline["short_term"].append(action["action"])
            elif "3-6 months" in action_timeline:
                timeline["medium_term"].append(action["action"])
            else:
                timeline["long_term"].append(action["action"])
        
        return timeline
    
    def _create_tracking_plan(self, actions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create tracking and monitoring plan"""
        
        return {
            "monthly_reviews": [
                "Track carbon footprint changes",
                "Monitor implementation progress",
                "Assess cost savings",
                "Update EcoScore"
            ],
            "quarterly_assessments": [
                "Comprehensive impact evaluation",
                "Plan adjustments if needed",
                "Celebrate achievements",
                "Set next quarter goals"
            ],
            "key_performance_indicators": [
                "Total CO2 reduction achieved",
                "Percentage of actions completed",
                "Cost savings realized",
                "EcoScore improvement"
            ]
        }
    
    def _define_expected_outcomes(self, actions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Define expected outcomes"""
        
        total_co2_reduction = 0.0
        for action in actions:
            co2_text = action.get("co2_reduction", "0.5")
            try:
                import re
                numbers = re.findall(r'(\d+(?:\.\d+)?)', co2_text)
                if numbers:
                    total_co2_reduction += float(numbers[-1])
            except:
                total_co2_reduction += 0.5
        
        return {
            "carbon_impact": {
                "total_reduction": f"{total_co2_reduction:.1f} tons CO2/year",
                "percentage_reduction": "40-70%",
                "global_impact": "Equivalent to planting 50-150 trees annually"
            },
            "financial_impact": {
                "annual_savings": "$1,000-5,000/year",
                "payback_period": "3-8 years",
                "long_term_value": "$10,000-50,000 over 10 years"
            },
            "lifestyle_impact": {
                "health_benefits": "Improved air quality, more active lifestyle",
                "convenience": "Long-term convenience improvements",
                "satisfaction": "Positive environmental impact satisfaction"
            }
        }
    
    def _define_next_steps(self, actions: List[Dict[str, Any]]) -> List[str]:
        """Define immediate next steps"""
        
        if not actions:
            return ["Review and understand your carbon footprint", "Choose your first action to implement"]
        
        first_action = actions[0]
        action_text = first_action.get("action", "")
        
        if "solar" in action_text.lower():
            return [
                "Get 3 quotes from certified solar installers",
                "Research local incentives and tax credits",
                "Schedule roof assessment"
            ]
        elif "electric" in action_text.lower():
            return [
                "Research EV models within your budget",
                "Test drive top 3 candidates",
                "Plan home charging installation"
            ]
        elif "diet" in action_text.lower():
            return [
                "Plan 2 plant-based meals for next week",
                "Find local farmers market or organic store",
                "Download a meal planning app"
            ]
        else:
            return [
                f"Begin planning: {action_text}",
                "Set up progress tracking system",
                "Schedule first implementation milestone"
            ]
    
    def _identify_support_resources(self, actions: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Identify support resources needed"""
        
        return {
            "professional_services": [
                "Energy auditor for home efficiency assessment",
                "Solar installer for renewable energy systems",
                "Nutritionist for dietary transition support"
            ],
            "online_resources": [
                "Carbon footprint tracking apps",
                "Energy efficiency calculators",
                "Sustainable living communities and forums"
            ],
            "local_resources": [
                "Environmental organizations",
                "Green building contractors",
                "Farmers markets and co-ops",
                "EV dealerships and charging networks"
            ],
            "financial_resources": [
                "Green financing options",
                "Government incentives and rebates",
                "Utility company programs",
                "Carbon offset programs"
            ]
        }
    
    def _calculate_final_eco_score(self, synthesis: Dict[str, Any], 
                                 evaluation_results: Dict[str, Any],
                                 user_alignment: Dict[str, Any]) -> float:
        """Calculate final EcoScore incorporating all factors"""
        
        base_score = synthesis.get("eco_score", 25)
        
        # Evaluation quality bonus
        overall_eval_score = evaluation_results.get("overall_score", 0.5)
        eval_bonus = overall_eval_score * 20  # Up to 20 point bonus
        
        # User alignment bonus
        alignment_score = user_alignment.get("alignment_score", 0.5)
        alignment_bonus = alignment_score * 15  # Up to 15 point bonus
        
        # Implementation feasibility bonus
        feasibility_data = evaluation_results.get("feasibility", {})
        feasibility_score = feasibility_data.get("feasibility_score", 0.5)
        feasibility_bonus = feasibility_score * 10  # Up to 10 point bonus
        
        final_score = base_score + eval_bonus + alignment_bonus + feasibility_bonus
        
        return round(min(100, max(0, final_score)), 1)
    
    def _calculate_implementation_confidence(self, validation_results: Dict[str, Any]) -> float:
        """Calculate confidence in successful implementation"""
        
        validation_score = validation_results.get("validation_score", 0.5)
        validation_passed = validation_results.get("validation_passed", False)
        
        if validation_passed and validation_score >= 0.9:
            return 0.95
        elif validation_passed and validation_score >= 0.8:
            return 0.85
        elif validation_passed:
            return 0.75
        elif validation_score >= 0.6:
            return 0.6
        else:
            return 0.4
    
    def _create_recommendations_summary(self, final_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Create executive summary of recommendations"""
        
        actions = final_plan.get("final_actions", [])
        
        if not actions:
            return {"summary": "No specific recommendations generated"}
        
        # Top 3 recommendations
        top_3 = actions[:3]
        
        # Quick wins (high feasibility, low cost)
        quick_wins = [a for a in actions if a.get("feasibility") == "high" and 
                     ("low" in a.get("cost_impact", "").lower() or "savings" in a.get("cost_impact", "").lower())]
        
        # High impact actions
        high_impact = [a for a in actions if "high" in a.get("co2_reduction", "")]
        
        return {
            "top_3_recommendations": [a["action"] for a in top_3],
            "quick_wins": [a["action"] for a in quick_wins[:2]],
            "high_impact_actions": [a["action"] for a in high_impact[:2]],
            "implementation_approach": "Start with quick wins, then tackle high-impact projects",
            "expected_timeline": "6-18 months for full implementation",
            "key_success_factors": [
                "Consistent progress tracking",
                "Phased implementation approach", 
                "Professional support where needed"
            ]
        }