# Data dictionary

The CSV schema contains 37 source columns. Confirm meanings and units from the Kaggle source documentation before treating names as definitive definitions. The pipeline adds `source_split` (`train` / `test`) and `efficiency_kwh_per_100km`.

| Column | Expected meaning / unit | Notes |
|---|---|---|
| `vehicle_id` | Vehicle record identifier | Used as the deduplication key. |
| `model_name` | Model name | Text. |
| `manufacturer` | Manufacturer/brand label | Text category; values may be simulated. |
| `model_year` | Vehicle model year | Do not label as transaction/sales year. |
| `manufacturing_country` | Country label | Confirm whether this represents the actual manufacturing site. |
| `market_region` | Market region label | Confirm how publisher defines region. |
| `category` | Vehicle category | Text category. |
| `battery_capacity_kwh` | Battery capacity (kWh) | Numeric measure. |
| `battery_type` | Battery technology label | Examples in supplied file include NMC, LFP, NCA, Sodium-Ion, Solid-State. |
| `battery_cycle_life` | Battery cycle life | Source unit/definition should be checked. |
| `battery_degradation_pct_5yr` | Five-year battery degradation percentage | Validate percent scale in the source docs. |
| `range_km` | Driving range (km) | Source method and testing conditions may be unknown. |
| `efficiency_wh_per_km` | Efficiency (Wh/km) | Derived conversion is `efficiency_wh_per_km / 10` kWh/100 km. |
| `motor_power_kw` | Motor power (kW) | Numeric measure. |
| `torque_nm` | Torque (Nm) | Numeric measure. |
| `num_motors` | Motor count | Count. |
| `drivetrain` | Drivetrain category | Text. |
| `top_speed_kmph` | Top speed (km/h) | Numeric measure. |
| `acceleration_0_100_sec` | 0–100 km/h acceleration time (seconds) | Numeric measure. |
| `max_dc_charging_kw` | Maximum DC charging power (kW) | Numeric measure. |
| `charging_dc_fast_time_min` | DC fast-charge duration (minutes) | Validate start/end charge levels in source documentation. |
| `charging_ac_time_hr` | AC charging duration (hours) | Validate charging conditions in source docs. |
| `num_charging_ports` | Charging port count | Count. |
| `num_seats` | Seating capacity | Count. |
| `weight_kg` | Vehicle weight (kg) | Confirm curb/gross weight definition. |
| `cargo_capacity_liters` | Cargo capacity (litres) | Numeric measure. |
| `price_usd` | Price in US dollars | May not include taxes/trim/region differences. |
| `insurance_cost_usd_yearly` | Estimated annual insurance cost (USD/year) | Confirm methodology/source. |
| `warranty_years` | Warranty duration (years) | Numeric measure. |
| `resale_value_pct_3yr` | Resale value percentage after 3 years | Confirm base value and percentage scale. |
| `safety_rating_stars` | Safety rating in stars | Confirm rating authority and maximum scale. |
| `autonomous_level` | Autonomous driving level | Confirm whether it follows a recognized standard. |
| `infotainment_screen_inch` | Screen size (inches) | Numeric measure. |
| `co2_saved_tons_per_year` | Estimated CO₂ saved (tonnes/year) | Baseline assumptions need source documentation. |
| `annual_sales_units` | Annual sales units field | Validate grain and additivity before summing. |
| `customer_rating` | Customer rating | Scale and review count/source are not included as separate columns. |
| `recommended_use_case` | Recommended use-case label | Text category. |
| `source_split` | Added by pipeline: train/test | Records source CSV, not a business property. |
| `efficiency_kwh_per_100km` | Added by pipeline (kWh/100 km) | Equals `efficiency_wh_per_km / 10`. |
