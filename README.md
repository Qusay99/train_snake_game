Dieses Repository beinhaltet die Implementierung eines evolutionären Algorithmus zur Optimierung der Spielleistung eines Snake-Games mithilfe von neuronalen Netzwerken.

Verwendete Methoden:

- **Evolutionärer Algorithmus:** Der Algorithmus simuliert die natürliche Evolution und nutzt dabei Selektion, Kreuzung und Mutation, um eine bessere Lösung für ein gegebenes Optimierungsproblem zu finden. In diesem Fall wird der Algorithmus verwendet, um die besten Gewichtungen für das neuronale Netzwerk zu identifizieren.
- **Vorwärtspropagation:** Die Vorwärtspropagation ist der Prozess, bei dem die Eingabedaten durch das neuronale Netzwerk propagiert werden, um die Ausgabe zu generieren. Hier wird sie verwendet, um die Vorhersagen der KI basierend auf den aktuellen Gewichtungen zu erhalten.

Während der Implementierung wurde einige Einstellungen für den Algorihtmus folgendem Paper entnommen: https://ceur-ws.org/Vol-2468/p9.pdf

Im Verlauf der Entwicklungs- und Evaluierungsphasen wurden diverse Fitnessfunktionen implementiert und einer gründlichen Prüfung unterzogen. In der abschließenden Phase erfolgte die Selektion der optimalen Fitnessfunktion, gefolgt von mehreren Evaluierungsdurchgängen. Hervorzuheben ist, dass nur die unten dargestellten Evaluierungsdurchgänge protokolliert wurden, da bei ihnen bedeutende Leistungsdisparitäten infolge der Parameteranpassungen beobachtet wurden.

<p align="center">
  <img src="https://github.com/Qusay99/train_snake_game/blob/main/eval_img/evaluation.png" align="center" width=65% height=50%>
</p>

Die Ergebnisse nach Erhöhung der Populationsgröße:

<p align="center">
  <img src="https://github.com/Qusay99/train_snake_game/blob/main/eval_img/evaluation2.png" align="center" width=65% height=50%>
</p>

## Quellen:
- https://www.youtube.com/watch?v=5KsZte3DXW8
- https://www.youtube.com/watch?v=xbDPEOgX3n8
- https://www.youtube.com/watch?v=SGxVaptD9Ug
- https://towardsdatascience.com/introduction-to-genetic-algorithms-including-example-code-e396e98d8bf3
- https://theailearnee.com/2018/11/09/snake-game-with-geneticalgorithm/
- https://davideliu.com/2020/02/03/teaching-ai-to-play-snake-with-genetic-algorithm/
- https://blog.devgenius.io/i-finally-made-a-neural-network-that-learns-snake-in-python-4ba9f3975783
- https://towardsdatascience.com/training-a-snake-game-ai-a-literature-review-1cdddcd1862f
