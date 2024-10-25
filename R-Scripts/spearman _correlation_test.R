
# Function to compute Spearman correlation and approximate p-value for 'eb_time' with respect to 'energy_efficiency'
spearman_correlation_eb_time <- function(df, subject_name) {
  # Compute Spearman correlation and p-value for 'eb_time' against 'energy_efficiency'
  results <- df %>%
    group_by(iterations) %>%
    summarise(
      eb_time_correlation = ifelse(sd(eb_time, na.rm = TRUE) == 0 || sd(energy_efficiency, na.rm = TRUE) == 0,
                                   NA,
                                   cor(eb_time, energy_efficiency, method = "spearman")),
      eb_time_p_value = ifelse(sd(eb_time, na.rm = TRUE) == 0 || sd(energy_efficiency, na.rm = TRUE) == 0,
                               NA,
                               cor.test(eb_time, energy_efficiency, method = "spearman", exact = FALSE)$p.value),
      .groups = 'drop'  # Drop grouping
    )
  
  return(results)
}

# Apply the function to the CogVideo dataset
cogvideo_spearman_corr <- spearman_correlation_eb_time(cogvideo_data, "CogVideo")

# Apply the function to the Sherlock dataset
sherlock_spearman_corr <- spearman_correlation_eb_time(sherlock_data, "Sherlock")

