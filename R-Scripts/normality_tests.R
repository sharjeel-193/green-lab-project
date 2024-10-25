# Load necessary libraries
library(tidyverse)



# Function to compute Shapiro-Wilk test for each metric in each combination of treatment and iterations
shapiro_test_by_group <- function(df, metrics) {
  df %>%
    group_by(treatment, iterations) %>%
    summarise(across(all_of(metrics), 
                     ~ shapiro.test(.x)$p.value, 
                     .names = "shapiro_p_{.col}"),
              .groups = 'drop')  # Drop group column after summarising
}

# Define the list of metrics you want to test
metrics <- c("eb_time", 
             "total_cpu_energy", "average_cpu_usage", 
             "used_memory")

# Compute Shapiro-Wilk test p-values for CogVideo
cogvideo_shapiro <- shapiro_test_by_group(cogvideo_data, metrics)

# Compute Shapiro-Wilk test p-values for Sherlock
sherlock_shapiro <- shapiro_test_by_group(sherlock_data, metrics)

# Function to perform Kruskal-Wallis test for multiple metrics
kruskal_wallis_tests <- function(df, subject_name) {
  metrics <- c("eb_time", "total_cpu_energy", "average_cpu_usage", "used_memory")
  
  # Loop through each metric and perform Kruskal-Wallis test
  results <- df %>%
    group_by(treatment, iterations) %>%
    summarise(
      across(all_of(metrics), ~kruskal.test(.x ~ interaction(treatment, iterations))$p.value, 
             .names = "kruskal_p_{.col}")
    )
  
  # Return results
  return(results)
}

# Compute Kruskal-Wallis test p-values for CogVideo
cogvideo_kruskal <- kruskal_test_by_group(cogvideo_data, metrics)

# Compute Kruskal-Wallis test p-values for Sherlock
sherlock_kruskal <- kruskal_test_by_group(sherlock_data, metrics)

