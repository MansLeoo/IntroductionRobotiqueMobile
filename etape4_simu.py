
from ev3dev2.sound   import Sound
from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
import time


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

    def getCouleur(self) :
        r,g,b = self.capteurCouleur.rgb
        return (r,g,b)
    def isCouleurNoir(self,limite) :
        couleur = self.getCouleur()
        if (couleur[0] > limite and couleur[1] > limite and couleur[2] > limite) :
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
        Vérifie si le capteur de couleur est défini pour l'instance Robot.

        Returns:
            bool: True si le capteur de couleur est défini, False sinon.
        """
        return True if self.capteurCouleur is not None else False

    def verificationCapteurUltrason(self) :
        """
        Vérifie si le capteur ultrasonique est défini pour l'instance Robot.

        Returns:
            bool: True si le capteur ultrasonique est défini, False sinon.
        """
        return True if self.capteurUltrason is not None else False

    def verificationMoteurDroite(self) :
        """
        Vérifie si le moteur droit est défini pour l'instance Robot.

        Returns:
            bool: True si le moteur droit est défini, False sinon.
        """
        return True if self.moteurDroite is not None else False

    def verificationMoteurGauche(self) :
        """
        Vérifie si le moteur gauche est défini pour l'instance Robot.

        Returns:
            bool: True si le moteur gauche est défini, False sinon.
        """
        return True if self.moteurGauche is not None else False

    def verificationBouton1(self) :
        """
        Vérifie si le bouton 1 est défini pour l'instance Robot.

        Returns:
            bool: True si le bouton 1 est défini, False sinon.
        """
        return True if self.bouton1 is not None else False

    def verificationBouton2(self) :
        """
        Vérifie si le bouton 2 est défini pour l'instance Robot.

        Returns:
            bool: True si le bouton 2 est défini, False sinon.
        """
        return True if self.bouton2 is not None else False

    def verificationGyroscope(self) :
        """
        Vérifie si le gyroscope est défini pour l'instance Robot.

        Returns:
            bool: True si le gyroscope est défini, False sinon.
        """
        return True if self.gyroscope is not None else False
  
    def avancerLigneDepart(self) :
        """
        Permet au robot d'avancer vers la première zone noire qu'il détecte.
        """
        SEUIL_NOIR = 200
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
        """
        Permet au robot de reculer vers la première zone noire qu'il détecte,
        tout en faisant des observation a l'aide de ses capteurs.
        """
        SEUIL_NOIR = 200
        nb_ligne = 0
        while(nb_ligne != 2) :
            while( not self.isCouleurNoir(SEUIL_NOIR) ) :
                self.reculer()
                print(self.getCouleur())
            print("Ligne de départ atteinte !")
            while(self.isCouleurNoir(SEUIL_NOIR)) :
                self.reculer()
                print(self.getCouleur())   
            print("Ligne de départ traverse !")
            self.stop()
            nb_ligne +=1
    def avancerLigneArrivee(self) :
        """
        Permet au robot d'avancer vers la seconde zone noire qu'il détecte,
        tout en faisant des observation a l'aide de ses capteurs.
        """
        SEUIL_NOIR = 200
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
        """
        Retourne le moteur gauche de l'instance Robot.

        Returns:
            object: Le moteur gauche.
        """
        return self.moteurGauche

    def set_moteurGauche(self, value):
        """
        Définit le moteur gauche de l'instance Robot.

        Args:
            value (object): Le moteur gauche à définir.
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
        Définit le moteur droit de l'instance Robot.

        Args:
            value (object): Le moteur droit à définir.
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
        Définit le moteur secondaire de l'instance Robot.

        Args:
            value (object): Le moteur secondaire à définir.
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
        Définit le bouton 1 de l'instance Robot.

        Args:
            value (object): Le bouton 1 à définir.
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
        Définit le bouton 2 de l'instance Robot.

        Args:
            value (object): Le bouton 2 à définir.
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
        # Calcul de la correction à appliquer aux moteurs
        correction = angle_actuel
        # Utilisation de la correction pour ajuster les moteurs
        self.moteurs.on(steering=correction, speed=70)
    def reculer(self):
        """
        Permet au robot de reculer tout en gardant la trajectoire a l'aide du gyroscope.
        """
        # Lecture de l'angle actuel du gyroscope
        angle_actuel =  - self.gyroscope.angle
        # Calcul de la correction à appliquer aux moteurs
        correction = angle_actuel
        # Utilisation de la correction pour ajuster les moteurs
        self.moteurs.on(steering=correction, speed=-70)        
    def stop(self) :
        """
        Permet de stopper les moteurs permettant les déplacements du robot.
        """
        self.moteurs.off()    
    def tourner(self) :
        left_motor = self.moteurGauche
        right_motor = self.moteurDroite

        # Define motor parameters
        speed = 20  # Speed of the motors
        turn_duration = 1  # Duration to turn (adjust as needed)
        turn_angle = 90  # Desired turn angle

        # Perform the turn
        left_motor.on_for_seconds(speed, turn_duration)
        right_motor.on_for_seconds(-speed, turn_duration)

        # Wait for the turn to complete

        # Stop the motors
        left_motor.off()
        right_motor.off()
    def slalom(self) :
        self.tourner_avec_gyroscope(90,10)
        self.avancerCM(5.5)
        self.tourner_avec_gyroscope(-90,10)
        self.avancerCM(11)
        self.tourner_avec_gyroscope(-90,10)
        self.avancerCM(10)
    def avancerCM(self,distance_cm):
        # Convertir la distance en nombre de rotations
        rotations = distance_cm / 5.6
    
        # Définir la vitesse des moteurs
        vitesse = 10  # Ajustez selon votre besoin
        motor_left = self.moteurGauche
        motor_right = self.moteurDroite
        # Réinitialiser les encodeurs
        motor_left.reset()
        motor_right.reset()
        steering_drive = MoveSteering(OUTPUT_A, OUTPUT_B)
    
        # Faire avancer les moteurs jusqu'à ce que la distance parcourue atteigne la distance désirée
        steering_drive.on_for_rotations(0,vitesse,rotations)
    def tourner_avec_gyroscope(self,angle_cible, vitesse_rotation):
        tank = MoveTank(OUTPUT_A, OUTPUT_B)

        gyro = self.gyroscope
        # Lecture de l'angle initial
        angle_initial = gyro.angle
    
        # Calcul de l'angle final
        angle_final = angle_initial + angle_cible
    
        if(angle_cible > 0) :
            # Rotation du robot
            tank.on(left_speed=vitesse_rotation, right_speed=-vitesse_rotation)
        else :
            tank.on(left_speed=-vitesse_rotation, right_speed=vitesse_rotation)

    
        while True:
            # Lire l'angle actuel du gyroscope
            angle_actuel = gyro.angle
    
            # Si l'angle actuel atteint ou dépasse l'angle final, arrêter les moteurs
            if(angle_cible > 0) :
                if angle_actuel >= angle_final:
                    tank.off()
                    break
            else :
                if angle_actuel <= angle_final:
                    tank.off()
                    break
def main():
    try :
        #(L_motor1, L_motor2,M_motor,colorSensor,ultrasonSensor,giroSensor,but_1,but_2):
        robot = Robot(OUTPUT_B, OUTPUT_A, None, INPUT_1, INPUT_2,INPUT_3, None, None)
        robot.preparationRobot()
        robot.slalom()
        

    except RobotException as r :
        print("Il y a eu un probleme avec le Robot. Arret de la simulation.")
        print(str(r))
    except Exception as e :
        print("Il y a eu un quelconque probleme lors de la simulation. Arret de la simulation")
        print(str(e))
    else :
        print("La simulation est terminée, il n'y a eu aucun problème.")
    return 0
    #def __init__(self, L_motor1, L_motor2,M_motor,colorSensor,ultrasonSensor,giroSensor,but_1,but_2):






if __name__ == "__main__":
    main()