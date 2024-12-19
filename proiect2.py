import PySimpleGUI as sg
import random


class Birou:
    def __init__(self, nume, ocupat, echipamente=None, consum_neocupat=10):
        self.nume = nume
        self.ocupat = ocupat
        self.echipamente = echipamente if echipamente else {}
        self.consum_neocupat = consum_neocupat

    def consum_energie(self):
        if self.ocupat:
            return sum(self.echipamente.values())
        else:
            return self.consum_neocupat
class Etaj:
    def __init__(self, numar, numar_birouri, echipamente_birou):
        self.numar = numar
        self.birouri = [Birou(f"Birou {i + 1}", False, echipamente_birou) for i in range(numar_birouri)]
    def set_ocupare_birouri(self, ocupare_birouri):
        for i, birou in enumerate(self.birouri):
            birou.ocupat = ocupare_birouri[i]

    def consum_energie(self):
        return sum(birou.consum_energie() for birou in self.birouri)

class Cladire:
    def __init__(self, nume, etaje, pret_kwh):
        self.nume = nume
        self.etaje = etaje
        self.pret_kwh = pret_kwh
    def consum_energie_total(self):
        return sum(etaj.consum_energie() for etaj in self.etaje)
    def cost_total_energie(self):
        return self.consum_energie_total() * self.pret_kwh
def creare_etaj(numar, numar_birouri, echipamente_birou, ocupare_birouri):
    etaj = Etaj(numar, numar_birouri, echipamente_birou)
    etaj.set_ocupare_birouri(ocupare_birouri)
    return etaj

def creare_cladire(nume, pret_kwh, numar_etaje, numar_birouri, echipamente_birou, ocupare_birouri):
    etaje = []
    for i in range(numar_etaje):
        etaj = creare_etaj(i + 1, numar_birouri, echipamente_birou, ocupare_birouri[i])
        etaje.append(etaj)
    return Cladire(nume, etaje, pret_kwh)
def obtinere_pret_energie():
    pret = round(random.uniform(0.6, 1.2), 2)  # Preț aleator între 0.6 și 1.2 lei/kWh
    return pret


def interfata_grafica():
    layout = [
        [sg.Text('Introduceti detalii pentru cladire')],
        [sg.Text('Numele cladirii'), sg.InputText(key='nume_cladire')],
        [sg.Text('Numar de etaje'), sg.InputText(key='numar_etaje')],
        [sg.Text('Numar de birouri pe etaj'), sg.InputText(key='numar_birouri')],
        [sg.Text('Pretul energiei pe kWh (lei) va fi actualizat dinamic')],
        [sg.Button('Creare Cladire')],
        [sg.Text('', size=(40, 10), key='output')],
        [sg.Text('Pret curent energie (actualizat in timp real):', key='current_price')],
        [sg.Text('... lei/kWh', size=(10, 1), key='pret_kwh_dynamic')],
    ]
    
    window = sg.Window('Aplicatie de Gestionare a Energiei', layout)

    while True:
        event, values = window.read(timeout=10000)  # Actualizare dinamică la fiecare 10 secunde

        if event == sg.WIN_CLOSED:
            break

        # Actualizarea prețului energiei dinamic (în fiecare ciclu)
        pret_kwh_dynamic = obtinere_pret_energie()  # Obținem prețul dinamic
        window['pret_kwh_dynamic'].update(f'{pret_kwh_dynamic} lei/kWh')

        if event == 'Creare Cladire':
            try:
                nume_cladire = values['nume_cladire']
                numar_etaje = int(values['numar_etaje'])
                numar_birouri = int(values['numar_birouri'])
                
                # Adăugăm echipamente comune pentru fiecare birou
                echipamente_birou = {}
                while True:
                    echipament = sg.popup_get_text("Introduceti numele echipamentului pentru birou (sau 'stop' pentru a termina): ")
                    if echipament and echipament.lower() == 'stop':
                        break
                    if echipament:
                        consum = float(sg.popup_get_text(f"Introduceti consumul echipamentului '{echipament}' (kWh): "))
                        echipamente_birou[echipament] = consum

                # Setăm ocuparea birourilor pentru fiecare etaj
                ocupare_birouri = []
                for i in range(numar_etaje):
                    ocupare_birouri_etaj = []
                    for j in range(numar_birouri):
                        ocupat = sg.popup_yes_no(f"Este Birou {j+1} ocupat pe Etajul {i+1}?")
                        ocupare_birouri_etaj.append(ocupat == 'Yes')  # Comparăm cu "Yes" (string)
                    ocupare_birouri.append(ocupare_birouri_etaj)

                # Creăm clădirea
                cladire = creare_cladire(nume_cladire, pret_kwh_dynamic, numar_etaje, numar_birouri, echipamente_birou, ocupare_birouri)

                # Calculăm consumul și costul total
                total_consum = cladire.consum_energie_total()
                total_cost = cladire.cost_total_energie()

                # Formatează rezultatele pentru a le afișa
                result = f"Consum total de energie pentru {cladire.nume}: {total_consum} kWh\n"
                result += f"Cost total energie: {total_cost} lei\n"

                for etaj in cladire.etaje:
                    result += f"Consum energie pentru etajul {etaj.numar}: {etaj.consum_energie()} kWh\n"

                window['output'].update(result)

            except ValueError:
                sg.popup_error('Te rog sa introduci valori valide.')

    window.close()

# Program principal
if __name__ == "__main__":
    interfata_grafica()
