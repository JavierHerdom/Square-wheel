import pygad
import numpy
import streamlit as st


#Animated wheel.
def generateWheelMarkup(wheelMatrix):
    cssString = """
    .room {
      display: flex;
      flex-direction: column;
      margin: 10px;
    }
    .row {
      display: flex;
    }
    .cell {
      width: 20px;
      height: 20px;
      border: 1px solid black;
      display: flex;
      justify-content: center;
      align-items: center;
    }
    .protections {
      background-color: yellow;
      color: black;
    }
    .wheel {
      background-color: black;
    }
    .pinchazo {
      background-color: red;
    }
    .wheelCenter {
      background-color: white;
    }
    .spike {
      background-color: grey;
    }
    .roadBackground {
      background-color: white;
    }
    """
    htmlWrapperInit = f"<html><head></head><body><style>{cssString}</style>"
    htmlWrapperEnd = '</body></html>'

    roomWrapperInit = "<div class='room'>"
    roomWrapperEnd = "</div>"

    output = ""

    for i in range(len(wheelMatrix)):
        output += "<div class='row'>"
        for j in range(len(wheelMatrix[0])):
            roomCell = wheelMatrix[i][j]
            cellContent = ""
            if roomCell == 1:
                cellTypeClass = "protections"
                cellContent = 1
            elif roomCell == 0:
                cellTypeClass = "wheel"
                cellContent = 0
            elif roomCell == 2:
                cellTypeClass = "pinchazo"
                cellContent = 2
            elif roomCell == 3:
                cellTypeClass = "wheelCenter"
                cellContent = 3
            elif roomCell == "":
                cellTypeClass = "roadBackground"
                cellContent = ""
            elif roomCell == "X":
                cellTypeClass = "spike"
                cellContent = "X"


            output += f"<div class='{cellTypeClass} cell'>{cellContent}</div>"
        output += "</div>"

    return f"{htmlWrapperInit}{roomWrapperInit}{output}{roomWrapperEnd}{htmlWrapperEnd}"


#Streamlit functions.
def generar_pagina():
    # Generacion de la pagina web con Streamlit
    st.set_page_config(
        page_title="AG - Square wheel",
        page_icon="🔮"
    )

    st.write("# Genetic Algorithm - Square wheel.")
    st.markdown('by Javier Hernandez & Javier Valverde', unsafe_allow_html=True)

    with st.expander("🧙 Click here to learn more about this project 🧙"):
        st.markdown("""
            <p>For this work we will present the design of a square wheel with reinforcements which must make a revolution through a rocky road, in this case the square wheel will be a square of 7 x 7, and the road through which it must cross will be a rectangle that will have dimensions of 7 x 35, this road will have in its interior the so-called "stones" which will break the wheel, unless they run into the reinforced places of the wheel, which will not do any damage to them. Taking the above into account, this project seeks to use the least amount of reinforcements possible in the wheel, taking into account that it must cross this rocky road, this in order to save money and minimize material losses.</p>
        """, unsafe_allow_html=True)

    st.button("Start simulation", on_click=startProgram)

    # Declaro e inicializo componentes de pantalla que seran poblados mas adelante por el algoritmo
    global textHolder, roomHolder
    textHolder = st.empty()
    roomHolder = st.empty()


def page_set_summary_text(new_text):
    textHolder.markdown(new_text, unsafe_allow_html=True)


def page_set_room_preview(new_markup):
    roomHolder.markdown(new_markup, unsafe_allow_html=True)


#Aux functions.
bestWheel =[0, 0, 0, 0, []] #generation/fitness/protecciones/pinchazos/rueda
def callback_generation(ga_instance):
    global last_fitness, bestWheel
    print("Generation = {generation}".format(generation=ga_instance.generations_completed),
    ",  Fitness Best  = {fitness:.3f}".format(fitness=ga_instance.best_solution()[1]),
    ",  Change   = {change:.3f}".format(change=ga_instance.best_solution()[1] - last_fitness))
    page_set_summary_text(
        f"Generation: {ga_instance.generations_completed} Best fitness: {ga_instance.best_solution()[1]} Change: {ga_instance.best_solution()[1] - last_fitness}"
    )
    protecciones, pinchazos, newSolution = calcFitness(ga_instance.best_solution()[0], roadP1, roadP2, roadP3, roadP4)
    if ga_instance.best_solution()[1] > bestWheel[1]:
        bestWheel = [
            ga_instance.generations_completed,
            ga_instance.best_solution()[1],
            protecciones,
            pinchazos,
            newSolution
        ]
    page_set_room_preview(f"""
    {generateWheelMarkup(roadP1)} {generateWheelMarkup(roadP2)} {generateWheelMarkup(roadP3)} {generateWheelMarkup(roadP4)}
    Current gen best wheel has {protecciones} protections and {pinchazos} punctures and the solution looks like: \n{generateWheelMarkup(newSolution)}
    Best solution so far is in gen {bestWheel[0]}. The wheel has {bestWheel[2]} protections and {bestWheel[3]} punctures and looks like: \n{generateWheelMarkup(bestWheel[4])}
    """)
    last_fitness = ga_instance.best_solution()[1]


