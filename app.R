library(dash)
library(dashHtmlComponents)
library(dashCoreComponents)
library(tidyverse)



app = Dash$new(external_stylesheets = "https://codepen.io/chriddyp/pen/bWLwgP.css")

app$layout(htmlDiv(
  list(
    dccDropdown(
      options = list(list(label = "Data Scientist", value = "DS"))
    ))))

app$run_server(debg = T)