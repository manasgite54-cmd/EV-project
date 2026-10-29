# Tableau Story storyboard

Use the following outline to author the Tableau Story. Replace any prompts with findings actually verified in the workbook.

## Scene 1 — What is in this dataset?
- **Question:** What vehicle records, model years, manufacturers, categories, and regions are covered?
- **View:** KPI summary + record count by model year/category.
- **Narrative:** State source, date coverage, row count, and whether the dataset is synthetic/simulated/real according to its source documentation.
- **Caution:** Model year is not the same thing as transaction year.

## Scene 2 — How do manufacturers compare?
- **Question:** How do manufacturers compare by record count and recorded sales field?
- **View:** Sorted manufacturer bar chart.
- **Narrative:** Report the top groups and exact measurement used.
- **Caution:** Do not state “market leader” or market share based on record count alone. Confirm whether annual sales values are additive.

## Scene 3 — How do battery technologies differ?
- **Question:** What battery types appear, and what range/capacity/degradation patterns are observed?
- **View:** Battery mix + range/capacity scatter or box plot.
- **Narrative:** Describe the spread and group averages with sample counts.
- **Caution:** Correlation is not causation; missing measurements affect group sizes.

## Scene 4 — What is the observed price-range relationship?
- **Question:** How does price vary across ranges and vehicle categories?
- **View:** Price versus range scatter with category/manufacturer filters.
- **Narrative:** Report descriptive patterns and notable outliers.
- **Caution:** Price in USD may not reflect taxes, geography, model trim, or comparable ownership costs.

## Scene 5 — What varies by country, region, and category?
- **Question:** How are records distributed across manufacturing countries and market regions?
- **View:** Country/region bar chart or appropriately validated map.
- **Narrative:** Describe represented records and group differences.
- **Caution:** Manufacturing location does not necessarily equal market of sale.

## Scene 6 — What can a decision-maker conclude?
- **Question:** Which follow-up questions or strategic areas merit deeper investigation?
- **View:** Summary dashboard and key metrics.
- **Narrative:** Present 2–4 findings backed by values and sample sizes, followed by practical next steps.
- **Caution:** List limitations, incomplete fields, source reliability, and non-causal nature of comparisons.

## Final story review

- [ ] All numbers were copied from the final workbook/query, not invented.
- [ ] Every chart has a title, measure, unit where relevant, and understandable axes.
- [ ] Samples and missing values are disclosed where they affect interpretation.
- [ ] Source provenance and license are documented.
- [ ] The final scene includes limitations and next steps.
