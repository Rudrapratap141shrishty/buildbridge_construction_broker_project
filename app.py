import sqlite3
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, abort

app = Flask(__name__)
app.secret_key = "change-this-development-secret"
DB_PATH = Path(__file__).with_name("buildbridge.db")

CATEGORIES = ["All", "Construction Contractor", "Property Broker", "Building Materials", "Architect", "Interior Designer"]

SEED_LISTINGS = [
    ("Sharma Construction Group", "Construction Contractor", "Prayagraj", "Residential construction, renovation and turnkey home projects.", "9876501234", "₹1,500–₹2,200 / sq. ft.", "4.8"),
    ("Aarav Property Connect", "Property Broker", "Lucknow", "Residential plots, flats and verified property-site visits.", "9876502345", "Commission based", "4.6"),
    ("BuildMart Supplies", "Building Materials", "Varanasi", "Cement, TMT steel, bricks, sand and aggregate supply.", "9876503456", "Quote on request", "4.5"),
    ("Studio Brick & Beam", "Architect", "Kanpur", "Architectural plans, 3D elevations and building permission drawings.", "9876504567", "From ₹15,000", "4.9"),
    ("NestCraft Interiors", "Interior Designer", "Prayagraj", "Modular kitchens, wardrobes and complete home interiors.", "9876505678", "Quote on request", "4.7"),
    ("Verma Build Solutions", "Construction Contractor", "Jaunpur", "Small homes, boundary walls, structural repairs and extensions.", "9876506789", "Site estimate", "4.4"),
]

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS listings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                business_name TEXT NOT NULL,
                category TEXT NOT NULL,
                city TEXT NOT NULL,
                description TEXT NOT NULL,
                phone TEXT NOT NULL,
                price TEXT NOT NULL,
                rating TEXT NOT NULL DEFAULT 'New'
            )
        """)
        count = conn.execute("SELECT COUNT(*) FROM listings").fetchone()[0]
        if count == 0:
            conn.executemany("""
                INSERT INTO listings (business_name, category, city, description, phone, price, rating)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, SEED_LISTINGS)

@app.route("/")
def home():
    query = request.args.get("q", "").strip()
    category = request.args.get("category", "All")
    city = request.args.get("city", "").strip()
    sql = "SELECT * FROM listings WHERE 1=1"
    params = []
    if query:
        sql += " AND (business_name LIKE ? OR description LIKE ? OR category LIKE ?)"
        params.extend([f"%{query}%", f"%{query}%", f"%{query}%"])
    if category != "All":
        sql += " AND category = ?"
        params.append(category)
    if city:
        sql += " AND city LIKE ?"
        params.append(f"%{city}%")
    sql += " ORDER BY id DESC"
    with get_db() as conn:
        listings = conn.execute(sql, params).fetchall()
        total = conn.execute("SELECT COUNT(*) FROM listings").fetchone()[0]
    return render_template("index.html", listings=listings, categories=CATEGORIES,
                           query=query, category=category, city=city, total=total)

@app.route("/listing/<int:listing_id>")
def listing_detail(listing_id):
    with get_db() as conn:
        listing = conn.execute("SELECT * FROM listings WHERE id = ?", (listing_id,)).fetchone()
    if listing is None:
        abort(404)
    return render_template("detail.html", listing=listing)

@app.route("/add", methods=["GET", "POST"])
def add_listing():
    if request.method == "POST":
        fields = {
            "business_name": request.form.get("business_name", "").strip(),
            "category": request.form.get("category", "").strip(),
            "city": request.form.get("city", "").strip(),
            "description": request.form.get("description", "").strip(),
            "phone": request.form.get("phone", "").strip(),
            "price": request.form.get("price", "").strip(),
        }
        if not all(fields.values()):
            flash("Please fill in every field.")
            return render_template("add.html", categories=CATEGORIES[1:], values=fields), 400
        if fields["category"] not in CATEGORIES[1:]:
            flash("Please select a valid category.")
            return render_template("add.html", categories=CATEGORIES[1:], values=fields), 400
        if len(fields["business_name"]) > 100 or len(fields["description"]) > 1000:
            flash("Business name or description is too long.")
            return render_template("add.html", categories=CATEGORIES[1:], values=fields), 400
        with get_db() as conn:
            cursor = conn.execute("""
                INSERT INTO listings (business_name, category, city, description, phone, price, rating)
                VALUES (?, ?, ?, ?, ?, ?, 'New')
            """, tuple(fields.values()))
            new_id = cursor.lastrowid
        flash("Your listing was added successfully.")
        return redirect(url_for("listing_detail", listing_id=new_id))
    return render_template("add.html", categories=CATEGORIES[1:], values={})

@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
