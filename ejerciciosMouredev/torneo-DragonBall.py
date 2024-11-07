import random

class Fighter:
    def __init__(self, name: str, speed: int, attack: int, defense: int ): # Inicialiazdor de la clase Fighter con atributos con el tipo de parametros de cada uno.
       # Asignamos cada uno de los parametros
        self.name = name
        self.speed = speed
        self.attack = attack
        self.defense = defense
        self.health = 100

    # Podemos crear una nueva funcion para resetear la vida al maximo (100).
    def reset_health(self):
        self.health = 100

    def is_alive (self) -> bool: # Funcion que nos devuelve un boolean.
        return self.health > 0
    
    def take_damage(self, damage: int): # Funcion para calcular el daño recivido.
        
        attack_damage = 0

        if random.random() < 0.2: # Como hay un 20% de posibilidad de que lo esquive, calculamos un numero random (de 0 a 1) y lo compramaos con el 0.2 que es el 20%
            print(f"{self.name} ha esquivado el ataque.")
        else:
            if self.defense >= damage: # Si la defensa es mayor que la potencia del ataque, se le aplicara un 10% de daño.
               attack_damage =  damage * 0.1
            else:
                attack_damage = damage - self.defense # Si el ataque es mayor que la defensa se le restara para ir debilitando la defensa.
        
        self.health -= max(attack_damage, 0)
        print(f"{self.name} ha recibido {attack_damage} de daño.")
        print(f"Salud restante: {self.health}")




#  Hemos creado una clase Luchador (Fighter), que le definen 4 parametros, y ya hemos asociado dichos parametros.

class Battle:
    def __init__(self, fighter1: Fighter, fighter2: Fighter): # Inicializador de la clase Battle.
        self.fighter1 = fighter1
        self.fighter2 = fighter2

    def fight (self) -> Fighter: # Funcion de la pelea.

        print(f"\n=== {self.fighter1.name} vs. {self.fighter2.name} === ")

        while self.fighter1.is_alive() and self.fighter2.is_alive(): # Creamos un while para que siempre que los dos esten vivos se ataquen.

            if self.fighter1.speed >= self.fighter2.speed: # Como segun quien es mas rapido ataca o antes o no, vamos a separarlos por atakker y defender.
                self.turn(self.fighter1, self.fighter2) # Una vez separamos lo mandamos a la funcion turn.
                    
                if self.fighter2.is_alive():
                    self.turn(self.fighter2, self.fighter1)

            else:
                self.turn(self.fighter2, self.fighter1)
                if self.fighter1.is_alive():
                    self.turn(self.fighter1, self.fighter2)

        if self.fighter1.is_alive():
            print(f"\n{self.fighter1.name} es el ganador de la baralla.") 
            return self.fighter1
        else:
            print(f"\n{self.fighter2.name} es el ganador de la baralla.") 
            return self.fighter2
    
    def turn (self, attacker: Fighter, defender: Fighter): # Funcion para ver quien es el atacante y el defensor.
        print(f"\n{attacker.name} ataca a {defender.name}")
        defender.take_damage(attacker.attack) # Llamamos a la funcion que nos gestiona el daño realizado.


class Tournament:
    def __init__(self, fighters: list):

        if not self.is_power_of_two(len(fighters)): # Comprobamos que el listado de luchadores del torneo es divisible entre dos.
            raise ValueError("El numero de luchadores debe ser potencia de 2")
        self.fighters = fighters
    
    def start(self):
        round = 1
        while len(self.fighters) > 1:
            
            print(f"\n=== Ronda {round} === ")

            random.shuffle(self.fighters)  # Reordenamos el listado para los emparejamientos.

            winners = [] # Creamos una lisat donde se guardaran los ganadores de la ronda anterior

            for index in range(0, len(self.fighters), 2): # Creamos in for que recorra todos los luchadores, pero que los pille de 2 en 2.
                fighter1 = self.fighters[index]
                fighter2 = self.fighters[index + 1] # Mas 1 porque pillamos de dos en dos.

                battle = Battle(fighter1, fighter2)
                winner = battle.fight()
                winners.append(winner)

            self.fighters = winners # Reescribimos la lista de lucharores por los ganadores para que se enfrenten entre ellos hasta que quede uno.

            round += 1
    
        print(f"\n¡El ganador del torneo es {self.fighters[0].name}!")

    def is_power_of_two(self,n) -> bool:
        if n <= 0:
            return False
        while n % 2 == 0:
            n //= 2 # Dividimos el resto.
        return n == 1


# battle = Battle(fighter1, fighter2)
# winner = battle.fight()
# print(f"Ganador:  {winner.name}")


fighters = [ # Creamos un listado con los luchadores.
    Fighter("Goku", 90, 95, 80),
    Fighter("Vegeta", 95, 90, 82),
    Fighter("Piccolo", 80, 85, 90),
    Fighter("Freezer", 95, 90, 75),
]

tournament = Tournament (fighters)
tournament.start()
