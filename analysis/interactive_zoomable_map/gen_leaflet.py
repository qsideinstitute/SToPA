import pandas as pd
import numpy as np
import datetime

df = pd.read_csv("df_with_geo_data.csv")

output = ""

selector_name = "call-reason"
all_option_name = "All reasons"

with open("map_template.html",'r') as f:
    lines = f.readlines()
    for line in lines:
        output += line
        if (line == "  <!--SELECTORS-->\n"):
            output += "<select name=\"" + selector_name + "\" class=\"custom-select\" id=\""+selector_name+"\" onchange=\"updateMap()\">\n<option value=\""+all_option_name+"\">"+all_option_name+"</option>\n"
            list_of_reasons = list(set(df['call_reason']))
            list_of_reasons.sort()
            for reason in list_of_reasons:
                output += "<option value=\"" + reason + "\">" + reason + "</option>\n"
            output += "</select"
                
        elif (line == "  //MAP\n"):
            map_coords = [42.7, -73.2]
            init_zoom = 12
            output += "var map = L.map(\"map\").setView(" + str(map_coords) + ", " + str(init_zoom) + ")\n"
            output += "var tileLayer = L.tileLayer(\'https://tile.openstreetmap.org/{z}/{x}/{y}.png\', {\nmaxZoom: 18, attribution: \'&copy; <a href=\"http://www.openstreetmap.org/copyright\">OpenStreetMap</a>\'\n}).addTo(map);\n"
            output += "var marker_cluster = L.markerClusterGroup({});\nmap.addLayer(marker_cluster);"

            output += "var myIcon = L.AwesomeMarkers.icon({\"extraClasses\": \"fa-rotate-0\", \"icon\": \"building\", \"iconColor\": \"white\", \"markerColor\": \"black\", \"prefix\": \"fa\"});\n"

            output += "let markers = new Map();\n"

            for lab, row in df.iterrows():
                marker_coords = list(row[['latitude','longitude']])
                if False in [marker_coords[i] == marker_coords[i] for i in range(len(marker_coords))]:
                    continue
                str_coords = str(marker_coords)
                marker_label = "marker" + str(lab)
                popup_label = "popup" + str(lab)
                html_label = "popupHtml" + str(lab)

                ### Data ###
                pdf_page = row['pdf_page']
                street = row['street']
                date_time_object = datetime.datetime.strptime(row["call_datetime"], "%Y-%m-%d %H:%M:%S")if row["call_datetime"] == row["call_datetime"] else None
                date_time = date_time_object.strftime("%m/%d/%Y, %I:%M%p").lower() if not date_time_object is None else ""
                year = date_time_object.strftime("%Y") if not date_time_object is None else "No date/time found."
                call_reason = row['call_reason']
                narrative = row['narrative'].replace("\"", "\\\"") if row['narrative'] == row['narrative'] else ""
                py_dict = {"pdf_page": pdf_page, "street": street, "date_time": date_time, "call-reason": call_reason, "narrative": narrative}
                
                output += "var " + marker_label + " = L.marker(" + str_coords + ",{icon: myIcon});\n"
                output += marker_label + ".attributes = {" + ", ".join(["\"" + str(key) + "\": \"" + str(value) + "\"" for key, value in zip(py_dict.keys(), py_dict.values())])+ "}\n"
                output += "var " + popup_label + " = L.popup({\"maxWidth\": 300, \"minWidth\": 300});\n"
                output += "var " + html_label + " = $(`<div id=\"" + html_label + "\" style=\"width: 100.0%; height: 100.0%;\"><a href=../../data/primary_datasets/Logs{}.pdf#page={} target=\"blank\" rel=\"noopener noreferrer\">Log No. {}</a><br>{}<br>{}<br>Call Reason:<br>{}<br>Narrative:<br>{}</div>`)[0];\n".format(year, str(pdf_page), str(row['log_num']), street, date_time, call_reason, narrative)
                output += popup_label + ".setContent(" + html_label + ");\n"
                output += marker_label + ".bindPopup(" + popup_label + ");\n"
                output += marker_label + ".bindTooltip(\n`<div>" + street + "</div>`,{\"sticky\": true});\n"
                output += marker_label + ".addTo(marker_cluster);\n"

                output += "markers.set(" + marker_label + ", " + str(lab) + ");\n"
                

with open("map_out.html", 'w') as f:
    f.write(output)
