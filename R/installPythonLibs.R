library(reticulate)
version <- "3.11.7"
install_python(version = version)
virtualenv_create("python-session", python_version = version)
use_virtualenv("python-session",require = TRUE)
virtualenv_install(envname = "python-session","pandas",ignore_installed = FALSE,pip_options = character())
virtualenv_install(envname = "python-session","ipython",ignore_installed = FALSE,pip_options = character())
virtualenv_install(envname = "python-session","networkx",ignore_installed = FALSE,pip_options = character())
virtualenv_install(envname = "python-session","plotly",ignore_installed = FALSE,pip_options = character())
virtualenv_install(envname = "python-session","matplotlib",ignore_installed = FALSE,pip_options = character())

