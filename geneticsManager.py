from nn import NN
import random
import time
import copy
netArray = []
players = []
scores = []
times = []
count = 100
mutationRate = 0.2  # 10%
currTime = time.time()
crea = False
gen = 0


def fitness():
    pass

# we chose 6 pairs to mate algorithm returns an array like this [[top player 1,top player 2]... ]


def restart(crossoverResult):
    global gen
    gen = gen + 1
    from game import Player
    from game import resetTime
    from game import resetPipes
    players.clear()
    global count
    count = len(crossoverResult)
    for i in range(len(crossoverResult)):
        network = crossoverResult[i]
        netArray.append(network)
        p = Player(network)
        players.append(p)
    # resetTime()
    resetPipes()


def selection():
    global count
    selectionResult = []
    offspring_count = max((int)(0.8*count), 6)
    count = offspring_count
    for i in range(count):
        if i % 2 == 0:
            continue
        selectionResult.append([players[i], players[i+1]])
    return selectionResult

# creates the child by giving half or more of the weights to the heighest and the other half to the lowest
# mutations might occur on the way to help create diversity


def crossover(selectedPairs):
    nextGeneration = []  # contains top 2 + 2 children from each pair so 8
    # only done to have a fit gene in case of a decline
    nextGeneration.append(selectedPairs[0][0].nuernet)
    # nextGeneration.append(selectedPairs[0][1].nuernet)
    for pairs in selectedPairs:
        net1 = pairs[0].nuernet
        net2 = pairs[1].nuernet
        copyOfnet2 = net2.copyNN()  # copy.copy(net2)  # net2.copy()
        for i, node in enumerate(net2.net[0], 0):
            for j, weight in enumerate(node["weights"], 0):
                rando = random.randint(0, 100)
                if(rando <= (mutationRate * 100)):
                    net2.net[0][i]["weights"][j] = random.random()
                    net1.net[0][i]["weights"][j] = random.random()
                elif(rando <= 55 and rando > mutationRate):
                    val = net2.net[0][i]["weights"][j]
                    net2.net[0][i]["weights"][j] = net2.net[0][i]["weights"][j]
                    net1.net[0][i]["weights"][j] = net1.net[0][i]["weights"][j]

                else:
                    temp = net1.net[0][i]["weights"][j]
                    net1.net[0][i]["weights"][j] = copyOfnet2[0][i]["weights"][j]
                    net2.net[0][i]["weights"][j] = temp

            pass
        pass
        for i, node in enumerate(net1.net[1], 0):
            for j, weight in enumerate(node["weights"], 0):
                rando = random.randint(0, 100)
                if(rando < (mutationRate * 100)):
                    net1.net[1][i]["weights"][j] = random.random()
                elif(rando <= 55 and rando > mutationRate):
                    net1.net[1][i]["weights"][j] = net1.net[1][i]["weights"][j]
                else:
                    net1.net[1][i]["weights"][j] = net2.net[1][i]["weights"][j]
            pass
        pass
        nextGeneration.append(net1)
        nextGeneration.append(net2)

    return nextGeneration
    pass


def sort():
    copy = players
    for i in range(count):
        maxIndex = i
        for j in range(i, count):
            if players[maxIndex].deathTime < players[j].deathTime:
                maxIndex = j
        temp = players[i]
        players[i] = players[maxIndex]
        players[maxIndex] = temp


def createInitialPopulation():
    from game import Player

    for i in range(count):
        network = NN(2, 10, 2, i)
        netArray.append(network)
        p = Player(network)
        players.append(p)

    crea = True


def takeAction(screen):
    from game import getOnScreenPipes
    allDone = True
    # print(count)
    for i in range(count):
        players[i].moveY(5)
        if(players[i].done == True):
            continue
        else:
            allDone = False
        pipes = getOnScreenPipes()
        for p in pipes:
            p.collides(players[i])
            out = netArray[i].forward_prop(
                p.distanceToPipe(10, players[i].getY()))

            if(gen == 5):
                print("out")

            if out[0] < out[1]:  # stay put
                pass
            else:
                players[i].moveY(-50)
        players[i].drawPlayer(screen)
    if(allDone):
        sort()
        statistics()
        pairs = selection()
        crossresult = crossover(pairs)
        # quit()
        restart(crossresult)
        print(len(players))
        # quit()


def printRemaining():
    cou = 0
    for p in players:
        if p.done == False:
            print("pos ", p.getY())
            cou = cou + 1
    print(cou)


def checkForGround(ground, sky):
    for p in players:
        p.checkForGround(ground, sky)


def statistics():
    for i in range(count):
        print(i, players[i].deathTime)
    print()


class Manager:
    def __init__(self):

        createInitialPopulation()

    def act(self, screen):
        takeAction(screen)

    def printRemaining(self):
        printRemaining()

    def checkForGround(self, ground, sky):
        checkForGround(ground, sky)
