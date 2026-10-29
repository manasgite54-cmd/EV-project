-- Electric Vehicle Market Performance & Insights
-- Run after the data pipeline has loaded ev_vehicles.
-- These queries are written for MySQL 8+; SQLite users can run most SELECTs
-- after changing any engine-specific syntax if needed.

-- 1. Table and date coverage
SELECT COUNT(*) AS vehicle_records,
       COUNT(DISTINCT vehicle_id) AS unique_vehicle_ids,
       MIN(model_year) AS first_model_year,
       MAX(model_year) AS latest_model_year
FROM ev_vehicles;

-- 2. Executive summary metrics
SELECT COUNT(*) AS records,
       COUNT(DISTINCT manufacturer) AS manufacturers,
       ROUND(AVG(range_km), 1) AS average_range_km,
       ROUND(AVG(battery_capacity_kwh), 1) AS average_battery_capacity_kwh,
       ROUND(AVG(customer_rating), 2) AS average_customer_rating,
       SUM(annual_sales_units) AS sum_of_recorded_sales_values
FROM ev_vehicles;
-- Caution: only interpret SUM(annual_sales_units) as market-wide units if the
-- dataset's documentation confirms records are additive and not repeated model-level snapshots.

-- 3. Manufacturer-level recorded sales and vehicle profile
SELECT manufacturer,
       COUNT(*) AS vehicle_records,
       SUM(annual_sales_units) AS recorded_sales_sum,
       ROUND(AVG(range_km), 1) AS avg_range_km,
       ROUND(AVG(price_usd), 0) AS avg_price_usd,
       ROUND(AVG(customer_rating), 2) AS avg_customer_rating
FROM ev_vehicles
GROUP BY manufacturer
ORDER BY recorded_sales_sum DESC;

-- 4. Annual recorded sales pattern
SELECT model_year,
       SUM(annual_sales_units) AS recorded_sales_sum,
       COUNT(*) AS vehicle_records
FROM ev_vehicles
GROUP BY model_year
ORDER BY model_year;
-- model_year is the vehicle model year, not necessarily the sales transaction year.

-- 5. Category comparison
SELECT category, COUNT(*) AS vehicle_records,
       ROUND(AVG(range_km), 1) AS avg_range_km,
       ROUND(AVG(price_usd), 0) AS avg_price_usd,
       ROUND(AVG(customer_rating), 2) AS avg_customer_rating
FROM ev_vehicles
GROUP BY category
ORDER BY vehicle_records DESC;

-- 6. Battery technology distribution and performance
SELECT battery_type, COUNT(*) AS vehicle_records,
       ROUND(AVG(battery_capacity_kwh), 1) AS avg_battery_capacity_kwh,
       ROUND(AVG(range_km), 1) AS avg_range_km,
       ROUND(AVG(battery_cycle_life), 0) AS avg_cycle_life,
       ROUND(AVG(battery_degradation_pct_5yr), 2) AS avg_5yr_degradation_pct
FROM ev_vehicles
GROUP BY battery_type
ORDER BY vehicle_records DESC;

-- 7. Manufacturing-country distribution
SELECT manufacturing_country, COUNT(*) AS vehicle_records,
       COUNT(DISTINCT manufacturer) AS manufacturers,
       ROUND(AVG(price_usd), 0) AS avg_price_usd,
       ROUND(AVG(range_km), 1) AS avg_range_km
FROM ev_vehicles
GROUP BY manufacturing_country
ORDER BY vehicle_records DESC;

-- 8. Market-region comparison
SELECT market_region, COUNT(*) AS vehicle_records,
       SUM(annual_sales_units) AS recorded_sales_sum,
       ROUND(AVG(customer_rating), 2) AS avg_customer_rating
FROM ev_vehicles
GROUP BY market_region
ORDER BY recorded_sales_sum DESC;

-- 9. Driving range versus battery capacity; use as a scatter plot source
SELECT vehicle_id, manufacturer, model_name, category, battery_type,
       battery_capacity_kwh, range_km, efficiency_wh_per_km,
       efficiency_kwh_per_100km, price_usd
FROM ev_vehicles
WHERE battery_capacity_kwh IS NOT NULL AND range_km IS NOT NULL;

-- 10. Value/price comparison (not a judgment about quality)
SELECT vehicle_id, manufacturer, model_name, category,
       price_usd, range_km,
       ROUND(price_usd / NULLIF(range_km, 0), 2) AS price_usd_per_km_range,
       customer_rating
FROM ev_vehicles
WHERE price_usd IS NOT NULL AND range_km > 0;

-- 11. Data quality audit
SELECT 'customer_rating' AS field_name, COUNT(*) AS missing_count
FROM ev_vehicles WHERE customer_rating IS NULL
UNION ALL
SELECT 'annual_sales_units', COUNT(*) FROM ev_vehicles WHERE annual_sales_units IS NULL
UNION ALL
SELECT 'battery_cycle_life', COUNT(*) FROM ev_vehicles WHERE battery_cycle_life IS NULL
UNION ALL
SELECT 'resale_value_pct_3yr', COUNT(*) FROM ev_vehicles WHERE resale_value_pct_3yr IS NULL;

-- 12. Candidate outlier review. Review, do not automatically delete.
SELECT vehicle_id, manufacturer, model_name, model_year, range_km,
       battery_capacity_kwh, price_usd, customer_rating
FROM ev_vehicles
WHERE range_km <= 0 OR battery_capacity_kwh <= 0
   OR price_usd <= 0 OR customer_rating < 0 OR customer_rating > 5;
