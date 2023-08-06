import { ConfigurationData } from "../configuration/types";

export const WORLD_POPULATION_DATA: ConfigurationData = {
  id: "735ccdf3-c77c-4558-baa3-99495082b77e",
  name: "Example dataset with world population",
  parameters: ["Age"],
  measurements: ["Female", "Male"],
  data: `Age,Female,Male
0-4,327.601,350.321
5-9,316.714,338.892
10-14,301.011,322.363
15-19,288.482,308.333
20-24,287.820,306.100
25-29,298.802,313.635
30-34,284.628,294.299
35-39,254.272,260.623
40-44,241.212,246.733
45-49,232.150,235.016
50-54,210.913,210.672
55-59,180.543,176.861
60-64,156.485,149.018
65-69,124.190,113.766
70-74,87.781,76.413
75-79,65.132,52.196
80-84,44.715,31.985
85-89,24.933,15.256
90-94,10.710,5.262
95-99,2.851,1.087
100+,0.384,0.102
`,
};
