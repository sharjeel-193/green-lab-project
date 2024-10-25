# Load the data
data <- read.csv("run_table.csv")

# Create a new column for Energy Efficiency (J/ms)
data <- data %>%
  mutate(energy_efficiency = total_cpu_energy / (eb_time))

print(data)

# Group by subject, treatment, and iterations, then calculate the average energy efficiency
average_efficiency <- data %>%
  group_by(subject, treatment, iterations) %>%
  summarise(average_energy_efficiency = mean(energy_efficiency, na.rm = TRUE), .groups = 'drop')

print(average_efficiency)

# Reshape the table to have separate columns for Default Loop and Optimized Loop efficiency
average_efficiency_wide <- average_efficiency %>%
  pivot_wider(names_from = treatment, 
              values_from = average_energy_efficiency, 
              names_prefix = "avg_efficiency_with_")

# Rename columns to improve readability
colnames(average_efficiency_wide) <- c("subject", "iterations", 
                                       "avg_efficiency_with_default_loop", 
                                       "avg_efficiency_with_optimized_loop")

# Display the result
print(average_efficiency_wide)


# Split the data into separate datasets for CogVideo and Sherlock
cogvideo_data <- data %>% filter(subject == "CogVideo")
sherlock_data <- data %>% filter(subject == "Sherlock")
