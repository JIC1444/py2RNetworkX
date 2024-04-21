library(reticulate)
createGraph <- function(df_location, phyla, about_location, save_location) {

  py_run_file("Python/NXFunctions.py")

  py$createGraph(df_location, phyla, about_location, save_location)
}


