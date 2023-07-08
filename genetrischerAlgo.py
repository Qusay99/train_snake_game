from random import randint
from spielUmgebung import *
import numpy as np
import pandas as pd

# Durchführung der Vorwärtspropagation
def vorwaertpropagation(X, individuum: np.ndarray) -> np.ndarray:
    # Erstellung der Gewichtungsmatrixen aus dem individuum-Array
    M1_ende = matrix1_form[0] * matrix1_form[1]
    M2_start = M1_ende
    M2_ende = matrix2_form[0] * matrix2_form[1] + M1_ende
    M3_start = M2_ende
    M3_ende = M3_start + matrix3_form[0] * matrix3_form[1]

    matrix1 = individuum[:M1_ende].reshape(matrix1_form)
    matrix2 = individuum[M2_start:M2_ende].reshape(matrix2_form)
    matrix3 = individuum[M3_start:M3_ende].reshape(matrix3_form)

    # Berechnung der Zwischenergebnisse und Aktivierungsfunktionen
    hidden1_input = np.matmul(matrix1, X.T)
    hidden1_activation = np.tanh(hidden1_input)
    hidden2_input = np.matmul(matrix2, hidden1_activation)
    hidden2_activation = np.tanh(hidden2_input)
    output_input = np.matmul(matrix3, hidden2_activation)
    output_activation = np.exp(output_input.T) / np.sum(np.exp(output_input.T), axis=1)
    output_activation.reshape(-1, 1)

    return output_activation

def start_training(anzeige, uhr, gewichte, generation):
    max_punktzahl = 0
    test_spiele = 1
    tod_score = 0
    schritte_pro_spiel = 3000
    punktzahl2 = 0

    for _ in range(test_spiele):
        schlange_start, schlange_position, apfel_position, punktzahl = startposition()

        anzahl_gleiche_richtung = 0
        vorherige_richtung = 0

        for _ in range(schritte_pro_spiel):
            aktueller_richtungsvektor, ist_vorne_blockiert, ist_links_blockiert, ist_rechts_blockiert = blocked_directions(
                schlange_position)
            winkel, schlange_richtungsvektor, apfel_richtungsvektor_normalisiert, schlange_richtungsvektor_normalisiert = angle_with_apple(
                schlange_position, apfel_position)
            vorhersagen = []
            vorhergesagte_richtung = np.argmax(np.array(vorwaertpropagation(np.array(
                [ist_links_blockiert, ist_vorne_blockiert, ist_rechts_blockiert, apfel_richtungsvektor_normalisiert[0],
                 schlange_richtungsvektor_normalisiert[0], apfel_richtungsvektor_normalisiert[1],
                 schlange_richtungsvektor_normalisiert[1]]).reshape(-1, 7), gewichte))) - 1

            if vorhergesagte_richtung == vorherige_richtung:
                anzahl_gleiche_richtung += 1
            else:
                anzahl_gleiche_richtung = 0
                vorherige_richtung = vorhergesagte_richtung

            neue_richtung = np.array(schlange_position[0]) - np.array(schlange_position[1])
            if vorhergesagte_richtung == -1:
                neue_richtung = np.array([neue_richtung[1], -neue_richtung[0]])
            if vorhergesagte_richtung == 1:
                neue_richtung = np.array([-neue_richtung[1], neue_richtung[0]])

            richtung_taste = generate_button_direction(neue_richtung)

            naechster_schritt = schlange_position[0] + aktueller_richtungsvektor
            if boundaries_collision(schlange_position[0]) == 1 or collision_with_self(naechster_schritt.tolist(),
                                                                                               schlange_position) == 1:
                tod_score += -150
                break

            else:
                tod_score += 0

            schlange_position, apfel_position, punktzahl = play_game(schlange_start, schlange_position, apfel_position,
                                                                       richtung_taste, punktzahl, anzeige, uhr, generation)

            if punktzahl > max_punktzahl:
                max_punktzahl = punktzahl

            if anzahl_gleiche_richtung > 8 and vorhergesagte_richtung != 0:
                punktzahl2 -= 1
            else:
                punktzahl2 += 2
    belohnung = tod_score + punktzahl2 + (max_punktzahl * 5000)


    return belohnung, punktzahl


