module GUI.Lobby exposing (lobby)

import Dict
import GUI.Controls
import GUI.Text as Text
import Html exposing (Html, div)
import Html.Attributes as Attr
import Color exposing (Color)
import Players exposing (AllPlayers)
import Types.Player exposing (Player)
import Types.PlayerStatus exposing (PlayerStatus(..))


lobby : AllPlayers -> Html msg
lobby players =
    div
        [ Attr.id "lobby"
        ]
        (Dict.values players |> List.map playerEntry)


playerEntry : ( Player, PlayerStatus ) -> Html msg
playerEntry ( player, status ) =
    let
        ( left, right ) =
            GUI.Controls.showControls player
    in
    Html.div
        [ Attr.class "playerEntry" ]
        [ Html.div
            [ Attr.class "controls"
            ]
            (Text.string (Text.Size 4) player.color <| "(" ++ left ++ " " ++ right ++ ")")
        , Html.div
            [ Attr.style "visibility"
                (case status of
                    Participating _ ->
                        "visible"

                    NotParticipating ->
                        "hidden"
                )
            ]
            (Text.string (Text.Size 2) player.color "READY")
            , Html.img
            [
                if Color.toCssString player.color == "rgba(100%,15.69%,0%,1)" then Attr.src "./resources/stian.png" 
                    else if Color.toCssString player.color == "rgba(0%,79.61%,0%,1)" then Attr.src "./resources/adne.png"
                    else if Color.toCssString player.color == "rgba(76.47%,76.47%,0%,1)" then Attr.src "./resources/jonas.png"
                    else if Color.toCssString player.color == "rgba(87.45%,31.76%,71.37%,1)" then Attr.src "./resources/andreas.png"
                     else Attr.src "./resources/nikhil.png" ,
                Attr.class "icon"
            ]
            []
        ]
