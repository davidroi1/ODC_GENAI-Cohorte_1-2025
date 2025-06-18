from dataclasses import dataclass
from statistics import median, stdev, mode, mean
from collections import Counter


@dataclass
class ColumnData:
    name: str
    data: list

    def __post_init__(self):
        """
        faire une post initialisation apres celle de dataclasss
        """
        self.type = self._type_of_data()

    def _type_of_data(self) -> str:
        """
        Retourne le type des donnee contenue dans l'attribut data
        """
        if not isinstance(self.data[0], int):
            return "categorical"
        return "numeric"

    def unique(self):
        """
        Retourne l'ensemble des valeurs uniques de la colonne. [cite: 12]
        """
        return list(set(self.data))

    def value_counts(self) -> dict:
        """
        Retourne un dictionnaire associant chaque valeur unique à son occurrence. [cite: 12]
        """
        return dict(Counter(self.data))

    def stats(self) -> dict:
        """
        Retourne un ensemble de statistiques possibles sur la colonne (moyenne, écart type, max, min, mode, ...). [cite: 13]
        S'adapte au type de la colonne (numérique ou catégorielle).
        """
        data_stats = {}

        if self.type == "numeric":
            data_stats[f"moyen {self.name}"] = mean(self.data)
            data_stats[f"mediane {self.name}"] = median(self.data)
            data_stats[f"ecart-type {self.name}"] = stdev(self.data)
            data_stats[f"minimum {self.name}"] = min(self.data)
            data_stats[f"maximum {self.name}"] = max(self.data)
        else:
            data_stats[f"mode {self.name}"] = mode(self.value_counts())

        return data_stats


class ClientData(ColumnData):
    def __init__(self, data_csv: dict):
        self.new_data_csv = self.reoganize_data()

        for element in data_csv:
            self.columns = list(element.keys())
        self.dimension = (len(data_csv), len(self.columns))

        for key, value in self.new_data_csv.items():
            setattr(self, key, ColumnData(name=key, data=value))

    def reoganize_data(self):
        """ la methode permet de reorganiser les information du csv en pair clé valeur
            --toute les donnee d'une cliee serons organiser sous forme de list---
            ------------------------------------
            attribue:
            --------
            init_data_dic: de type dict, creation d'un dictionnaire avec les paire des colonne du csv et liste vide comme valeur
            return: retourne un dictionnaire de paire colonne csv et data sous forme de liste
        """
        init_data_dic = {val: [] for val in self.columns}
        for element in self.data_csv:
            for key, value in element.items():
                init_data_dic[key] += [value]

        return init_data_dic

    def get_column_by_name(self, name):
        """ la methode permet de renvoyer une colonne du csv
            ------------------------------------
            attribue:
            --------
            obj_name: de type class ColumnData, creation d'un objet representant une colonne du csv
            return: renvoie un objet class ColumnData
        """
        # last version
        #obj_name = ColumnData(name=name, data=self.new_data_csv[name])
        #return obj_name.name

        if hasattr(self, name):
            return getattr(self, name)
        raise AttributeError(f"La colonne '{name}' n'existe pas.")
        

    def get_row_by_index(self, index: int) -> list:
        row_list = []
        for dict_val in self.new_data_csv.values():
            row_list.append(dict_val[index])
        
        return row_list

    def stats_data(self):
        pass

    def build_data_json(self, mode):
        pass

        """for col_name, col_data_list in data_by_column.items():
            column_obj = ColumnData(name=col_name, data=col_data_list)
            # Et on l'affecte comme attribut à notre objet ClientData !
            setattr(self, col_name, column_obj)"""

        # Maintenant, tu peux faire self.age, self.job, etc. et ils seront des objets ColumnData !
        

def load_csv_data(data_from_csv) -> ClientData:
    pass


def preprocess_data() -> ClientData:
    pass