def berechne_fitness(werte,generation):
    # Berechnung des Fitnesswerts durch Spielen eines Spiels mit den gegebenen Gewichten im Chromosom
    fitness = []
    punktzahl_liste = []
    for i in range(werte.shape[0]):
        fit, punktzahl = start_training(display, clock, werte[i], generation)
        fitness.append(fit)
        punktzahl_liste.append(punktzahl)
    return np.array(fitness), np.array(punktzahl_liste)


def eltern_finden(population, fitness, anzahl_eltern):
    # Auswahl der besten Individuen in der aktuellen Generation als Eltern für die Erzeugung der Nachkommen in der nächsten Generation.
    eltern = np.empty((anzahl_eltern, population.shape[1]))
    for eltern_num in range(anzahl_eltern):
        max_fitness_idx = np.where(fitness == np.max(fitness))
        max_fitness_idx = max_fitness_idx[0][0]
        eltern[eltern_num, :] = population[max_fitness_idx, :]
        fitness[max_fitness_idx] = -99999999
    return eltern


def kreuzung(eltern, nachkommen_groeße):
    # Erzeugung von Nachkommen für die nächste Generation
    nachkommen = np.empty(nachkommen_groeße)
    
    for k in range(nachkommen_groeße[0]): 
  
        while True:
            eltern1_idx = random.randint(0, eltern.shape[0] - 1)
            eltern2_idx = random.randint(0, eltern.shape[0] - 1)
            # Nachkommen erzeugen, wenn die beiden Eltern unterschiedlich sind
            if eltern1_idx != eltern2_idx:
                for j in range(nachkommen_groeße[1]):
                    if random.uniform(0, 1) < 0.5:
                        nachkommen[k, j] = eltern[eltern1_idx, j]
                    else:
                        nachkommen[k, j] = eltern[eltern2_idx, j]
                break
    return nachkommen



def mutation(nachkommen_kreuzung):
    # Mutation der aus der Kreuzung erzeugten Nachkommen, um Variation in der Population zu erhalten
    
    for idx in range(nachkommen_kreuzung.shape[0]):
        for _ in range(25):
            i = randint(0, nachkommen_kreuzung.shape[1]-1)

        random_value = np.random.choice(np.arange(-1, 1, step=0.05), size=(1), replace=False)
        nachkommen_kreuzung[idx, i] = nachkommen_kreuzung[idx, i] + random_value

    return nachkommen_kreuzung

input_layer = 7
hidden_layer1 = 9
hidden_layer2 = 15
output_layer = 3

matrix1_form = (hidden_layer1,input_layer)
matrix2_form = (hidden_layer2,hidden_layer1)
matrix3_form = (output_layer,hidden_layer2)

df = pd.DataFrame(columns=["generation","gen_highest_Fitness","gen_higest_score"])

sol_per_pop = 50
num_weights = input_layer * hidden_layer1 + hidden_layer1* hidden_layer2 + hidden_layer2*output_layer

# Defining the population size.
pop_size = (sol_per_pop,num_weights)
#Creating the initial population.
new_population = np.random.choice(np.arange(-1,1,step=0.01),size=pop_size,replace=True)

num_generations = 200

# Berechnung der Anzahl der Eltern, die ausgewählt werden sollen (20% der Populationsgröße)
num_parents_mating = int(0.2 * pop_size[0])
for generation in range(num_generations):
    print('Generation:\t', generation)
    # Measuring the fitness of each chromosome in the population.
    fitness, punktzahl = berechne_fitness(new_population, generation)
    df = df.append({"generation":generation,"gen_highest_Fitness":np.max(fitness),"gen_higest_score": np.max(punktzahl)}, ignore_index=True)
    print('Höchst ereichter Fitnesswert:\t', np.max(fitness))
    # Selecting the best parents in the population for mating.
    eltern = eltern_finden(new_population, fitness, num_parents_mating)

    # Generating next generation using crossover.
    nachfolger_crossover = kreuzung(eltern, nachkommen_groeße=(pop_size[0] - eltern.shape[0], num_weights))

    # Adding some variations to the offsrping using mutation.
    offspring_mutation = mutation(nachfolger_crossover)

    # Creating the new population based on the parents and offspring.
    new_population[0:eltern.shape[0], :] = eltern
    new_population[eltern.shape[0]:, :] = offspring_mutation

print("Übersicht der gesammelten Daten:\t", df.info())

df.to_csv('training_protokoll.csv', index=False)