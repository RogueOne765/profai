import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import random


@dataclass
class ScenarioParameters:
    revenue_change: float
    cost_change: float
    interest_rate_change: float
    exchange_rate_change: float
    probability: float


@dataclass
class ScenarioResult:
    scenario_name: str
    year: int
    revenue: float
    ebitda: float
    ebit: float
    net_income: float
    cash_flow: float
    debt: float
    current_ratio: float
    quick_ratio: float
    probability: float


class RiskSimulator:
    def __init__(self, baseline_data: Dict[str, Any]):
        self.baseline = baseline_data
        self.scenarios = self._define_scenarios()
        
    def _define_scenarios(self) -> Dict[str, ScenarioParameters]:
        return {
            "base": ScenarioParameters(
                revenue_change=0.0,
                cost_change=0.0,
                interest_rate_change=0.0,
                exchange_rate_change=0.0,
                probability=0.50
            ),
            "recession": ScenarioParameters(
                revenue_change=-0.15,
                cost_change=0.10,
                interest_rate_change=0.02,
                exchange_rate_change=-0.10,
                probability=0.25
            ),
            "stress": ScenarioParameters(
                revenue_change=-0.25,
                cost_change=0.20,
                interest_rate_change=0.03,
                exchange_rate_change=-0.15,
                probability=0.15
            ),
            "expansion": ScenarioParameters(
                revenue_change=0.10,
                cost_change=0.03,
                interest_rate_change=-0.01,
                exchange_rate_change=0.05,
                probability=0.10
            )
        }
    
    def simulate(self, years: int = 3) -> Dict[str, List[ScenarioResult]]:
        results = {}
        
        for scenario_name, params in self.scenarios.items():
            scenario_results = []
            current_revenue = self.baseline.get("revenue", 45.0)
            current_ebitda = self.baseline.get("ebitda", 9.3)
            current_debt = self.baseline.get("total_liabilities", 40.7)
            
            for year in range(1, years + 1):
                revenue = current_revenue * (1 + params.revenue_change) ** year
                costs_multiplier = 1 + params.cost_change
                ebitda = revenue * (self.baseline.get("ebitda_margin", 0.19) + 
                                   (params.revenue_change * 0.5) - 
                                   (params.cost_change * 0.5))
                
                ebit = ebitda * 0.75
                interest = current_debt * (0.03 + params.interest_rate_change)
                taxes = (ebit - interest) * 0.24
                net_income = ebit - interest - taxes
                
                cash_flow = ebitda * 0.5
                current_ratio = self.baseline.get("current_ratio", 1.14) + (params.revenue_change * 0.5)
                quick_ratio = self.baseline.get("quick_ratio", 0.72) + (params.revenue_change * 0.3)
                
                if params.revenue_change < 0:
                    debt_change = abs(params.revenue_change) * 0.3
                else:
                    debt_change = -0.02
                debt = current_debt * (1 + debt_change) ** year
                
                result = ScenarioResult(
                    scenario_name=scenario_name,
                    year=year,
                    revenue=round(revenue, 2),
                    ebitda=round(ebitda, 2),
                    ebit=round(ebit, 2),
                    net_income=round(net_income, 2),
                    cash_flow=round(cash_flow, 2),
                    debt=round(debt, 2),
                    current_ratio=round(current_ratio, 2),
                    quick_ratio=round(quick_ratio, 2),
                    probability=params.probability
                )
                scenario_results.append(result)
            
            results[scenario_name] = scenario_results
        
        return results
    
    def calculate_default_probability(self, results: Dict) -> float:
        default_count = 0
        total_scenarios = 0
        
        for scenario_name, scenario_results in results.items():
            params = self.scenarios[scenario_name]
            total_scenarios += params.probability
            
            for result in scenario_results:
                if result.current_ratio < 0.8 or result.quick_ratio < 0.5:
                    default_count += params.probability
        
        return round((default_count / total_scenarios) * 100, 2) if total_scenarios > 0 else 0
    
    def get_value_at_risk(self, results: Dict, percentile: int = 5) -> Dict:
        all_ebitdas = []
        all_net_incomes = []
        
        for scenario_name, scenario_results in results.items():
            params = self.scenarios[scenario_name]
            weight = params.probability
            
            for result in scenario_results:
                all_ebitdas.extend([result.ebitda] * int(weight * 100))
                all_net_incomes.extend([result.net_income] * int(weight * 100))
        
        if not all_ebitdas:
            return {"var_ebitda": 0, "var_net_income": 0}
        
        all_ebitdas.sort()
        all_net_incomes.sort()
        
        idx = max(0, len(all_ebitdas) * percentile // 100 - 1)
        
        return {
            "var_ebitda": all_ebitdas[idx],
            "var_net_income": all_net_incomes[idx],
            "percentile": percentile
        }
    
    def monte_carlo_simulation(self, n_simulations: int = 1000) -> Dict:
        revenues = []
        ebitdas = []
        net_incomes = []
        
        for _ in range(n_simulations):
            rev_change = random.gauss(-0.05, 0.15)
            cost_change = random.gauss(0.03, 0.08)
            
            revenue = self.baseline.get("revenue", 45.0) * (1 + rev_change)
            ebitda = revenue * (self.baseline.get("ebitda_margin", 0.19) + 
                               (rev_change * 0.3) - (cost_change * 0.4))
            ebitda = max(0, ebitda)
            net_income = ebitda * 0.6 * 0.76
            
            revenues.append(revenue)
            ebitdas.append(ebitda)
            net_incomes.append(net_income)
        
        revenues.sort()
        ebitdas.sort()
        net_incomes.sort()
        
        return {
            "revenue": {
                "mean": round(sum(revenues) / len(revenues), 2),
                "p5": round(revenues[int(len(revenues) * 0.05)], 2),
                "p95": round(revenues[int(len(revenues) * 0.95)], 2)
            },
            "ebitda": {
                "mean": round(sum(ebitdas) / len(ebitdas), 2),
                "p5": round(ebitdas[int(len(ebitdas) * 0.05)], 2),
                "p95": round(ebitdas[int(len(ebitdas) * 0.95)], 2)
            },
            "net_income": {
                "mean": round(sum(net_incomes) / len(net_incomes), 2),
                "p5": round(net_incomes[int(len(net_incomes) * 0.05)], 2),
                "p95": round(net_incomes[int(len(net_incomes) * 0.95)], 2)
            }
        }
    
    def export_results(self, results: Dict, format: str = "json") -> str:
        if format == "json":
            output = {}
            for scenario_name, scenario_results in results.items():
                output[scenario_name] = [asdict(r) for r in scenario_results]
            return json.dumps(output, indent=2)
        
        elif format == "csv":
            lines = ["scenario,year,revenue,ebitda,ebit,net_income,cash_flow,debt,current_ratio,quick_ratio,probability"]
            for scenario_name, scenario_results in results.items():
                for r in scenario_results:
                    lines.append(f"{r.scenario_name},{r.year},{r.revenue},{r.ebitda},{r.ebit},{r.net_income},{r.cash_flow},{r.debt},{r.current_ratio},{r.quick_ratio},{r.probability}")
            return "\n".join(lines)
        
        return ""


if __name__ == "__main__":
    baseline = {
        "revenue": 49.0,
        "ebitda": 9.3,
        "ebitda_margin": 0.19,
        "total_liabilities": 40.7,
        "current_ratio": 1.14,
        "quick_ratio": 0.72
    }
    
    simulator = RiskSimulator(baseline)
    results = simulator.simulate(3)
    
    print("Scenario Analysis Results:")
    for scenario, res in results.items():
        print(f"\n{scenario.upper()}:")
        for r in res:
            print(f"  Year {r.year}: Revenue={r.revenue}M, EBITDA={r.ebitda}M, Net Income={r.net_income}M")
    
    print(f"\nDefault Probability: {simulator.calculate_default_probability(results)}%")
    print(f"Value at Risk (5th percentile): {simulator.get_value_at_risk(results)}")
