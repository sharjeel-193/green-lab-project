plot_densityPlot_metric <- function(df, subject_name, metric, metric_label) {
  # Create a new factor for the interaction of treatment and iterations
  df$iterations <- factor(df$iterations, 
                          levels = c("100000", "10000000"), 
                          labels = c("100k", "10m"))  # Update labels for iterations
  
  df$interaction_group <- interaction(df$treatment, df$iterations)
  
  ggplot(df, aes(x = .data[[metric]], fill = interaction_group, color = interaction_group)) +
    geom_density(alpha = 0.5) +  # Add transparency to better visualize overlapping densities
    labs(title = paste("Density Plot for", subject_name, "-", metric_label),
         x = metric_label,
         y = "Density",
         fill = "Interaction Group",
         color = "Interaction Group"
         ) +
    theme_minimal() +
    facet_wrap(~ subject) +
    scale_x_log10() +  # Log scale for the x-axis (metric)
    theme(axis.text.x = element_text(angle = 45, hjust = 1)) +  # Adjust x-axis text for readability
    scale_fill_manual(values = c("Default Loop.100k" = "blue", 
                                 "Default Loop.10m" = "lightblue",
                                 "Loop Unrolling.100k" = "red", 
                                 "Loop Unrolling.10m" = "lightcoral",
                                 "Loop Unswitching.100k" = "green", 
                                 "Loop Unswitching.10m" = "yellow")) +  # Custom colors for treatments and iterations
    scale_color_manual(values = c("Default Loop.100k" = "blue", 
                                  "Default Loop.10m" = "lightblue",
                                  "Loop Unrolling.100k" = "red", 
                                  "Loop Unrolling.10m" = "lightcoral",
                                  "Loop Unswitching.100k" = "green", 
                                  "Loop Unswitching.10m" = "yellow"))  # Custom colors for treatments and iterations
}

cogvideo_density_plot <- plot_densityPlot_metric(cogvideo_data, "CogVideo", "energy_efficiency", "Energy Efficiency(J/ms)")
sherlock_density_plot <- plot_densityPlot_metric(sherlock_data, "Sherlock", "energy_efficiency", "Energy Efficiency(J/ms)")

