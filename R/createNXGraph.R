library(reticulate)
createGraph <- function(df_location, phyla, about_location,
                            y_axis, y_axis_label, save_location, gtype) {

  py_run_file("Python/NXFunctions.py")

  py$CreateNXGraph(df_location, phyla, about_location,
                   y_axis, y_axis_label, save_location, gtype)
}