def countSolution(solution):
    protecciones = 0
    pinchazos = 0
    for n in solution:
        if n == 1:
            protecciones += 1
        elif n == 2:
            pinchazos += 1
    return protecciones, pinchazos


def readFile(file):
    roadP1 = list()
    roadP2 = list()
    roadP3 = list()
    roadP4 = list()
    file = open(file, "r")
    count = 0
    for line in file:
        line = line.replace('\n'," ")
        #Road P1
        checkColumn(line, 4, 0, 7, 3, roadP1, count)
        checkColumn(line, 3, 0, 7, 4, roadP1, count)
        checkColumn(line, 2, 0, 7, 5, roadP1, count)
        checkColumn(line, 1, 0, 7, 6, roadP1, count)
        #Road P2
        checkColumn(line, 4, 7, 14, 3, roadP2, count)
        checkColumn(line, 3, 7, 14, 4, roadP2, count)
        checkColumn(line, 2, 7, 14, 5, roadP2, count)
        checkColumn(line, 1, 7, 14, 6, roadP2, count)
        #Road P3
        checkColumn(line, 4, 14, 21, 3, roadP3, count)
        checkColumn(line, 3, 14, 21, 4, roadP3, count)
        checkColumn(line, 2, 14, 21, 5, roadP3, count)
        checkColumn(line, 1, 14, 21, 6, roadP3, count)
        #Road P4
        checkColumn(line, 4, 21, 28, 3, roadP4, count)
        checkColumn(line, 3, 21, 28, 4, roadP4, count)
        checkColumn(line, 2, 21, 28, 5, roadP4, count)
        checkColumn(line, 1, 21, 28, 6, roadP4, count)
        count += 1

    newRoadP1 = rotAnd2dRoad(roadP1)
    newRoadP2 = rotAnd2dRoad(roadP2)
    newRoadP3 = rotAnd2dRoad(roadP3)
    newRoadP4 = rotAnd2dRoad(roadP4)
    return newRoadP1, newRoadP2, newRoadP3, newRoadP4


def rotAnd2dRoad(road):
    newRoadP1 = buildArray(road)
    rotated = numpy.rot90(newRoadP1)
    return rotated


def checkColumn(line, largo, min, max, nEspacios, roadList, count):
    if len(line) == largo and min <= count < max:
        for char in line:
            if char == " ":
                char = ""
            roadList.append(char)
        for i in range(0,nEspacios):
            roadList.append("")


def buildArray(solution):
    newSolution = list()
    f1 = list()
    f2 = list()
    f3 = list()
    f4 = list()
    f5 = list()
    f6 = list()
    f7 = list()
    for i in range(len(solution)):
        if i < 7:
            f1.append(solution[i])
        elif i >= 7 and i < 14:
            f2.append(solution[i])
        elif i >= 14 and i < 21:
            f3.append(solution[i])
        elif i >= 21 and i < 28:
            f4.append(solution[i])
        elif i >= 28 and i < 35:
            f5.append(solution[i])
        elif i >= 35 and i < 42:
            f6.append(solution[i])
        elif i >= 42 and i < 49:
            f7.append(solution[i])
    newSolution.append(f1)
    newSolution.append(f2)
    newSolution.append(f3)
    newSolution.append(f4)
    newSolution.append(f5)
    newSolution.append(f6)
    newSolution.append(f7)
    return newSolution


