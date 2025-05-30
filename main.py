from flask import Flask, request, Response
import csv, io, datetime

app = Flask(__name__)

CSV_HEADER = ["Datum", "Buchungstext", "Betrag", "Kategorie"]
KAT_MAPPING = {
    "Lebensmittel": "Allgemeine Betriebsausgaben",
    "Miete":        "Raumkosten",
    "Freizeit":     "Sonstige nicht abzugsfähige",
    "Fixkosten":    "Allgemeine Betriebsausgaben"
}

@app.post("/export/elster")
def export_elster():
    data = request.get_json(force=True)
    out = io.StringIO(); writer = csv.writer(out, delimiter=';')
    writer.writerow(CSV_HEADER)

    for b in data.get("bookings", []):
        writer.writerow([
            b.get("date", datetime.date.today().isoformat()),
            b.get("text", ""),
            b.get("amount", 0),
            KAT_MAPPING.get(b.get("category", ""), "Sonstiges")
        ])

    return Response(
        "\ufeff" + out.getvalue(),               # UTF-8 BOM
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=euer.csv"}
    )

@app.get("/")
def root():
    return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
