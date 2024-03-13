
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
    def __init__(self, message, line_number=""):
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
    gyroscope = None
    moteurs = None 
    def __init__(self, L_motor1, L_motor2,M_motor,colorSensor,ultrasonSensor,giroSensor,but_1,but_2):
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
            if(giroSensor != None) :
                self.gyroscope= GyroSensor(giroSensor)
            if(but_1 != None) :
                self.bouton1 = TouchSensor(but_1)
            if(but_2 != None) :
                self.bouton2 = TouchSensor(but_2)
            if (L_motor1 != None and L_motor2 != None) :
                self.moteurs = MoveSteering(L_motor1,L_motor2)
        except Exception as e : 
            line_number = str(e).split(" ")[-1]  # Extraire le numéro de ligne de la chaîne de traceback
            raise RobotException("Erreur lors de la création de l'objet robot \nErreur: " + str(e),line_number )
    
    def preparationCouleur(self) :
        if not self.verificationCapteurCouleur() :
            raise RobotException("Le robot n'a pas de capteur couleur définis")

  
        # Calibrage blanc
        self.capteurCouleur.calibrate_white

    def  getCouleur(self) :
        r,g,b = self.capteurCouleur.rgb
        return (r,g,b)
    def isCouleurNoir(self,limite) :
        couleur = self.getCouleur()
        if (couleur[0] > limite and couleur[1] > limite and couleur[2] > limite) :
            return False
        else :
            return True

    def preparationRobot(self,) :
        if (self.verificationCapteurCouleur()) :
            self.preparationCouleur()
        if(self.verificationGyroscope) :
            self.preparationGyroscope
    def preparationGyroscope(self) :
        self.gyroscope.calibrate()
    def verificationCapteurCouleur(self) :
        return True if self.capteurCouleur is not None else False
    def verificationCapteurUltrason(self) :
        return True if self.capteurUltrason is not None else False
    def verificationMoteurDroite(self) :
        return True if self.moteurDroite is not None else False
    def verificationMoteurGauche(self) :
        return True if self.moteurGauche is not None else False
    def verificationBouton1(self) :
        return True if self.bouton1 is not None else False
    def verificationBouton2(self) :
        return True if self.bouton2 is not None else False            
    def verificationGyroscope(self) :
        return True if self.gyroscope is not None else False    
    def avancerLigneDepart(self) :
        SEUIL_NOIR = 100
        while( not self.isCouleurNoir(SEUIL_NOIR) ) :
            self.avancer()
            print(self.getCouleur())
        print("Ligne de départ atteinte !")
        while(self.isCouleurNoir(SEUIL_NOIR)) :
            self.avancer()
            print(self.getCouleur())   
        print("Ligne de départ traverse !")
        self.stop()
    def reculerLigneDepart(self) :
        SEUIL_NOIR = 100
        while( not self.isCouleurNoir(SEUIL_NOIR) ) :
            self.reculer()
            print(self.getCouleur())
        print("Ligne de départ atteinte !")
        while(self.isCouleurNoir(SEUIL_NOIR)) :
            self.reculer()
            print(self.getCouleur())   
        print("Ligne de départ traverse !")
        self.stop()
    def avancerLigneArrivee(self) :
        SEUIL_NOIR = 100
        while( not self.isCouleurNoir(SEUIL_NOIR) ) :
            # Calcul a faire (etape2)
            self.avancer()
            print(self.getCouleur())
        print("Ligne d'arrivée atteinte !")
        while(self.isCouleurNoir(SEUIL_NOIR)) :
            self.avancer()
            print(self.getCouleur())   
        print("Ligne d'arrivée traverse !")
        self.stop()
    def get_moteurGauche(self):
        return self.moteurGauche

    def set_moteurGauche(self, value):
        self.moteurGauche = value

    def get_moteurDroite(self):
        return self.moteurDroite

    def set_moteurDroite(self, value):
        self.moteurDroite = value

    def get_moteurSecondaire(self):
        return self.moteurSecondaire

    def set_moteurSecondaire(self, value):
        self.moteurSecondaire = value

    def get_capteurCouleur(self):
        return self.capteurCouleur

    def set_capteurCouleur(self, value):
        self.capteurCouleur = value

    def get_bouton1(self):
        return self.bouton1

    def set_bouton1(self, value):
        self.bouton1 = value

    def get_bouton2(self):
        return self.bouton2

    def set_bouton2(self, value):
        self.bouton2 = value

    def get_gyroscope(self):
        return self.gyroscope              
                
    def avancer(self):
        # Lecture de l'angle actuel du gyroscope
        angle_actuel = self.gyroscope.angle
        # Calcul de la correction à appliquer aux moteurs
        correction = angle_actuel
        # Utilisation de la correction pour ajuster les moteurs
        self.moteurs.on(steering=correction, speed=70)
    def reculer(self):
        # Lecture de l'angle actuel du gyroscope
        angle_actuel = self.gyroscope.angle
        # Calcul de la correction à appliquer aux moteurs
        correction = angle_actuel
        # Utilisation de la correction pour ajuster les moteurs
        self.moteurs.on(steering=correction, speed=-70)        
    def stop(self) :
        self.moteurs.off()        


def main():
    try :
        robot = Robot(OUTPUT_B, OUTPUT_A, None, INPUT_1, INPUT_2,INPUT_3, None, None)
        robot.preparationRobot()
        robot.avancerLigneDepart()
        robot.avancerLigneArrivee()
        robot.reculerLigneDepart()

        
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