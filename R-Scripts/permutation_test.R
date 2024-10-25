
# Function for performing separate permutation tests
perform_separate_permutation_tests <- function(df, metric, subject_name) {
  df <- df %>%
    filter(tolower(subject) == tolower(subject_name))  # Case insensitive filtering
  
  # Convert treatment and iterations to factors
  df$treatment <- factor(df$treatment)
  df$iterations <- factor(df$iterations)
  
  # Create a formula for each test
  formulas <- list(
    treatment = as.formula(paste(metric, "~ treatment")),
    iterations = as.formula(paste(metric, "~ iterations")),
    interaction = as.formula(paste(metric, "~ treatment * iterations"))
  )
  
  results <- list()
  
  # Perform the permutation test for each formula
  for (test_name in names(formulas)) {
    # Perform the permutation test
    perm_test <- independence_test(formulas[[test_name]], data = df, distribution = approximate(nresample = 10000))  # 10,000 permutations
    
    # Extract the statistic and p-value
    test_statistic <- statistic(perm_test)  # Use statistic() to extract the test statistic
    p_value <- pvalue(perm_test)  # Use pvalue() to extract the p-value
    
    # Save results in a data frame
    results[[test_name]] <- data.frame(
      Test = paste("Permutation Test for", subject_name, "-", test_name),
      MaxT = test_statistic,
      P_Value = p_value
    )
  }
  
  # Combine results into one data frame
  combined_results <- do.call(rbind, results)
  
  return(combined_results)
}

# Run the separate permutation tests for Sherlock and CogVideo
results_sherlock <- perform_separate_permutation_tests(sherlock_data, "energy_efficiency", "Sherlock")
results_cogvideo <- perform_separate_permutation_tests(cogvideo_data, "energy_efficiency", "CogVideo")

# Combine results
final_results <- rbind(results_sherlock, results_cogvideo)

# Export to CSV
write.csv(final_results, "separate_permutation_test_results.csv", row.names = FALSE)

# Print message
cat("Separate permutation test results exported to 'separate_permutation_test_results.csv'.\n")
