import pandas as pd
import numpy as np
import datetime

### Interface ###

class MapWriter():

    slots = ("_df_origin", "_target_path", "_df", "_output", "_selector_names", "_coords", "_init_zoom")

    
    @staticmethod
    def html_friendly_name(s):
        return s.replace("_", "-")

    
    def __init__(self):
        self._df_origin = "./df_with_geo_data.csv"
        self._template_path = "./map_template.html"
        self._target_path = "./map_out.html"
        self._df = pd.read_csv(self._df_origin)
        self._selector_names = {"call_reason": "All reasons", "call_taker": "All call takers", "street": "All streets"}
        self._coords = [42.7, -73.2]
        self._init_zoom = 12


    def selector_html(self):
        result = ""
        for selection_box in self._selector_names:
            result += "<select name=\"" + MapWriter.html_friendly_name(selection_box) + "\" class=\"custom-select\" id=\""+ MapWriter.html_friendly_name(selection_box) +"\" onchange=\"updateMap()\">\n<option value=\"" + self._selector_names[selection_box]  + "\">" + self._selector_names[selection_box] + "</option>\n"
            list_of_reasons = list(set(self._df[selection_box]))
            list_of_reasons.sort()
            for reason in list_of_reasons:
                result += "<option value=\"" + reason + "\">" + reason + "</option>\n"
            result += "</select>\n"
        return result


    def write_template_to_html(self):
        self._output = ""
        with open(self._template_path,'r') as f:
            lines = f.readlines()
            for line in lines:
                self._output += line
                if (line == "  <!--SELECTORS-->\n"):
                    self._output += self.selector_html()
                elif (line == "  //MAP\n"):
                    self._output += self.map_html()
                elif (line == "  //FUNCTIONS\n"):
                    self._output += self.functions()
        with open(self._target_path, 'w') as f:
            f.write(self._output)

            
    def functions(self):
        result = ""
        result += "function currentAttributes() {\n"
        result += "var result = new Map();\n"
        for selection_box in self._selector_names:
            result += "result.set(\"" + MapWriter.html_friendly_name(selection_box) + "\", $(\'#" + MapWriter.html_friendly_name(selection_box) + "\').val());\n"
        result += "return result;\n"
        result += "}\n"

        result += "function updateMap() {\n"
        result += "attributes = currentAttributes();\n"
        result += "markers.forEach(function(key, marker) {\n"
        result += "if (!marker_cluster.hasLayer(marker)) {\n"
        result += "marker.addTo(marker_cluster);\n"
        result += "}"
        for selection_box in self._selector_names:
            result += "if (marker.attributes[\"" + MapWriter.html_friendly_name(selection_box) + "\"] != attributes.get(\"" + MapWriter.html_friendly_name(selection_box) + "\") && attributes.get(\"" + MapWriter.html_friendly_name(selection_box) + "\") != \"" + self._selector_names[selection_box] + "\") {\n"
            result += "marker_cluster.removeLayer(marker);\n"
            result += "}\n"
        result += "});\n}\n"

        return result

    
    def map_html(self):
        result = ""
        result += "var map = L.map(\"map\").setView(" + str(self._coords) + ", " + str(self._init_zoom) + ")\n"
        result += "var tileLayer = L.tileLayer(\'https://tile.openstreetmap.org/{z}/{x}/{y}.png\', {\nmaxZoom: 18, attribution: \'&copy; <a href=\"http://www.openstreetmap.org/copyright\">OpenStreetMap</a>\'\n}).addTo(map);\n"
        result += "var marker_cluster = L.markerClusterGroup({});\nmap.addLayer(marker_cluster);"
        result += "var myIcon = L.AwesomeMarkers.icon({\"extraClasses\": \"fa-rotate-0\", \"icon\": \"building\", \"iconColor\": \"white\", \"markerColor\": \"black\", \"prefix\": \"fa\"});\n" # TODO implement icon options
        result += "let markers = new Map();\n"

        for lab, row in self._df.iterrows():
            marker_coords = list(row[['latitude','longitude']])
            if False in [marker_coords[i] == marker_coords[i] for i in range(len(marker_coords))]:
                continue
            str_coords = str(marker_coords)
            marker_label = "marker" + str(lab)
            popup_label = "popup" + str(lab)
            html_label = "popupHtml" + str(lab)

            ### Data ###
            # TODO modularize, abstract, implement option to format popups and other displays
            pdf_page = row['pdf_page']
            street = row['street']
            date_time_object = datetime.datetime.strptime(row["call_datetime"], "%Y-%m-%d %H:%M:%S")if row["call_datetime"] == row["call_datetime"] else None
            date_time = date_time_object.strftime("%m/%d/%Y, %I:%M%p").lower() if not date_time_object is None else ""
            year = date_time_object.strftime("%Y") if not date_time_object is None else "No date/time found."
            call_reason = row['call_reason']
            call_taker = row['call_taker']
            narrative = row['narrative'].replace("\"", "\\\"") if row['narrative'] == row['narrative'] else ""
            py_dict = {"pdf_page": pdf_page, "street": street, "date_time": date_time, "call-reason": call_reason, "narrative": narrative, "call-taker": call_taker}
                
            result += "var " + marker_label + " = L.marker(" + str_coords + ",{icon: myIcon});\n"
            result += marker_label + ".attributes = {" + ", ".join(["\"" + str(key) + "\": \"" + str(value) + "\"" for key, value in zip(py_dict.keys(), py_dict.values())])+ "}\n"
            result += "var " + popup_label + " = L.popup({\"maxWidth\": 400, \"minWidth\": 400});\n"
            result += "var " + html_label + " = $(`<div id=\"" + html_label + "\" style=\"width: 100.0%; height: 100.0%;\"><a href=../../data/primary_datasets/Logs{}.pdf#page={} target=\"blank\" rel=\"noopener noreferrer\">Log No. {}</a><br>{}<br>{}<br>Call Reason: {}<br>Call Taker: {}<br>Narrative:<br>{}</div>`)[0];\n".format(year, str(pdf_page), str(row['log_num']), street, date_time, call_reason, call_taker, narrative)
            result += popup_label + ".setContent(" + html_label + ");\n"
            result += marker_label + ".bindPopup(" + popup_label + ");\n"
            result += marker_label + ".bindTooltip(\n`<div>" + street + "</div>`,{\"sticky\": true});\n"
            result += marker_label + ".addTo(marker_cluster);\n"

            result += "markers.set(" + marker_label + ", " + str(lab) + ");\n"

        result += "var attributes\n"
        result += "updateMap()\n"

        return result


if __name__ == "__main__":
    mw = MapWriter()
    mw.write_template_to_html()
