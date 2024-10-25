# Function to create individual box plots for multiple metrics with custom iteration labels
plot_boxplots_for_metrics <- function(df, subject_name, metrics) {
  # Update the iteration labels to custom ones for the entire dataframe
  df$iterations <- factor(df$iterations, levels = c("100000", "10000000"), labels = c("100k", "10m"))
  
  # Loop over each metric and create a box plot
  for (metric in metrics) {
    metric_label <- switch(metric,
                           "eb_time" = "Execution Time (ms)",
                           "average_cpu_usage" = "Average CPU Usage (%)",
                           "total_cpu_energy" = "Total CPU Energy (J)")
    
    # Create the box plot for the current metric
    p <- ggplot(df, aes(x = interaction(treatment, iterations), y = .data[[metric]], fill = treatment)) +
      geom_boxplot() +
      geom_jitter(width = 0.2) +
      labs(title = paste("Boxplot for", subject_name, "-", metric_label),
           x = "Treatment and Iterations",
           y = metric_label) +
      theme_minimal() +
      scale_y_log10() +  # Logarithmic y-scale for better readability
      scale_fill_manual(values = c("Default Loop" = "blue", "Loop Unrolling" = "red", "Loop Unswitching" = "green")) +
      theme(axis.text.x = element_text(angle = 45, hjust = 1))  # Rotate x-axis labels for clarity
    
    # Print or save the plot
    print(p)  # Print each plot to view individually
  }
}

# Example usage
plot_boxplots_for_metrics(cogvideo_data, "CogVideo", c("used_memory"))
