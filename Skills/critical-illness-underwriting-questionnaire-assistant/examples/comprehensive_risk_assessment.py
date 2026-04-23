#!/usr/bin/env python3
"""
GEO-INFER-RISK Example: Comprehensive Risk Assessment

This example demonstrates multi-hazard risk assessment with
exposure analysis, vulnerability modeling, and loss estimation.
"""

from geo_infer_risk import (
    EnhancedRiskEngine,
    HazardModel,
    ExposureModel,
    VulnerabilityModel,
    LossModel
)


def main():
    print("=" * 60)
    print("GEO-INFER-RISK: Comprehensive Risk Assessment")
    print("=" * 60)
    
    # 1. Initialize Risk Engine
    print("\n1. Initializing Enhanced Risk Engine...")
    
    engine = EnhancedRiskEngine(
        config={
            'analysis_type': 'probabilistic',
            'correlation_modeling': True,
            'uncertainty_quantification': True
        }
    )
    
    integration_status = engine.get_integration_status()
    print(f"   Space integration: {'✓' if integration_status.space_integration else '✗'}")
    print(f"   Bayes integration: {'✓' if integration_status.bayes_integration else '✗'}")
    
    # 2. Define Study Area
    print("\n2. Defining Study Area...")
    
    study_area = {
        'name': 'Metropolitan Region',
        'bbox': [-122.5, 37.2, -121.8, 37.9],
        'area_km2': 3500,
        'zones': 150
    }
    
    print(f"   Area: {study_area['name']}")
    print(f"   Size: {study_area['area_km2']:,} km²")
    
    # 3. Hazard Modeling
    print("\n3. Running Hazard Models...")
    
    hazard_model = HazardModel(
        hazard_types=['earthquake', 'flood', 'wildfire'],
        modeling_approach='probabilistic'
    )
    
    # Earthquake hazard
    eq_hazard = hazard_model.compute_hazard(
        hazard_type='earthquake',
        region=study_area,
        return_periods=[100, 250, 500, 1000],
        intensity_measure='pga'
    )
    
    print(f"   Earthquake (100yr): PGA = {eq_hazard['100yr']['pga']:.3f}g")
    print(f"   Earthquake (500yr): PGA = {eq_hazard['500yr']['pga']:.3f}g")
    
    # Flood hazard
    flood_hazard = hazard_model.compute_hazard(
        hazard_type='flood',
        region=study_area,
        return_periods=[100, 500],
        intensity_measure='depth'
    )
    
    print(f"   Flood (100yr): Depth = {flood_hazard['100yr']['depth']:.1f}m")
    
    # 4. Exposure Analysis
    print("\n4. Analyzing Exposure...")
    
    exposure = ExposureModel(
        asset_categories=['residential', 'commercial', 'industrial', 'infrastructure'],
        valuation_method='replacement_cost'
    )
    
    exposure_data = exposure.analyze(
        region=study_area,
        building_data={
            'residential': {'count': 500000, 'avg_value': 450000},
            'commercial': {'count': 50000, 'avg_value': 2000000},
            'industrial': {'count': 5000, 'avg_value': 5000000},
            'infrastructure': {'count': 500, 'avg_value': 50000000}
        }
    )
    
    print(f"   Total exposed value: ${exposure_data['total_value']/1e9:.1f}B")
    print(f"   Residential: ${exposure_data['by_category']['residential']/1e9:.1f}B")
    print(f"   Commercial: ${exposure_data['by_category']['commercial']/1e9:.1f}B")
    
    # 5. Vulnerability Modeling
    print("\n5. Building Vulnerability Functions...")
    
    vulnerability = VulnerabilityModel(
        approach='fragility_based',
        building_taxonomy='gem'
    )
    
    vuln_functions = vulnerability.build_functions(
        building_types=['wood_frame', 'concrete_moment', 'masonry', 'steel_frame'],
        hazard_types=['earthquake', 'flood']
    )
    
    print(f"   Vulnerability functions: {len(vuln_functions)}")
    
    # Sample vulnerability
    damage_state = vulnerability.compute_damage_state(
        building_type='wood_frame',
        hazard_type='earthquake',
        intensity=0.3  # 0.3g PGA
    )
    
    print(f"   Wood frame at 0.3g PGA:")
    for state, prob in damage_state.items():
        print(f"     {state}: {prob:.1%}")
    
    # 6. Loss Estimation
    print("\n6. Estimating Losses...")
    
    loss_model = LossModel(
        loss_categories=['structural', 'contents', 'business_interruption'],
        economic_model='direct_indirect'
    )
    
    # Scenario-based loss
    scenario_loss = loss_model.estimate_scenario(
        hazard_event={
            'type': 'earthquake',
            'magnitude': 7.0,
            'return_period': 500
        },
        exposure=exposure_data,
        vulnerability=vuln_functions
    )
    
    print(f"   Scenario loss (M7.0 EQ):")
    print(f"     Structural: ${scenario_loss['structural']/1e9:.1f}B")
    print(f"     Contents: ${scenario_loss['contents']/1e9:.1f}B")
    print(f"     Business interruption: ${scenario_loss['business_interruption']/1e9:.1f}B")
    print(f"     Total: ${scenario_loss['total']/1e9:.1f}B")
    
    # 7. Probabilistic Loss Analysis
    print("\n7. Running Probabilistic Analysis...")
    
    prob_analysis = loss_model.run_probabilistic(
        hazard_models=[eq_hazard, flood_hazard],
        exposure=exposure_data,
        vulnerability=vuln_functions,
        num_simulations=10000
    )
    
    print(f"   Average Annual Loss (AAL): ${prob_analysis['aal']/1e6:.1f}M")
    print(f"   Standard deviation: ${prob_analysis['std']/1e6:.1f}M")
    
    # Exceedance probability curve
    print("   Exceedance Probabilities:")
    for ep, loss in prob_analysis['ep_curve'].items():
        print(f"     {ep}: ${loss/1e9:.1f}B")
    
    # 8. Risk Metrics
    print("\n8. Computing Risk Metrics...")
    
    metrics = engine.compute_risk_metrics(
        loss_distribution=prob_analysis,
        exposure=exposure_data
    )
    
    print(f"   Pure risk premium: {metrics['pure_premium']:.4f}")
    print(f"   Return period 250yr: ${metrics['rp250']/1e9:.1f}B")
    print(f"   Coefficient of variation: {metrics['cov']:.2f}")
    print(f"   Tail Value at Risk (95%): ${metrics['tvar_95']/1e9:.1f}B")
    
    # 9. Multi-Hazard Correlation
    print("\n9. Analyzing Multi-Hazard Correlations...")
    
    correlation = engine.analyze_hazard_correlation(
        hazards=['earthquake', 'flood', 'wildfire'],
        method='copula'
    )
    
    print("   Hazard correlations:")
    print(f"     EQ-Flood: {correlation['earthquake_flood']:.2f}")
    print(f"     EQ-Fire: {correlation['earthquake_wildfire']:.2f}")
    print(f"     Flood-Fire: {correlation['flood_wildfire']:.2f}")
    
    print("\n" + "=" * 60)
    print("Risk Assessment Complete!")
    print("=" * 60)
    
    # Summary
    print("\nRisk Summary:")
    print(f"  - Study Area: {study_area['name']}")
    print(f"  - Total Exposure: ${exposure_data['total_value']/1e9:.1f}B")
    print(f"  - AAL: ${prob_analysis['aal']/1e6:.1f}M ({prob_analysis['aal']/exposure_data['total_value']*100:.3f}%)")
    print(f"  - 500yr Loss: ${prob_analysis['ep_curve'].get('0.2%', 0)/1e9:.1f}B")


if __name__ == "__main__":
    main()
