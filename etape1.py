# -*- coding: utf-8 -*-

from ev3dev2.sound   import Sound
from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
import time
import sys


class RobotException(Exception):
    """
    Erreurs liees au Robot
    """
    message = ""
    line_number=""
    def __init__(self, message, line_number=""):
        super().__init__()
        self.message = message
        self.line_number = line_number

    def __str__(self):
        return "Ligne {} RobotException: {}".format(self.line_number, self.message)
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
                self.capteurCouleur = ColorSensor()
            if(ultrasonSensor != None) :
                self.capteurUltrason= UltrasonicSensor()
            if(giroSensor != None) :
                self.gyroscope= GyroSensor()
            if(but_1 != None) :
                self.bouton1 = TouchSensor(but_1)
            if(but_2 != None) :
                self.bouton2 = TouchSensor(but_2)
            if (L_motor1 != None and L_motor2 != None) :
                self.moteurs = MoveSteering(L_motor1,L_motor2)
        except Exception as e : 
            line_number = str(e).split(" ")[-1]  # Extraire le numero de ligne de la chaîne de traceback
            raise RobotException("Erreur lors de la creation de l'objet robot \nErreur: " + str(e),line_number )
    
    def preparationCouleur(self) :
        if not self.verificationCapteurCouleur() :
            raise RobotException("Le robot n'a pas de capteur couleur definis")

  
        # Calibrage blanc
        self.capteurCouleur.calibrate_white

    def getCouleur(self) :
        r,g,b = self.capteurCouleur.rgb
        return (r,g,b)
    def isCouleurNoir(self,limite) :
        couleur = self.getCouleur()
        if (couleur[0] > limite or couleur[1] > limite or couleur[2] > limite) :
            return False
        else :
            return True

    def preparationRobot(self) :
        if (self.verificationCapteurCouleur()) :
            self.preparationCouleur()
        if(self.verificationGyroscope) :
            self.preparationGyroscope
    def preparationGyroscope(self) :
        self.gyroscope.calibrate()
    def move_forward(self,distance_centimeters):
        self.moteurGauche.run_to_rel_pos(position_sp=distance_centimeters * 5, speed_sp=500, stop_action="hold")
        self.moteurDroite.run_to_rel_pos(position_sp=distance_centimeters * 5, speed_sp=500, stop_action="hold")
    def verificationCapteurCouleur(self) :
        """
        Verifie si le capteur de couleur est defini pour l'instance Robot.

        Returns:
            bool: True si le capteur de couleur est defini, False sinon.
        """
        return True if self.capteurCouleur is not None else False

    def verificationCapteurUltrason(self) :
        """
        Verifie si le capteur ultrasonique est defini pour l'instance Robot.

        Returns:
            bool: True si le capteur ultrasonique est defini, False sinon.
        """
        return True if self.capteurUltrason is not None else False

    def verificationMoteurDroite(self) :
        """
        Verifie si le moteur droit est defini pour l'instance Robot.

        Returns:
            bool: True si le moteur droit est defini, False sinon.
        """
        return True if self.moteurDroite is not None else False

    def verificationMoteurGauche(self) :
        """
        Verifie si le moteur gauche est defini pour l'instance Robot.

        Returns:
            bool: True si le moteur gauche est defini, False sinon.
        """
        return True if self.moteurGauche is not None else False

    def verificationBouton1(self) :
        """
        Verifie si le bouton 1 est defini pour l'instance Robot.

        Returns:
            bool: True si le bouton 1 est defini, False sinon.
        """
        return True if self.bouton1 is not None else False

    def verificationBouton2(self) :
        """
        Verifie si le bouton 2 est defini pour l'instance Robot.

        Returns:
            bool: True si le bouton 2 est defini, False sinon.
        """
        return True if self.bouton2 is not None else False

    def verificationGyroscope(self) :
        """
        Verifie si le gyroscope est defini pour l'instance Robot.

        Returns:
            bool: True si le gyroscope est defini, False sinon.
        """
        return True if self.gyroscope is not None else False
  
    def avancerLigneDepart(self) :
        """
        Permet au robot d'avancer vers la premiere zone noire qu'il detecte.
        """
        SEUIL_NOIR = 20
        print(self.getCouleur())
        sys.stdout.flush()   
        while( not self.isCouleurNoir(SEUIL_NOIR) ) :
            self.avancer()
            print(self.getCouleur())
            sys.stdout.flush()   
        """
        print("Ligne de depart atteinte !")
        while(self.isCouleurNoir(SEUIL_NOIR)) :
            self.avancer()
            print(self.getCouleur())  
            sys.stdout.flush()   
        print("Ligne de depart traverse !")
        """
        self.stop()
    def reculerLigneDepart(self) :
        """
        Permet au robot de reculer vers la premiere zone noire qu'il detecte,
        tout en faisant des observation a l'aide de ses capteurs.
        """
        SEUIL_NOIR = 20
        nb_ligne = 0
        while(nb_ligne != 2) :
            while( not self.isCouleurNoir(SEUIL_NOIR) ) :
                self.reculer()
                print(self.getCouleur())
                sys.stdout.flush()   
            print("Ligne de depart atteinte !")
            self.stop()
            nb_ligne +=1
    def avancerLigneArrivee(self) :
        """
        Permet au robot d'avancer vers la seconde zone noire qu'il detecte,
        tout en faisant des observation a l'aide de ses capteurs.
        """
        SEUIL_NOIR = 20
        while( not self.isCouleurNoir(SEUIL_NOIR) ) :
            # Calcul a faire (etape2)
            self.avancer()
            print(self.getCouleur())
            sys.stdout.flush()   
        print("Ligne d'arrivee atteinte !")
        self.stop()
    def get_moteurGauche(self):
        """
        Retourne le moteur gauche de l'instance Robot.

        Returns:
            object: Le moteur gauche.
        """
        return self.moteurGauche

    def set_moteurGauche(self, value):
        """
        Definit le moteur gauche de l'instance Robot.

        Args:
            value (object): Le moteur gauche a definir.
        """
        self.moteurGauche = value

    def get_moteurDroite(self):
        """
        Retourne le moteur droit de l'instance Robot.

        Returns:
            object: Le moteur droit.
        """
        return self.moteurDroite

    def set_moteurDroite(self, value):
        """
        Definit le moteur droit de l'instance Robot.

        Args:
            value (object): Le moteur droit a definir.
        """
        self.moteurDroite = value

    def get_moteurSecondaire(self):
        """
        Retourne le moteur secondaire (medium Motor) de l'instance Robot.
        Returns:
            object: Le moteur secondaire.
        """
        return self.moteurSecondaire

    def set_moteurSecondaire(self, value):
        """
        Definit le moteur secondaire de l'instance Robot.

        Args:
            value (object): Le moteur secondaire a definir.
        """
        self.moteurSecondaire = value

    def get_capteurCouleur(self):
        """
        Retourne le capteur de couleur de l'instance Robot.

        Returns:
            object: Le capteur de couleur.
        """
        return self.capteurCouleur

    def set_capteurCouleur(self, value):
        """
        Retourne le capteur de couleur de l'instance Robot.

        Returns:
            object: Le capteur de couleur.
        """
        self.capteurCouleur = value

    def get_bouton1(self):
        """
        Retourne le bouton 1 de l'instance Robot.

        Returns:
            object: Le bouton 1.
        """
        return self.bouton1

    def set_bouton1(self, value):
        """
        Definit le bouton 1 de l'instance Robot.

        Args:
            value (object): Le bouton 1 a definir.
        """
        self.bouton1 = value

    def get_bouton2(self):
        """
        Retourne le bouton 2 de l'instance Robot.

        Returns:
            object: Le bouton 2.
        """
        return self.bouton2

    def set_bouton2(self, value):
        """
        Definit le bouton 2 de l'instance Robot.

        Args:
            value (object): Le bouton 2 a definir.
        """
        self.bouton2 = value

    def get_gyroscope(self):
        """
        Retourne le gyroscope de l'instance Robot.

        Returns:
            object: Le gyroscope.
        """
        return self.gyroscope              
                
    def avancer(self):
        """
        Permet au robot d'avancer tout en gardant la trajectoire a l'aide du gyroscope.
        """
        # Lecture de l'angle actuel du gyroscope
        angle_actuel = self.gyroscope.angle
        # Calcul de la correction a appliquer aux moteurs
        correction = angle_actuel
        # Utilisation de la correction pour ajuster les moteurs
        self.moteurs.on(steering=correction, speed=20)
    def reculer(self):
        """
        Permet au robot de reculer tout en gardant la trajectoire a l'aide du gyroscope.
        """
        # Lecture de l'angle actuel du gyroscope
        angle_actuel =  - self.gyroscope.angle
        # Calcul de la correction a appliquer aux moteurs
        correction = angle_actuel
        # Utilisation de la correction pour ajuster les moteurs
        self.moteurs.on(steering=correction, speed=-20)        
    def stop(self) :
        """
        Permet de stopper les moteurs permettant les deplacements du robot.
        """
        self.moteurs.off()        


def main():
    try :
        robot = Robot(OUTPUT_B, OUTPUT_A, None, INPUT_2, INPUT_1,INPUT_4, None, None)
        #def __init__(self, L_motor1, L_motor2,M_motor,colorSensor,ultrasonSensor,giroSensor,but_1,but_2):
        robot.preparationRobot()
        robot.preparationGyroscope()
        robot.avancerLigneDepart()
        time.sleep(1)
        robot.avancerLigneArrivee()
        time.sleep(1)
        robot.move_forward(100)
        time.sleep(2)
        robot.reculerLigneDepart()

        
    except RobotException as r :
        print("Il y a eu un probleme avec le Robot. Arret de la simulation.")
        print(str(r))
    except Exception as e :
        print("Il y a eu un quelconque probleme lors de la simulation. Arret de la simulation")
        print(str(e))
    else :
        print("La simulation est terminee, il n'y a eu aucun probleme.")
    return 0





if __name__ == "__main__":
    main()