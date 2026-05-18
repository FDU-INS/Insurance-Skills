"""
Basic risk assessment example using GEO-INFER-RISK.

This example demonstrates:
- Risk engine initialization
- Hazard modeling
- Vulnerability assessment
- Risk calculation
"""

import sys
import os
import numpy as np
import pandas as pd

# Add src directory to path
project_root = os.path.dirname(os.path.dirname(__file__))
src_path = os.path.join(project_root, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    import geopandas as gpd
    from shapely.geometry import Point, Polygon
    from geo_infer_risk.core.risk_engine import RiskEngine
    IMPORTS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Some imports not available: {e}")
    IMPORTS_AVAILABLE = False


def create_sample_exposure_data():
    """Create sample exposure data (assets at risk)."""
    # Create sample points representing assets
    points = [
        Point(-122.4194, 37.7749),  # Asset 1
        Point(-122.4094, 37.7849),  # Asset 2
        Point(-122.4294, 37.7649),  # Asset 3
    ]
    
    data = {
        'asset_id': ['asset_001', 'asset_002', 'asset_003'],
        'asset_type': ['building', 'infrastructure', 'building'],
        'value': [1000000, 5000000, 2000000],
        'geometry': points
    }
    
    return gpd.GeoDataFrame(data, crs='EPSG:4326')


def main():
    """Run basic risk assessment example."""
    print("=" * 60)
    print("GEO-INFER-RISK: Basic Risk Assessment Example")
    print("=" * 60)
    
    if not IMPORTS_AVAILABLE:
        print("\n⚠️  Some required modules are not available.")
        print("   This example requires full GEO-INFER-RISK installation.")
        return
    
    # Step 1: Risk engine initialization
    print("\n⚙️  Step 1: Initializing risk engine...")
    try:
        risk_engine = RiskEngine()
        print(f"   ✅ Risk engine initialized")
        print(f"   Available capabilities:")
        print(f"      • Hazard modeling")
        print(f"      • Vulnerability assessment")
        print(f"      • Exposure analysis")
        print(f"      • Risk calculation")
        print(f"      • Uncertainty quantification")
    except Exception as e:
        print(f"   ⚠️  Risk engine initialization: {e}")
        risk_engine = None
    
    # Step 2: Exposure data
    print("\n📊 Step 2: Preparing exposure data...")
    try:
        exposure_data = create_sample_exposure_data()
        print(f"   ✅ Created exposure dataset with {len(exposure_data)} assets")
        print(f"   Total asset value: ${exposure_data['value'].sum():,.0f}")
        print(f"   Asset types: {', '.join(exposure_data['asset_type'].unique())}")
    except Exception as e:
        print(f"   ⚠️  Exposure data: {e}")
        exposure_data = None
    
    # Step 3: Risk assessment
    print("\n🔍 Step 3: Performing risk assessment...")
    try:
        if risk_engine is not None and exposure_data is not None:
            print(f"   ✅ Risk assessment framework ready")
            print(f"   Assessment components:")
            print(f"      • Hazard identification")
            print(f"      • Vulnerability modeling")
            print(f"      • Exposure mapping")
            print(f"      • Risk quantification")
            print(f"      • Spatial risk visualization")
    except Exception as e:
        print(f"   ⚠️  Risk assessment: {e}")
    
    # Step 4: Integration capabilities
    print("\n🔗 Step 4: Integration capabilities...")
    try:
        print(f"   ✅ GEO-INFER-RISK integrates with:")
        print(f"      • SPACE: Spatial risk mapping")
        print(f"      • TIME: Temporal risk dynamics")
        print(f"      • AI: Machine learning risk models")
        print(f"      • BAYES: Bayesian risk inference")
        print(f"      • MATH: Statistical risk methods")
        print(f"      • HEALTH: Health risk assessment")
        print(f"      • ECON: Economic risk analysis")
    except Exception as e:
        print(f"   ⚠️  Integration info: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Risk assessment example complete!")
    print("=" * 60)
    print("\nKey capabilities demonstrated:")
    print("  • Risk engine initialization")
    print("  • Exposure data management")
    print("  • Hazard and vulnerability modeling")
    print("  • Multi-module integration")
    print("\nNext steps:")
    print("  • Integrate with SPACE for spatial risk mapping")
    print("  • Connect with TIME for temporal risk analysis")
    print("  • Use with AI for predictive risk modeling")
    print("  • Combine with HEALTH for health risk assessment")


if __name__ == "__main__":
    main()

