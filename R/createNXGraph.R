library(reticulate)
createGraph <- function(df_location, phyla, about_location,
                            y_axis, y_axis_label, save_location) {

  py_run_file("Python/NXFunctions.py")

  py$createGraph(df_location, phyla, about_location,
                   y_axis, y_axis_label, save_location)
}


