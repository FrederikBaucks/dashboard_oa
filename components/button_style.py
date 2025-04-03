roundbutton =   {
    "border": None,
   # "border-radius": "50%",
    "padding": 0 ,
   # "color": "black",
    "textAlign": "center",
    "display": 'inline-block',
    "fontSize": "80%",
    "height": "70%",
    "width": "100%",
}

roundbutton_raw_data =   {
    "border": None,
   # "border-radius": "50%",
    "padding": 0 ,
   # "color": "black",
    "textAlign": "center",
    "display": 'inline-block',
    "fontSize": "80%",
    "height": "70%",
    "width": "24%",
    "margin-left": "75%"
}
import dash_bootstrap_components as dbc

help_modal = dbc.Modal(
    [
        dbc.ModalHeader("Help"),
        dbc.ModalBody("Your help text goes here."),
        dbc.ModalFooter(
            dbc.Button("Close", id="close", className="ml-auto")
        ),
    ],
    id="modal",
    is_open=False,  # True: open the modal; False: close the modal
    size="sm",  # "sm", "lg", "xl" -> small, large, extra large
    backdrop="static",  # "static" for a backdrop that doesn't close the modal on click.
    centered=True,  # To center the modal vertically in the page.
)