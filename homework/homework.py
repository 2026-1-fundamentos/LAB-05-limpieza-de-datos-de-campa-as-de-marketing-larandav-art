"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """
    import os
    import zipfile
    
    import pandas as pd

    # Create output directory if it doesn't exist
    os.makedirs("files/output", exist_ok=True)

    # Initialize list to store all data
    all_data = []

    # Read and process each zip file
    for i in range(10):
        zip_file = f"files/input/bank-marketing-campaing-{i}.csv.zip"
        with zipfile.ZipFile(zip_file, "r") as zip_ref:
            # Get the CSV file name inside the zip
            csv_file = zip_ref.namelist()[0]
            # Read the CSV directly from the zip
            df = pd.read_csv(zip_ref.open(csv_file))
            all_data.append(df)

    # Combine all data
    data = pd.concat(all_data, ignore_index=True)

    # Mapping for month abbreviations to numbers
    month_map = {
        "jan": "01",
        "feb": "02",
        "mar": "03",
        "apr": "04",
        "may": "05",
        "jun": "06",
        "jul": "07",
        "aug": "08",
        "sep": "09",
        "oct": "10",
        "nov": "11",
        "dec": "12",
    }

    # ============ PROCESS CLIENT DATA ============
    client = data[
        ["client_id", "age", "job", "marital", "education", "credit_default", "mortgage"]
    ].copy()

    # Transform job: change "." to "" and "-" to "_"
    client["job"] = client["job"].str.replace(".", "", regex=False).str.replace(
        "-", "_", regex=False
    )

    # Transform education: change "." to "_" and "unknown" to pd.NA
    client["education"] = client["education"].str.replace(".", "_", regex=False)
    client["education"] = client["education"].replace("unknown", pd.NA)

    # Transform credit_default: "yes" to 1, others to 0
    client["credit_default"] = (client["credit_default"] == "yes").astype(int)

    # Transform mortgage: "yes" to 1, others to 0
    client["mortgage"] = (client["mortgage"] == "yes").astype(int)

    # ============ PROCESS CAMPAIGN DATA ============
    campaign = data[
        [
            "client_id",
            "number_contacts",
            "contact_duration",
            "previous_campaign_contacts",
            "previous_outcome",
            "campaign_outcome",
            "day",
            "month",
        ]
    ].copy()

    # Transform previous_outcome: "success" to 1, others to 0
    campaign["previous_outcome"] = (campaign["previous_outcome"] == "success").astype(int)

    # Transform campaign_outcome: "yes" to 1, others to 0
    campaign["campaign_outcome"] = (campaign["campaign_outcome"] == "yes").astype(int)

    # Create date field: YYYY-MM-DD format with year 2022
    # Convert month names to numbers
    month_numbers = campaign["month"].str.lower().map(month_map)
    day_numbers = campaign["day"].astype(str).str.zfill(2)
    campaign["last_contact_date"] = "2022-" + month_numbers + "-" + day_numbers

    # Drop day and month columns as they are no longer needed
    campaign = campaign.drop(columns=["day", "month"])

    # ============ PROCESS ECONOMICS DATA ============
    economics = data[
        ["client_id", "cons_price_idx", "euribor_three_months"]
    ].copy()

    # ============ SAVE TO CSV ============
    client.to_csv("files/output/client.csv", index=False)
    campaign.to_csv("files/output/campaign.csv", index=False)
    economics.to_csv("files/output/economics.csv", index=False)

    return


if __name__ == "__main__":
    clean_campaign_data()
