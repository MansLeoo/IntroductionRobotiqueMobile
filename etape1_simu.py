
from ev3dev2.sound   import Sound
from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4


class RobotException(Exception):
    """
    Erreurs liées au Robot
    """
    message = ""
    line_number=""
    def __init__(self, message, line_number):
        super().__init__()
        self.message = message
        self.line_number = line_number

    def __str__(self):
        return f"Ligne {self.line_number} RobotException: {self.message}"
class Robot :
    moteurGauche = None
    moteurDroite  = None
    moteurSecondaire = None
    capteurCouleur = None
    bouton1 = None
    bouton2 = None
    def __init__(self, L_motor1, L_motor2,M_motor,colorSensor,ultrasonSensor,but_1,but_2):
        try :
            if(L_motor1 != None) :
                self.moteurGauche = LargeMotor(L_motor1)
            if(L_motor2 != None) :
                self.moteurDroite = LargeMotor(L_motor2)
            if(M_motor != None) :
                self.moteurSecondaire = MediumMotor(M_motor)
            if(colorSensor != None) :
                self.capteurCouleur = ColorSensor(colorSensor)
            if(ultrasonSensor != None) :
                self.capteurUltrason= UltrasonicSensor(ultrasonSensor)
            if(but_1 != None) :
                self.bouton1 = TouchSensor(but_1)
            if(but_2 != None) :
                self.bouton2 = TouchSensor(but_2)
        except Exception as e : 
            line_number = str(e).split(" ")[-1]  # Extraire le numéro de ligne de la chaîne de traceback
            raise RobotException("Erreur lors de la création de l'objet robot \nErreur: " + str(e),line_number )
    
    def preparationCouleur(self) :
        tentatives = 0
        not_calibrated = True
        while (not_calibrated or tentatives < 10):
            try:
                self.capteurCouleur.calibrate_white()
                # not good if one of the max is zero
                not_calibrated = ( (self.capteurCouleur.red_max == 0) 
                                   or (self.capteurCouleur.green_max == 0)
                                   or (self.capteurCouleur.blue_max == 0) )
            except:
                not_calibrated = True
        if(not_calibrated) :
            line_number = str(e).split(" ")[-1]  # Extraire le numéro de ligne de la chaîne de traceback
            raise RobotException("Erreur lors du calibrage du capteur couleur",line_number)
        
                
                
    def avancer(self,distance):
        self.moteurGauche.run_to_rel_pos(position_sp=distance, speed_sp=500, stop_action="hold")
        self.moteurDroite.run_to_rel_pos(position_sp=distance, speed_sp=500, stop_action="hold")
        self.moteurGauche.wait_until_not_moving()
        self.moteurDroite.wait_until_not_moving()                



def main():
    try :
        robot = Robot(OUTPUT_B, OUTPUT_A, None, INPUT_1, INPUT_2, None, None)
        robot.avancer(1000)
        x = 5/0
    except RobotException as r :
        print("Il y a eu un probleme avec le Robot. Arret de la simulation.")
        print(str(r))
    except Exception as e :
        print("Il y a eu un quelconque probleme lors de la simulation. Arret de la simulation")
        print(str(e))
    else :
        print("La simulation est terminée, il n'y a eu aucun problème.")
    return 0






if __name__ == "__main__":
    main()