def calcFitness(solution, roadP1, roadP2, roadP3, roadP4):
    def checkWheelSpin(solution, road):
        currPinchazos = 0
        rotatedSol = numpy.rot90(solution, 1, (1,0))
        print(f"Rotated sol: {rotatedSol}")
        print(f"Road: {road}")
        blockedColumn = list()
        for i in reversed(range(4, 7)):
            for j in range(0, 7):
                if j not in blockedColumn:
                    if rotatedSol[i][j] == 1 and road[i][j] == 'X':
                        blockedColumn.append(j)
                    elif rotatedSol[i][j] == 0 and road[i][j] == 'X':
                        currPinchazos += 1
                        rotatedSol[i][j] = 2
        print(f"After road: {rotatedSol}")
        return rotatedSol, currPinchazos
    
    solution[24] = 3
    pinchazos = 0
    protecciones = 0
    for gen in solution:
        if gen == 1:
            protecciones += 1
    newSolution = buildArray(solution)
    print(f"Inicial : {newSolution}")
    print(f"PRIMER CHECK VUELTA")
    solution2 = checkWheelSpin(newSolution, roadP1)
    pinchazos += solution2[1]
    print(f"SEGUNDO CHECK VUELTA")
    solution3 = checkWheelSpin(solution2[0], roadP2)
    pinchazos += solution3[1]
    print(f"TERCERO CHECK VUELTA")
    solution4 = checkWheelSpin(solution3[0], roadP3)
    pinchazos += solution4[1]
    print(f"CUARTO CHECK VUELTA")
    solution5 = checkWheelSpin(solution4[0], roadP4)
    pinchazos += solution5[1]
    return protecciones, pinchazos, solution5[0]


#Evaluate the road against the wheel(solution).
def fitness_func(solution, parametro2):
    global roadP1, roadP2, roadP3, roadP4
    protecciones, pinchazos, finalSolution = calcFitness(
        solution=solution, roadP1=roadP1, roadP2=roadP2,
        roadP3=roadP3, roadP4=roadP4
    )
    print(f"Protecciones {protecciones} y Pinchazos : {pinchazos}")
    fitness = 1/(pinchazos + protecciones)
    return fitness


def startProgram():
    num_generations = 500 # Number of generations.
    num_parents_mating = 15 # Number of solutions to be selected as parents in the mating pool.
    sol_per_pop = 49 # Number of solutions in the population.
    num_genes = 49
    parent_selection_type = "tournament" # Type of parent selection.
    keep_parents = 3 # Number of parents to keep in the next population. -1 means keep all parents and 0 means keep nothing.
    crossover_type = "single_point" # Type of the crossover operator.
    # Parameters of the mutation operation.
    mutation_type = "random" # Type of the mutation operator.
    mutation_percent_genes = 10 # Percentage of genes to mutate. This parameter has no action if the parameter mutation_num_genes exists or when mutation_type is None.
    #defining  the road.
    global roadP1, roadP2, roadP3, roadP4
    roadP1, roadP2, roadP3, roadP4 = readFile('road.txt')
    fitness_function = fitness_func
    global last_fitness
    last_fitness = 0
    ga_instance = pygad.GA(num_generations=num_generations,
            num_parents_mating=num_parents_mating,
            sol_per_pop=sol_per_pop,
            num_genes=num_genes,
            fitness_func=fitness_function,
            parent_selection_type=parent_selection_type,
            gene_space=[0, 1],
            keep_parents=keep_parents,
            crossover_type=crossover_type,
            mutation_type=mutation_type,
            mutation_percent_genes=mutation_percent_genes,
            callback_generation=callback_generation)
    # Running the GA to optimize the parameters of the function.
    ga_instance.run()
    # Returning the details of the best solution.
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print("Parameters of the best solution : {solution}".format(solution=solution))
    protecciones, pinchazos, finalSolution = calcFitness(
    solution=solution, roadP1=roadP1, roadP2=roadP2, roadP3=roadP3, roadP4=roadP4
    )
    print(f"Final solution \n {finalSolution}\nBest solution has : {protecciones} protecciónes y {pinchazos} pincházos.\n")
    print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
    print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))

    if ga_instance.best_solution_generation != -1:
        print("Best fitness value reached after {best_solution_generation} generations.".format(best_solution_generation=ga_instance.best_solution_generation))


    ## Saving the GA instance.
    #filename = 'genetic'
    #ga_instance.save(filename=filename)

    ## Loading the saved GA instance.
    #loaded_ga_instance = pygad.load(filename=filename)
    #loaded_ga_instance.plot_fitness()


if __name__ == '__main__':
    generar_pagina()
