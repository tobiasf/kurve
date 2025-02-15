module GUI.SplashScreen exposing (splashScreen)

import Html exposing (Html, h1, div, text)
import Html.Attributes as Attr


splashScreen : Html msg
splashScreen =
    div [
         Attr.id "newSplash"
    ]
    [
    h1
        [
        ]
        [ text "Achtung, die Mindwave"]

    ]
