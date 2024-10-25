# Load necessary libraries
library(ggplot2)
library(tidyr)  # For data reshaping
library(dplyr)  # For data manipulation

# Assume your cogvideo_data and sherlock_data dataframes are already loaded

# Reshape the data for Sherlock
long_df_sherlock <- sherlock_data %>%
  pivot_longer(cols = c(eb_time, total_cpu_energy, average_cpu_usage, used_memory),
               names_to = "metric", 
               values_to = "value")

# Define a named vector for metric labels
metric_labels <- c(
  eb_time = "Execution Time (ms)",
  total_cpu_energy = "Total CPU Energy (J)",
  average_cpu_usage = "Average CPU Usage (%)",
  used_memory = "Used Memory (B)"
)

# Update the 'metric' column with new labels for Sherlock
long_df_sherlock$metric <- factor(long_df_sherlock$metric, levels = names(metric_labels), labels = metric_labels)

# Convert iterations to factors with custom labels for Sherlock
long_df_sherlock$iterations <- factor(long_df_sherlock$iterations, 
                                      levels = c("100000", "10000000"), 
                                      labels = c("100k Iterations", "10m Iterations"))

# Create the QQ plot for Sherlock
qq_plot_sherlock <- ggplot(long_df_sherlock, aes(sample = value, color = interaction(treatment, iterations))) +
  stat_qq() +
  stat_qq_line() +
  facet_wrap(~ metric, scales = "free_y") +  # Facet by metric
  labs(title = "QQ Plots for Sherlock - Each Metric",
       x = "Theoretical Quantiles", 
       y = "Sample Quantiles") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1),
        legend.position = "top",  # Move legend to the top
        legend.title = element_blank())  # Optional: remove legend title if desired

# Reshape the data for CogVideo
long_df_cogvideo <- cogvideo_data %>%
  pivot_longer(cols = c(eb_time, total_cpu_energy, average_cpu_usage, used_memory),
               names_to = "metric", 
               values_to = "value")

# Update the 'metric' column with new labels for CogVideo
long_df_cogvideo$metric <- factor(long_df_cogvideo$metric, levels = names(metric_labels), labels = metric_labels)

# Convert iterations to factors with custom labels for CogVideo
long_df_cogvideo$iterations <- factor(long_df_cogvideo$iterations, 
                                      levels = c("100000", "10000000"), 
                                      labels = c("100k Iterations", "10m Iterations"))

# Create the QQ plot for CogVideo
qq_plot_cogvideo <- ggplot(long_df_cogvideo, aes(sample = value, color = interaction(treatment, iterations))) +
  stat_qq() +
  stat_qq_line() +
  facet_wrap(~ metric, scales = "free_y") +  # Facet by metric
  labs(title = "QQ Plots for CogVideo - Each Metric",
       x = "Theoretical Quantiles", 
       y = "Sample Quantiles") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1),
        legend.position = "top",  # Move legend to the top
        legend.title = element_blank())  # Optional: remove legend title if desired

# Optionally, you can print the plots
# print(qq_plot_sherlock)
# print(qq_plot_cogvideo)

# You can also save them using ggsave
# ggsave("qq_plot_sherlock.png", plot = qq_plot_sherlock, width = 10, height = 6)
# ggsave("qq_plot_cogvideo.png", plot = qq_plot_cogvideo, width = 10, height = 6)
