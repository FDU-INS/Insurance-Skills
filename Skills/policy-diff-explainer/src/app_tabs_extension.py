"""
Extended Tab Rendering Functions for PolicyPulse
Citizens, Groups, Experts, and Analytics tabs
"""

# This file contains the new tab functions that will be added to app.py
# Copy these functions into app.py after the render_time_series_tab function

def render_citizens_tab(result):
    """Render Citizens tab with detailed individual citizen analysis."""
    import streamlit as st
    import pandas as pd
    import plotly.express as px
    from src.data_models import IncomeLevel, CityZone, PoliticalView
    
    st.markdown('<div class="section-header">👤 Citizens Deep Dive</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="metric-card" style="border-left-color: #3b82f6;">
        <h4 style="margin-top: 0;">🔍 Individual Citizen Analysis</h4>
        <p>Explore how individual citizens responded to the policy based on their unique characteristics and circumstances.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get final states
    final_step = result.config.steps
    final_states = result.states_by_step.get(final_step, [])
    initial_states = result.states_by_step.get(0, [])
    
    # Create lookup dictionaries
    final_state_map = {s.citizen_id: s for s in final_states}
    initial_state_map = {s.citizen_id: s for s in initial_states}
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        income_filter = st.multiselect(
            "Filter by Income Level",
            options=[level.value for level in IncomeLevel],
            default=[level.value for level in IncomeLevel],
            key="citizens_income_filter"
        )
    
    with col2:
        zone_filter = st.multiselect(
            "Filter by City Zone",
            options=[zone.value for zone in CityZone],
            default=[zone.value for zone in CityZone],
            key="citizens_zone_filter"
        )
    
    with col3:
        political_filter = st.multiselect(
            "Filter by Political View",
            options=[view.value for view in PoliticalView],
            default=[view.value for view in PoliticalView],
            key="citizens_political_filter"
        )
    
    # Filter citizens
    filtered_citizens = [
        c for c in result.citizens
        if c.income_level.value in income_filter
        and c.city_zone.value in zone_filter
        and c.political_view.value in political_filter
    ]
    
    st.markdown(f"**Showing {len(filtered_citizens):,} of {len(result.citizens):,} citizens**")
    
    st.divider()
    
    # Citizen Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_happiness_change = sum(
            final_state_map.get(c.id, initial_state_map.get(c.id)).happiness - 
            initial_state_map.get(c.id).happiness
            for c in filtered_citizens if c.id in final_state_map and c.id in initial_state_map
        ) / max(len(filtered_citizens), 1)
        st.metric("Avg Happiness Change", f"{avg_happiness_change:+.1%}")
    
    with col2:
        avg_support = sum(
            final_state_map.get(c.id, initial_state_map.get(c.id)).policy_support
            for c in filtered_citizens if c.id in final_state_map
        ) / max(len(filtered_citizens), 1)
        st.metric("Avg Policy Support", f"{avg_support:+.1%}")
    
    with col3:
        positive_count = sum(
            1 for c in filtered_citizens 
            if c.id in final_state_map and final_state_map[c.id].policy_support > 0
        )
        st.metric("Supporters", f"{positive_count:,} ({positive_count/max(len(filtered_citizens), 1):.0%})")
    
    with col4:
        negative_count = sum(
            1 for c in filtered_citizens 
            if c.id in final_state_map and final_state_map[c.id].policy_support < 0
        )
        st.metric("Opponents", f"{negative_count:,} ({negative_count/max(len(filtered_citizens), 1):.0%})")
    
    st.divider()
    
    # Scatter plot: Age vs Happiness Change
    st.markdown("### 📊 Citizen Response Patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        scatter_data = []
        for c in filtered_citizens[:500]:  # Limit for performance
            if c.id in final_state_map and c.id in initial_state_map:
                happiness_change = final_state_map[c.id].happiness - initial_state_map[c.id].happiness
                scatter_data.append({
                    "Age": c.age,
                    "Happiness Change": happiness_change * 100,
                    "Income Level": c.income_level.value,
                    "Support": final_state_map[c.id].policy_support
                })
        
        if scatter_data:
            df_scatter = pd.DataFrame(scatter_data)
            fig = px.scatter(
                df_scatter,
                x="Age",
                y="Happiness Change",
                color="Income Level",
                size=abs(df_scatter["Support"]) * 100 + 5,
                hover_data=["Support"],
                color_discrete_map={"Low": "#ef4444", "Middle": "#f59e0b", "High": "#22c55e"},
                title="Age vs Happiness Change (Size = Support Strength)"
            )
            fig.update_layout(height=400, margin=dict(t=40, b=40, l=40, r=40))
            st.plotly_chart(fig, key="citizens_age_happiness_scatter", use_container_width=True)
    
    with col2:
        # Income vs Support
        scatter_data2 = []
        for c in filtered_citizens[:500]:
            if c.id in final_state_map:
                scatter_data2.append({
                    "Income": c.income,
                    "Policy Support": final_state_map[c.id].policy_support * 100,
                    "Political View": c.political_view.value,
                    "Happiness": final_state_map[c.id].happiness
                })
        
        if scatter_data2:
            df_scatter2 = pd.DataFrame(scatter_data2)
            fig = px.scatter(
                df_scatter2,
                x="Income",
                y="Policy Support",
                color="Political View",
                size=df_scatter2["Happiness"] * 100 + 5,
                hover_data=["Happiness"],
                title="Income vs Policy Support (Size = Happiness)"
            )
            fig.update_layout(height=400, margin=dict(t=40, b=40, l=40, r=40))
            st.plotly_chart(fig, key="citizens_income_support_scatter", use_container_width=True)
    
    st.divider()
    
    # Detailed Citizens Table
    st.markdown("### 📋 Detailed Citizen Records")
    
    # Build detailed dataframe
    detailed_data = []
    for c in filtered_citizens[:100]:  # Show top 100
        if c.id in final_state_map and c.id in initial_state_map:
            from src.utils import format_currency
            initial = initial_state_map[c.id]
            final = final_state_map[c.id]
            detailed_data.append({
                "ID": c.id,
                "Age": c.age,
                "Gender": c.gender,
                "Income": c.income,
                "Income Level": c.income_level.value,
                "Zone": c.city_zone.value,
                "Political": c.political_view.value,
                "Profession": c.profession,
                "Education": f"{c.education_years}y",
                "Family": c.family_size,
                "Initial Happiness": initial.happiness,
                "Final Happiness": final.happiness,
                "Happiness Δ": final.happiness - initial.happiness,
                "Support": final.policy_support,
            })
    
    if detailed_data:
        df_detailed = pd.DataFrame(detailed_data)
        st.dataframe(
            df_detailed.style.format({
                "Income": "${:,.0f}",
                "Initial Happiness": "{:.1%}",
                "Final Happiness": "{:.1%}",
                "Happiness Δ": "{:+.1%}",
                "Support": "{:+.1%}",
            }).background_gradient(cmap='RdYlGn', subset=['Happiness Δ', 'Support']),
            use_container_width=True,
            hide_index=True,
            height=400
        )
